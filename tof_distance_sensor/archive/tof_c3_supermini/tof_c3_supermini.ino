/*
 * ToF Distance Sensor — ESP32-C3 SuperMini + VL53L0X x2
 * 基於合作者版本，修改輸出格式以相容現有 Max/MSP patch
 *
 * 改動摘要（相對於原始版本）：
 *   1. 輸出格式改為 OSC 風格 "/tof fX fY rX rY"，相容 Max 的 [route /tof] + [unpack i i i i]
 *   2. 校正/錯誤訊息統一為 /status、/cal_done、/error 前綴
 *   3. 加入暖機階段（500ms 丟棄不穩定讀數）
 *   4. 校正改用中位數（比最小值更抗雜訊）
 *   5. 用 millis() 計時取代 delay()（避免累積延遲）
 *   6. 加入 Serial 指令：'c' = 重新校正，'r' = 重啟濾波器
 *   7. 同時輸出 raw 值供 Max 除錯
 *   8. 三層濾波：Median(殺突波) → 自適應 EMA(靜穩動快) → Deadband(鎖微抖)
 *
 * ── 硬體接線（ESP32-C3 SuperMini）─────────────────────
 *   I2C SDA   → GPIO5     I2C SCL  → GPIO6
 *   XSHUT_1   → GPIO3     感測器 1 硬體關閉腳
 *   XSHUT_2   → GPIO4     感測器 2 硬體關閉腳
 *   VCC       → 3.3V      GND → GND
 *   感測器 1 地址：0x30，感測器 2 地址：0x31
 *
 * ── Serial 輸出（115200 baud）─────────────────────────
 *   正常運作："/tof fX fY rX rY\n"（50Hz）
 *   校正中  ："/status calibrating N\n"（倒數秒數）
 *   校正完成："/cal_done offsetX offsetY samplesX samplesY\n"
 *   正常運行："/status running\n"
 *   濾波重置："/status filters_reset\n"
 *   錯誤    ："/error <message>\n"
 *
 * ── Serial 指令 ───────────────────────────────────────
 *   'c' → 重新校正（暖機 + 校正）
 *   'r' → 重啟濾波器（保留 offset）
 *
 * ── Max/MSP 接收 ──────────────────────────────────────
 *   [serial <port> 115200] → [sel 10] → [zl group] → [itoa] → [fromsymbol]
 *   → [route /tof /status /cal_done /error]
 *        |
 *   [unpack i i i i] → filtered_x, filtered_y, raw_x, raw_y
 */

#include <Wire.h>
#include "Adafruit_VL53L0X.h"
#include <math.h>

// =======================
// ESP32-C3 SuperMini Pins
// =======================
#define I2C_SDA 5
#define I2C_SCL 6
#define XSHUT_1 3
#define XSHUT_2 4
#define ADDR_1 0x30
#define ADDR_2 0x31

Adafruit_VL53L0X lox1 = Adafruit_VL53L0X();
Adafruit_VL53L0X lox2 = Adafruit_VL53L0X();

// === 參數 ===
const uint32_t TIMING_BUDGET_US = 33000;  // 33ms timing budget
const unsigned long WARMUP_MS   = 500;    // 暖機丟棄時間
const unsigned long CALIB_MS    = 5000;   // 校正收集時間（原 10s，配合現有流程改 5s）
const unsigned long OUTPUT_INTERVAL_MS = 20; // 50Hz 輸出
const int RANGE_MIN = 0;
const int RANGE_MAX = 2000;

// === 三層濾波參數 ===
// 第一層：Median 濾波（殺突波/離群值）
const int MEDIAN_WINDOW = 3;      // 窗口大小，3 = 最低延遲又能擋單次突波

// 第二層：自適應 EMA（靜止穩、移動快）
const float ALPHA_SLOW = 0.12f;   // 靜止/緩動時 → 很平滑
const float ALPHA_FAST = 0.6f;    // 快速移動時 → 跟手
const float ADAPTIVE_THRESH = 10.0f; // 超過此 mm 差距切快速模式

// 第三層：Deadband（鎖住微小抖動）
const int DEAD_BAND_MM = 3;       // 變化 ≤ 3mm 不更新（原 2mm 容易被穿透）

const int OUT_OF_RANGE = -1;

// === 感測器狀態 ===
enum State { STATE_WARMUP, STATE_CALIBRATING, STATE_RUNNING };
State currentState = STATE_WARMUP;
unsigned long stateStartMs = 0;
unsigned long lastOutputMs = 0;

// === 校正（改用中位數）===
int offsetX = 0, offsetY = 0;
int calibSamplesX[256];
int calibSamplesY[256];
int calibCountX = 0;
int calibCountY = 0;

// === Median 濾波器狀態 ===
int medBufX[MEDIAN_WINDOW], medBufY[MEDIAN_WINDOW];
int medIdxX = 0, medIdxY = 0;
int medFillX = 0, medFillY = 0;

// === EMA + Deadband 狀態 ===
bool emaInitX = false, emaInitY = false;
float emaX = 0, emaY = 0;
int stableX = 0, stableY = 0;

// === 最後有效輸出 ===
int lastValidX = 0, lastValidY = 0;
int lastRawX = 0, lastRawY = 0;

// --------------------------------------------------
// 工具函式
// --------------------------------------------------

// qsort 比較
int cmpInt(const void *a, const void *b) {
  return (*(int *)a) - (*(int *)b);
}

// 陣列中位數
int arrayMedian(int *arr, int n) {
  if (n <= 0) return 0;
  int tmp[256];
  int count = min(n, 256);
  memcpy(tmp, arr, count * sizeof(int));
  qsort(tmp, count, sizeof(int), cmpInt);
  if (count % 2 == 1) return tmp[count / 2];
  return (tmp[count / 2 - 1] + tmp[count / 2]) / 2;
}

// 第一層：Median 濾波器 — 插入新值，回傳中位數（殺突波）
int medianFilter(int *buf, int &idx, int &fill, int value) {
  buf[idx] = value;
  idx = (idx + 1) % MEDIAN_WINDOW;
  if (fill < MEDIAN_WINDOW) fill++;

  // 排序副本取中位數
  int tmp[MEDIAN_WINDOW];
  memcpy(tmp, buf, fill * sizeof(int));
  qsort(tmp, fill, sizeof(int), cmpInt);
  return tmp[fill / 2];
}

// 第二層 + 第三層：自適應 EMA → Deadband
int applyStableFilter(int medVal, bool &inited, float &ema, int &stableOut) {
  if (medVal == OUT_OF_RANGE) return OUT_OF_RANGE;

  // --- 自適應 EMA ---
  if (!inited) {
    ema = medVal;
    stableOut = medVal;
    inited = true;
    return stableOut;
  }
  float diff = fabs((float)medVal - ema);
  float alpha = (diff > ADAPTIVE_THRESH) ? ALPHA_FAST : ALPHA_SLOW;
  ema = alpha * medVal + (1.0f - alpha) * ema;
  int smooth = (int)lround(ema);

  // --- Deadband ---
  if (abs(smooth - stableOut) <= DEAD_BAND_MM) {
    return stableOut;   // 變化太小，鎖住
  } else {
    stableOut = smooth;
    return stableOut;
  }
}

// 重置濾波器
void resetFilters() {
  medIdxX = medIdxY = 0;
  medFillX = medFillY = 0;
  emaInitX = emaInitY = false;
  emaX = emaY = 0;
  stableX = stableY = 0;
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

// 讀取感測器
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
  delay(500);

  Wire.begin(I2C_SDA, I2C_SCL);
  // 注意：ESP32-C3 的 Wire.setClock() 有時不穩，可視情況移除
  Wire.setClock(400000);

  pinMode(XSHUT_1, OUTPUT);
  pinMode(XSHUT_2, OUTPUT);

  // 兩顆先關
  digitalWrite(XSHUT_1, LOW);
  digitalWrite(XSHUT_2, LOW);
  delay(10);

  // 開第一顆 → 改地址
  digitalWrite(XSHUT_1, HIGH);
  delay(10);
  if (!lox1.begin(0x29, false, &Wire)) {
    Serial.println("/error sensor1_init_failed");
    while (1) delay(1000);
  }
  lox1.setAddress(ADDR_1);

  // 開第二顆 → 改地址
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

  // === Serial 指令 ===
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

  // === 校正階段（收集中位數）===
  if (currentState == STATE_CALIBRATING) {
    if (validX && calibCountX < 256) {
      calibSamplesX[calibCountX++] = rawX;
    }
    if (validY && calibCountY < 256) {
      calibSamplesY[calibCountY++] = rawY;
    }

    unsigned long elapsed = now - stateStartMs;

    // 每秒倒數
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

  // === 正常運行：三層濾波 ===
  if (validX) {
    int zeroed = max(0, rawX - offsetX);
    int med = medianFilter(medBufX, medIdxX, medFillX, zeroed);  // 第一層
    int filtered = applyStableFilter(med, emaInitX, emaX, stableX); // 第二+三層
    if (filtered != OUT_OF_RANGE) {
      lastValidX = filtered;
    }
    lastRawX = zeroed;
  }

  if (validY) {
    int zeroed = max(0, rawY - offsetY);
    int med = medianFilter(medBufY, medIdxY, medFillY, zeroed);  // 第一層
    int filtered = applyStableFilter(med, emaInitY, emaY, stableY); // 第二+三層
    if (filtered != OUT_OF_RANGE) {
      lastValidY = filtered;
    }
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
