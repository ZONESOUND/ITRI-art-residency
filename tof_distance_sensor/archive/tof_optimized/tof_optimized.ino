/*
 * ToF Distance Sensor (Optimized) — ESP32 + VL53L0X x2
 * ToF 雙感測器距離測量 — 優化版
 *
 * 功能：
 *   - 雙感測器初始化 + 錯誤檢查（初始化失敗時停止並印出錯誤）
 *   - 三階段狀態機：暖機（500ms 丟棄）→ 校正（5s 收集中位數）→ 運作
 *   - 中位數基準校正：收集 5 秒有效樣本，取中位數作為零點偏移
 *   - 雙層平滑濾波：Median 窗口=3（去除離群值）+ 自適應 EMA
 *       靜止/緩動 → alpha=0.15（平滑），快速移動 → alpha=0.8（跟手）
 *   - 量測品質控制：RangeStatus != 4，距離限制 0~2000mm
 *   - 固定 50Hz 輸出（OUTPUT_INTERVAL_MS = 20ms）
 *   - Serial 指令：'c' = 重新校正，'r' = 重啟濾波器
 *
 * ── 硬體接線 ──────────────────────────────────────────────
 *   I2C SDA   → GPIO21    I2C SCL  → GPIO22（400kHz Fast Mode）
 *   XSHUT_1   → GPIO25    感測器 1 硬體關閉腳（低電位=關閉）
 *   XSHUT_2   → GPIO26    感測器 2 硬體關閉腳
 *   VCC       → 3.3V      GND → GND
 *   感測器 1 地址：0x30，感測器 2 地址：0x31（預設 0x29 依序改地址）
 *   注意：VL53L0X 只能接 3.3V，不可接 5V。
 *
 * ── Serial 輸出格式（115200 baud）────────────────────────
 *   暖機中  ：（無輸出，等待 500ms）
 *   校正中  ："/status calibrating 5\n"（每秒倒數）
 *   校正完成："/cal_done offsetX offsetY samplesX samplesY\n"
 *   正常運作："/tof X Y rawX rawY\n"（50Hz）
 *             X, Y = 中位數 + EMA 平滑後距離（mm）
 *             rawX, rawY = 僅歸零無平滑的距離（mm）
 *
 * ── Max/MSP 接收 ──────────────────────────────────────────
 *   [serial <port> 115200] → [fromsymbol]
 *   → [route /tof] → [unpack i i i i] → X Y rawX rawY
 */

#include <Wire.h>
#include "Adafruit_VL53L0X.h"

// === 硬體設定 ===
#define I2C_SDA 21
#define I2C_SCL 22
#define XSHUT_1 25
#define XSHUT_2 26
#define ADDR_1 0x30
#define ADDR_2 0x31

// === 參數 ===
const uint32_t TIMING_BUDGET_US = 33000;   // 33ms timing budget
const unsigned long WARMUP_MS   = 500;     // 暖機丟棄時間
const unsigned long CALIB_MS    = 5000;    // 校正收集時間
const unsigned long OUTPUT_INTERVAL_MS = 20; // 50Hz 輸出
const int RANGE_MIN = 0;
const int RANGE_MAX = 2000;

// === 中位數濾波器 ===
const int MEDIAN_WINDOW = 3;

// === 自適應 EMA ===
// 變化小時用 ALPHA_SLOW（平滑），變化大時用 ALPHA_FAST（跟手）
const float EMA_ALPHA_SLOW = 0.15f;  // 靜止/緩動時的平滑度
const float EMA_ALPHA_FAST = 0.8f;   // 快速移動/剛停下時的反應速度
const float ADAPTIVE_THRESHOLD = 15.0f; // 超過此 mm 差距就切快速模式

// === 感測器 ===
Adafruit_VL53L0X lox1;
Adafruit_VL53L0X lox2;

// === 狀態 ===
enum State { STATE_WARMUP, STATE_CALIBRATING, STATE_RUNNING };
State currentState = STATE_WARMUP;
unsigned long stateStartMs = 0;
unsigned long lastOutputMs = 0;

// === 校正 ===
int offsetX = 0, offsetY = 0;
int calibSamplesX[256];
int calibSamplesY[256];
int calibCountX = 0;
int calibCountY = 0;

// === 中位數濾波器緩衝 ===
int medBufX[MEDIAN_WINDOW];
int medBufY[MEDIAN_WINDOW];
int medIdxX = 0, medIdxY = 0;
int medFillX = 0, medFillY = 0;

// === EMA 狀態 ===
float emaX = 0, emaY = 0;
bool emaInitX = false, emaInitY = false;

// === 最後有效輸出值 ===
int lastValidX = 0, lastValidY = 0;
int lastRawX = 0, lastRawY = 0;

// --------------------------------------------------
// 工具函式
// --------------------------------------------------

// 排序用比較（for qsort）
int cmpInt(const void *a, const void *b) {
  return (*(int *)a) - (*(int *)b);
}

// 計算陣列中位數
int arrayMedian(int *arr, int n) {
  if (n <= 0) return 0;
  int tmp[256];
  int count = min(n, 256);
  memcpy(tmp, arr, count * sizeof(int));
  qsort(tmp, count, sizeof(int), cmpInt);
  if (count % 2 == 1) return tmp[count / 2];
  return (tmp[count / 2 - 1] + tmp[count / 2]) / 2;
}

// 中位數濾波器：插入值並回傳中位數
int medianFilter(int *buf, int &idx, int &fill, int value) {
  buf[idx] = value;
  idx = (idx + 1) % MEDIAN_WINDOW;
  if (fill < MEDIAN_WINDOW) fill++;

  int tmp[MEDIAN_WINDOW];
  memcpy(tmp, buf, fill * sizeof(int));
  qsort(tmp, fill, sizeof(int), cmpInt);
  return tmp[fill / 2];
}

// 自適應 EMA 更新：變化大 → alpha 大（跟手），變化小 → alpha 小（平滑）
float emaUpdate(float &ema, bool &inited, float value) {
  if (!inited) {
    ema = value;
    inited = true;
  } else {
    float diff = abs(value - ema);
    float alpha = (diff > ADAPTIVE_THRESHOLD) ? EMA_ALPHA_FAST : EMA_ALPHA_SLOW;
    ema = alpha * value + (1.0f - alpha) * ema;
  }
  return ema;
}

// 重置濾波器
void resetFilters() {
  medIdxX = medIdxY = 0;
  medFillX = medFillY = 0;
  emaInitX = emaInitY = false;
  emaX = emaY = 0;
}

// 開始校正流程
void startCalibration() {
  currentState = STATE_WARMUP;
  stateStartMs = millis();
  calibCountX = calibCountY = 0;
  offsetX = offsetY = 0;
  resetFilters();
  lastValidX = lastValidY = 0;
  lastRawX = lastRawY = 0;
}

// 讀取感測器，回傳是否有效
// RangeStatus: 0=valid, 1=sigma warn, 2=signal warn, 4=out of range
// status 0/1/2 的數值都可用，只排除 4（完全無效）
bool readSensor(Adafruit_VL53L0X &lox, int &outRaw) {
  VL53L0X_RangingMeasurementData_t m;
  lox.rangingTest(&m, false);
  if (m.RangeStatus != 4) {
    int val = (int)m.RangeMilliMeter;
    if (val >= RANGE_MIN && val <= RANGE_MAX) {
      outRaw = val;
      return true;
    }
  }
  return false;
}

// --------------------------------------------------
// Setup
// --------------------------------------------------
void setup() {
  Serial.begin(115200);
  delay(100);

  Wire.begin(I2C_SDA, I2C_SCL);
  Wire.setClock(400000);

  pinMode(XSHUT_1, OUTPUT);
  pinMode(XSHUT_2, OUTPUT);

  // 兩顆先關
  digitalWrite(XSHUT_1, LOW);
  digitalWrite(XSHUT_2, LOW);
  delay(10);

  // 開第一顆 -> 改地址
  digitalWrite(XSHUT_1, HIGH);
  delay(10);
  if (!lox1.begin(0x29, false, &Wire)) {
    Serial.println("/error sensor1_init_failed");
    while (1) delay(1000);
  }
  lox1.setAddress(ADDR_1);

  // 開第二顆 -> 改地址
  digitalWrite(XSHUT_2, HIGH);
  delay(10);
  if (!lox2.begin(0x29, false, &Wire)) {
    Serial.println("/error sensor2_init_failed");
    while (1) delay(1000);
  }
  lox2.setAddress(ADDR_2);

  // Timing budget
  lox1.setMeasurementTimingBudgetMicroSeconds(TIMING_BUDGET_US);
  lox2.setMeasurementTimingBudgetMicroSeconds(TIMING_BUDGET_US);

  // 開始校正
  startCalibration();
}

// --------------------------------------------------
// Loop
// --------------------------------------------------
void loop() {
  unsigned long now = millis();

  // === Serial 指令處理 ===
  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 'c') {
      startCalibration();
      return;
    } else if (cmd == 'r') {
      resetFilters();
      Serial.println("/status filters_reset");
      return;
    }
  }

  // === 讀取感測器 ===
  int rawX, rawY;
  bool validX = readSensor(lox1, rawX);
  bool validY = readSensor(lox2, rawY);

  // === 暖機階段 ===
  if (currentState == STATE_WARMUP) {
    if (now - stateStartMs >= WARMUP_MS) {
      currentState = STATE_CALIBRATING;
      stateStartMs = now;
      Serial.println("/status calibrating 5");
    }
    return;
  }

  // === 校正階段 ===
  if (currentState == STATE_CALIBRATING) {
    // 收集有效樣本
    if (validX && calibCountX < 256) {
      calibSamplesX[calibCountX++] = rawX;
    }
    if (validY && calibCountY < 256) {
      calibSamplesY[calibCountY++] = rawY;
    }

    unsigned long elapsed = now - stateStartMs;

    // 每秒印出倒數
    static unsigned long lastCalPrint = 0;
    if (now - lastCalPrint >= 1000) {
      lastCalPrint = now;
      long remainMs = (long)CALIB_MS - (long)elapsed;
      int remainSec = (remainMs > 0) ? (int)((remainMs + 999) / 1000) : 0;
      Serial.print("/status calibrating ");
      Serial.println(remainSec);
    }

    // 校正結束
    if (elapsed >= CALIB_MS) {
      offsetX = (calibCountX > 0) ? arrayMedian(calibSamplesX, calibCountX) : 0;
      offsetY = (calibCountY > 0) ? arrayMedian(calibSamplesY, calibCountY) : 0;

      Serial.print("/cal_done ");
      Serial.print(offsetX);
      Serial.print(" ");
      Serial.print(offsetY);
      Serial.print(" ");
      Serial.print(calibCountX);
      Serial.print(" ");
      Serial.println(calibCountY);

      currentState = STATE_RUNNING;
      Serial.println("/status running");
      lastOutputMs = now;
    }
    return;
  }

  // === 正常運行：濾波 ===
  if (validX) {
    int zeroed = max(0, rawX - offsetX);
    int med = medianFilter(medBufX, medIdxX, medFillX, zeroed);
    emaUpdate(emaX, emaInitX, (float)med);
    lastValidX = (int)(emaX + 0.5f);
    lastRawX = zeroed;
  }

  if (validY) {
    int zeroed = max(0, rawY - offsetY);
    int med = medianFilter(medBufY, medIdxY, medFillY, zeroed);
    emaUpdate(emaY, emaInitY, (float)med);
    lastValidY = (int)(emaY + 0.5f);
    lastRawY = zeroed;
  }

  // === 固定頻率輸出 ===
  if (now - lastOutputMs >= OUTPUT_INTERVAL_MS) {
    lastOutputMs = now;
    Serial.print("/tof ");
    Serial.print(lastValidX);
    Serial.print(" ");
    Serial.print(lastValidY);
    Serial.print(" ");
    Serial.print(lastRawX);
    Serial.print(" ");
    Serial.println(lastRawY);
  }
}
