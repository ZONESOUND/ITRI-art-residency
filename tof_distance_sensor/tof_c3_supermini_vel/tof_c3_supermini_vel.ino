/*
 * ToF Distance Sensor + Velocity — ESP32-C3 SuperMini + VL53L0X x2
 * 基於 tof_c3_supermini.ino，新增 X/Y 速度輸出
 *
 * 相對於 tof_c3_supermini 的改動：
 *   1. 輸出增加 vX vY 兩個浮點數（mm/s，帶正負方向）
 *   2. 速度從 fX/fY（deadband 後穩定值）計算 → 位置沒變就直接歸零，沒有慣性尾巴
 *   3. 移動中才用 EMA 平滑（VEL_SMOOTH = 0.06）→ 連續 ramp，不會跳動
 *   4. 新增 Serial 指令 'v' 可切換速度輸出開關
 *   5. 按鈕（GPIO0）按下 → 重新校正（不中斷 Serial）
 *   6. 狀態 LED（GPIO8）校正中閃爍，運行中常滅
 *
 * ── 硬體接線（ESP32-C3 SuperMini）─────────────────────
 *   I2C SDA   → GPIO5     I2C SCL  → GPIO6
 *   XSHUT_1   → GPIO4     感測器 1 硬體關閉腳
 *   XSHUT_2   → GPIO3     感測器 2 硬體關閉腳
 *   BUTTON    → GPIO0     外接按鈕（按下 = LOW，重新校正）
 *   LED       → GPIO8     狀態指示燈（校正中閃爍）
 *   VCC       → 3.3V      GND → GND
 *   感測器 1 地址：0x30，感測器 2 地址：0x31
 *
 * ── Serial 輸出（115200 baud）─────────────────────────
 *   正常運作："/tof fX fY rX rY vX vY\n"（50Hz）
 *     fX, fY = 濾波後位移（int, mm, ≥0）
 *     rX, rY = 校正後原始值（int, mm, ≥0）
 *     vX, vY = 速度（float, mm/s, 帶正負）
 *              正值 = 遠離感測器方向
 *              負值 = 靠近感測器方向
 *              典型範圍：慢 ±50, 中 ±200, 快 ±500~1000
 *
 *   校正中  ："/status calibrating N\n"（倒數秒數）
 *   校正完成："/cal_done offsetX offsetY samplesX samplesY\n"
 *   正常運行："/status running\n"
 *   濾波重置："/status filters_reset\n"
 *   錯誤    ："/error <message>\n"
 *
 * ── Serial 指令 ───────────────────────────────────────
 *   'c' → 重新校正（暖機 + 校正）
 *   'r' → 重啟濾波器（保留 offset）
 *   'v' → 切換速度輸出（預設開啟）
 *   "WHO\n" → 回覆 "ID:tof"（裝置識別）
 *
 * ── Max/MSP 接收 ──────────────────────────────────────
 *   [serial <port> 115200] → [sel 10] → [zl group] → [itoa] → [fromsymbol]
 *   → [route /tof /status /cal_done /error]
 *        |
 *   [unpack i i i i f f] → filtered_x, filtered_y, raw_x, raw_y, vel_x, vel_y
 *   （舊版 [unpack i i i i] 也相容，只是忽略速度）
 */

#include <Wire.h>
#include "Adafruit_VL53L0X.h"
#include <math.h>

// =========================
// Device ID (for WHO identification)
// =========================
const char* DEVICE_ID = "tof";

// =======================
// ESP32-C3 SuperMini Pins
// =======================
#define I2C_SDA 5
#define I2C_SCL 6
#define XSHUT_1 4
#define XSHUT_2 3
#define BUTTON_PIN 0
#define STATUS_LED 8
#define ADDR_1 0x30
#define ADDR_2 0x31

Adafruit_VL53L0X lox1 = Adafruit_VL53L0X();
Adafruit_VL53L0X lox2 = Adafruit_VL53L0X();

// === 參數 ===
const uint32_t TIMING_BUDGET_US = 33000;  // 33ms timing budget
const unsigned long WARMUP_MS   = 500;    // 暖機丟棄時間
const unsigned long CALIB_MS    = 5000;   // 校正收集時間
const unsigned long OUTPUT_INTERVAL_MS = 20; // 50Hz 輸出
const int RANGE_MIN = 0;
const int RANGE_MAX = 2000;

// === 三層濾波參數 ===
// 第一層：Median 濾波（殺突波/離群值）
const int MEDIAN_WINDOW = 3;

// 第二層：自適應 EMA（靜止穩、移動快）
const float ALPHA_SLOW = 0.12f;
const float ALPHA_FAST = 0.6f;
const float ADAPTIVE_THRESH = 10.0f;

// 第三層：Deadband（鎖住微小抖動）
const int DEAD_BAND_MM = 3;

const int OUT_OF_RANGE = -1;

// === 速度計算參數 ===
const float VEL_SMOOTH = 0.06f;  // 速度 EMA 平滑係數（越小 ramp 越緩，越大越即時）
                                  // 0.06 @ 50Hz ≈ 0.33s 達到 63% → 連續漸變不跳動
const float DT = OUTPUT_INTERVAL_MS / 1000.0f;  // 每幀秒數（0.02s @ 50Hz）

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

// === 速度狀態 ===
int prevFX = 0, prevFY = 0;  // 上一次輸出時的 fX/fY（deadband 後穩定值）
bool velInited = false;
float smoothVelX = 0, smoothVelY = 0;
bool velEnabled = true;  // 速度輸出開關

// === LED 閃爍 ===
unsigned long lastBlink = 0;
bool ledState = false;
const int BLINK_INTERVAL = 500;

// === 按鈕 debounce ===
bool buttonReading = HIGH;
bool lastButtonReading = HIGH;
bool buttonState = HIGH;
unsigned long lastDebounceTime = 0;
const unsigned long debounceDelay = 30;

// --------------------------------------------------
// 工具函式
// --------------------------------------------------

void updateBlink() {
  if (millis() - lastBlink > BLINK_INTERVAL) {
    lastBlink = millis();
    ledState = !ledState;
    digitalWrite(STATUS_LED, ledState);
  }
}

void checkButton() {
  buttonReading = digitalRead(BUTTON_PIN);
  if (buttonReading != lastButtonReading) {
    lastDebounceTime = millis();
  }
  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (buttonReading != buttonState) {
      buttonState = buttonReading;
      if (buttonState == LOW) {
        Serial.println("/status button_recalibrate");
        startCalibration();
      }
    }
  }
  lastButtonReading = buttonReading;
}

int cmpInt(const void *a, const void *b) {
  return (*(int *)a) - (*(int *)b);
}

int arrayMedian(int *arr, int n) {
  if (n <= 0) return 0;
  int tmp[256];
  int count = min(n, 256);
  memcpy(tmp, arr, count * sizeof(int));
  qsort(tmp, count, sizeof(int), cmpInt);
  if (count % 2 == 1) return tmp[count / 2];
  return (tmp[count / 2 - 1] + tmp[count / 2]) / 2;
}

// 第一層：Median 濾波器
int medianFilter(int *buf, int &idx, int &fill, int value) {
  buf[idx] = value;
  idx = (idx + 1) % MEDIAN_WINDOW;
  if (fill < MEDIAN_WINDOW) fill++;
  int tmp[MEDIAN_WINDOW];
  memcpy(tmp, buf, fill * sizeof(int));
  qsort(tmp, fill, sizeof(int), cmpInt);
  return tmp[fill / 2];
}

// 第二層 + 第三層：自適應 EMA → Deadband
int applyStableFilter(int medVal, bool &inited, float &ema, int &stableOut) {
  if (medVal == OUT_OF_RANGE) return OUT_OF_RANGE;

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

  if (abs(smooth - stableOut) <= DEAD_BAND_MM) {
    return stableOut;
  } else {
    stableOut = smooth;
    return stableOut;
  }
}

void resetFilters() {
  medIdxX = medIdxY = 0;
  medFillX = medFillY = 0;
  emaInitX = emaInitY = false;
  emaX = emaY = 0;
  stableX = stableY = 0;
  // 速度也重置
  velInited = false;
  smoothVelX = smoothVelY = 0;
  prevFX = prevFY = 0;
}

void startCalibration() {
  currentState = STATE_WARMUP;
  stateStartMs = millis();
  calibCountX = calibCountY = 0;
  offsetX = offsetY = 0;
  resetFilters();
  lastValidX = lastValidY = 0;
  lastRawX = lastRawY = 0;
  Serial.println("/status recalibrating");
}

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
// Serial command handler (WHO + single-char, non-blocking)
// --------------------------------------------------
char cmdBuf[16];
int cmdBufIdx = 0;

void handleSerialCommand() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      if (cmdBufIdx > 0) {
        cmdBuf[cmdBufIdx] = '\0';
        if (strcmp(cmdBuf, "WHO") == 0) {
          Serial.println("ID:" + String(DEVICE_ID));
        } else if (cmdBufIdx == 1) {
          // Single-char commands (backward compatible)
          if (cmdBuf[0] == 'c') {
            startCalibration();
          } else if (cmdBuf[0] == 'r') {
            resetFilters();
            Serial.println("/status filters_reset");
          } else if (cmdBuf[0] == 'v') {
            velEnabled = !velEnabled;
            Serial.print("/status velocity_");
            Serial.println(velEnabled ? "on" : "off");
          }
        }
        cmdBufIdx = 0;
      }
    } else if (cmdBufIdx < 15) {
      cmdBuf[cmdBufIdx++] = c;
    }
  }
}

// --------------------------------------------------
// Setup
// --------------------------------------------------
void setup() {
  Serial.begin(115200);
  delay(500);

  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(STATUS_LED, OUTPUT);

  Wire.begin(I2C_SDA, I2C_SCL);
  Wire.setClock(400000);

  pinMode(XSHUT_1, OUTPUT);
  pinMode(XSHUT_2, OUTPUT);

  digitalWrite(XSHUT_1, LOW);
  digitalWrite(XSHUT_2, LOW);
  delay(10);

  digitalWrite(XSHUT_1, HIGH);
  delay(10);
  if (!lox1.begin(0x29, false, &Wire)) {
    Serial.println("/error sensor1_init_failed");
    while (1) delay(1000);
  }
  lox1.setAddress(ADDR_1);

  digitalWrite(XSHUT_2, HIGH);
  delay(10);
  if (!lox2.begin(0x29, false, &Wire)) {
    Serial.println("/error sensor2_init_failed");
    while (1) delay(1000);
  }
  lox2.setAddress(ADDR_2);

  lox1.setMeasurementTimingBudgetMicroSeconds(TIMING_BUDGET_US);
  lox2.setMeasurementTimingBudgetMicroSeconds(TIMING_BUDGET_US);

  startCalibration();
}

// --------------------------------------------------
// Loop
// --------------------------------------------------
void loop() {
  unsigned long now = millis();

  // === 按鈕 + LED ===
  checkButton();
  if (currentState != STATE_RUNNING) {
    updateBlink();  // 校正中 LED 閃爍
  } else {
    digitalWrite(STATUS_LED, LOW);  // 運行中常滅
  }

  // === Serial 指令 (non-blocking) ===
  handleSerialCommand();

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
    if (validX && calibCountX < 256) {
      calibSamplesX[calibCountX++] = rawX;
    }
    if (validY && calibCountY < 256) {
      calibSamplesY[calibCountY++] = rawY;
    }

    unsigned long elapsed = now - stateStartMs;

    static unsigned long lastCalPrint = 0;
    if (now - lastCalPrint >= 1000) {
      lastCalPrint = now;
      long remainMs = (long)CALIB_MS - (long)elapsed;
      int remainSec = (remainMs > 0) ? (int)((remainMs + 999) / 1000) : 0;
      Serial.print("/status calibrating ");
      Serial.println(remainSec);
    }

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
    int med = medianFilter(medBufX, medIdxX, medFillX, zeroed);
    int filtered = applyStableFilter(med, emaInitX, emaX, stableX);
    if (filtered != OUT_OF_RANGE) {
      lastValidX = filtered;
    }
    lastRawX = zeroed;
  }

  if (validY) {
    int zeroed = max(0, rawY - offsetY);
    int med = medianFilter(medBufY, medIdxY, medFillY, zeroed);
    int filtered = applyStableFilter(med, emaInitY, emaY, stableY);
    if (filtered != OUT_OF_RANGE) {
      lastValidY = filtered;
    }
    lastRawY = zeroed;
  }

  // === 固定頻率輸出 ===
  if (now - lastOutputMs >= OUTPUT_INTERVAL_MS) {
    lastOutputMs = now;

    // ── 速度計算（使用 fX/fY = deadband 後穩定值）──
    // 位置沒變 → 直接 0（速度本來就該是這樣，沒有慣性）
    // 位置有變 → 用 EMA 平滑出 ramp 感
    if (!velInited) {
      prevFX = lastValidX;
      prevFY = lastValidY;
      velInited = true;
    } else {
      if (lastValidX == prevFX) {
        smoothVelX = 0;
      } else {
        float rawVelX = (float)(lastValidX - prevFX) / DT;
        smoothVelX = VEL_SMOOTH * rawVelX + (1.0f - VEL_SMOOTH) * smoothVelX;
      }
      if (lastValidY == prevFY) {
        smoothVelY = 0;
      } else {
        float rawVelY = (float)(lastValidY - prevFY) / DT;
        smoothVelY = VEL_SMOOTH * rawVelY + (1.0f - VEL_SMOOTH) * smoothVelY;
      }

      prevFX = lastValidX;
      prevFY = lastValidY;
    }

    // ── 輸出 ──
    Serial.print("/tof ");
    Serial.print(lastValidX);
    Serial.print(" ");
    Serial.print(lastValidY);
    Serial.print(" ");
    Serial.print(lastRawX);
    Serial.print(" ");
    Serial.print(lastRawY);

    if (velEnabled) {
      Serial.print(" ");
      Serial.print(smoothVelX, 1);  // 1 位小數（mm/s 不需要更高精度）
      Serial.print(" ");
      Serial.print(smoothVelY, 1);
    }

    Serial.println();
  }
}
