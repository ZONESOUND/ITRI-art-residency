#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_VL53L0X.h>
#include <Adafruit_NeoPixel.h>
#include <limits.h>
#include <math.h>

// =======================================================
// Pins
// =======================================================
const int PIN_HX_SCK   = 3;
const int PIN_HX_DOUT  = 4;

const int PIN_I2C_SDA  = 5;
const int PIN_I2C_SCL  = 6;

const int PIN_MIST_PWM = 7;
const int PIN_LED_RING = 2;

const int PIN_TOF_XSHUT = 10;
const int PIN_CALIB_BUTTON = 9;

// =======================================================
// PWM
// =======================================================
const int PWM_FREQ = 20000;
const int PWM_RES  = 10;
const int MAX_DUTYRAW = (1 << PWM_RES) - 1;

// =======================================================
// HX710B
// =======================================================
const long DEADZONE_RAW = 30000;

const float OUT_MIN_POS = 1.0f;
const float OUT_MAX_POS = 10.0f;
const float OUT_MIN_NEG = -1.0f;
const float OUT_MAX_NEG = -10.0f;

long baseline = 0;
bool baselineReady = false;
long maxBlow = LONG_MIN;
long minInhale = LONG_MAX;

// =======================================================
// Mist
// =======================================================
const float DUTY_BASELINE = 2.0f;   // 靜止：最低維持振動
const float DUTY_MIN_POS  = 3.0f;   // 微弱氣流從 3% 開始
const float OUT_FULL_SCALE = 10.0f;

int lastDutyRaw = 0;

// =======================================================
// TOF
// =======================================================
Adafruit_VL53L0X lox = Adafruit_VL53L0X();
VL53L0X_RangingMeasurementData_t measure;
bool tofReady = false;

// =======================================================
// LED
// =======================================================
const int NUM_LEDS = 12;
Adafruit_NeoPixel pixels(NUM_LEDS, PIN_LED_RING, NEO_GRB + NEO_KHZ800);

// =======================================================
// Button debounce
// =======================================================
bool lastButtonState = HIGH;
unsigned long lastDebounceTime = 0;
const unsigned long debounceDelay = 50;

// =======================================================
// Timing
// =======================================================
unsigned long lastLoopMs = 0;
const unsigned long LOOP_INTERVAL_MS = 50;

// =======================================================
// LED animation
// =======================================================
const float SMOOTH_FACTOR = 0.15f;   // 0~1，越小越平滑
const float DOT_SPEED = 1.0f;        // out=1 時每 loop 移動 1 格
const int MAX_TAIL = 8;              // 最大拖尾長度
const float TAIL_DECAY[] = {1.0f, 0.8f, 0.6f, 0.4f, 0.25f, 0.15f, 0.08f, 0.03f};

float dotPosition = 0.0f;            // 白點位置 0.0~12.0
float smoothTofR = 0.0f, smoothTofG = 50.0f, smoothTofB = 255.0f;
float smoothTofBri = 30.0f;

// =======================================================
// HX710B functions
// =======================================================
long readHX710B(int pinSCK, int pinDOUT) {
  unsigned long t0 = millis();
  while (digitalRead(pinDOUT) == HIGH) {
    if (millis() - t0 > 200) return LONG_MIN;
  }

  long value = 0;
  for (int i = 0; i < 24; i++) {
    digitalWrite(pinSCK, HIGH);
    delayMicroseconds(2);
    value = (value << 1) | digitalRead(pinDOUT);
    digitalWrite(pinSCK, LOW);
    delayMicroseconds(2);
  }

  digitalWrite(pinSCK, HIGH);
  delayMicroseconds(2);
  digitalWrite(pinSCK, LOW);
  delayMicroseconds(2);

  if (value & 0x800000) value |= 0xFF000000;
  return value;
}

float mapFloat(float x, float inMin, float inMax, float outMin, float outMax) {
  if (inMax == inMin) return outMin;
  float t = (x - inMin) / (inMax - inMin);
  t = constrain(t, 0, 1);
  return outMin + t * (outMax - outMin);
}

long calibrateBaseline(int pinSCK, int pinDOUT, int samples, int delayMs) {
  long long sum = 0;
  int ok = 0;

  for (int i = 0; i < samples; i++) {
    long v = readHX710B(pinSCK, pinDOUT);
    if (v != LONG_MIN) {
      sum += v;
      ok++;
    }
    delay(delayMs);
  }

  if (ok == 0) return 0;
  return (long)(sum / ok);
}

float breathMap(long raw, long baseline, long &maxBlow, long &minInhale) {
  long delta = raw - baseline;

  if (labs(delta) <= DEADZONE_RAW) return 0.0f;

  if (delta > 0) {
    if (raw > maxBlow) maxBlow = raw;
    long minPos = baseline + DEADZONE_RAW;
    return mapFloat(raw, minPos, maxBlow, OUT_MIN_POS, OUT_MAX_POS);
  } else {
    if (raw < minInhale) minInhale = raw;
    long maxNeg = baseline - DEADZONE_RAW;
    return mapFloat(raw, maxNeg, minInhale, OUT_MIN_NEG, OUT_MAX_NEG);
  }
}

// =======================================================
// Mist
// =======================================================
int dutyRawFromPercent(float percent) {
  percent = constrain(percent, 0.0f, 100.0f);
  return (int)((percent / 100.0f) * MAX_DUTYRAW);
}

float dutyPercentFromOut(float out) {
  if (out == 0.0f) return DUTY_BASELINE;  // 靜止 → 維持低功率，避免重新起振延遲

  float mag = fabs(out);
  if (mag < 1.0f) return DUTY_MIN_POS;

  // out 1→8 對應 3%→50%，超過 8 繼續往上到 100%
  if (mag <= 8.0f) return mapFloat(mag, 1.0f, 8.0f, DUTY_MIN_POS, 50.0f);
  return mapFloat(mag, 8.0f, OUT_FULL_SCALE, 50.0f, 100.0f);
}

void setMistDuty(int targetDutyRaw) {
  targetDutyRaw = constrain(targetDutyRaw, 0, MAX_DUTYRAW);
  ledcWrite(PIN_MIST_PWM, targetDutyRaw);
  lastDutyRaw = targetDutyRaw;
}

// =======================================================
// LED functions
// =======================================================
void setRingColor(uint8_t r, uint8_t g, uint8_t b, uint8_t brightness = 255) {
  pixels.setBrightness(brightness);
  for (int i = 0; i < NUM_LEDS; i++) {
    pixels.setPixelColor(i, pixels.Color(r, g, b));
  }
  pixels.show();
}

// TOF → 底色 RGB（橘→紫→藍）
void getTofColor(float tof, float &r, float &g, float &b) {
  tof = constrain(tof, 0.0f, 200.0f);
  if (tof <= 100.0f) {
    // 0~100: 橘(255,120,0) → 紫(150,0,200)
    float t = tof / 100.0f;
    r = 255.0f + t * (150.0f - 255.0f);
    g = 120.0f + t * (0.0f - 120.0f);
    b = 0.0f + t * (200.0f - 0.0f);
  } else {
    // 100~200: 紫(150,0,200) → 藍(0,50,255)
    float t = (tof - 100.0f) / 100.0f;
    r = 150.0f + t * (0.0f - 150.0f);
    g = 0.0f + t * (50.0f - 0.0f);
    b = 200.0f + t * (255.0f - 200.0f);
  }
}

// =======================================================
// Calibration
// =======================================================
void runCalibration(int durationMs) {
  setRingColor(255, 255, 255, 255);
  long newBaseline = calibrateBaseline(PIN_HX_SCK, PIN_HX_DOUT, durationMs / 50, 50);
  baseline = newBaseline;
  maxBlow   = baseline + DEADZONE_RAW;
  minInhale = baseline - DEADZONE_RAW;
  setRingColor(40, 40, 40, 40);
}

// =======================================================
// Setup
// =======================================================
void setup() {
  Serial.begin(115200);
  delay(300);
  Serial.println("[setup] start");

  pinMode(PIN_HX_SCK, OUTPUT);
  pinMode(PIN_HX_DOUT, INPUT);
  pinMode(PIN_CALIB_BUTTON, INPUT_PULLUP);

  pixels.begin();
  setRingColor(40, 40, 40, 40);

  Serial.println("[setup] I2C init...");
  Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL);

  Serial.println("[setup] TOF init...");
  tofReady = lox.begin();
  Serial.print("[setup] TOF ready: ");
  Serial.println(tofReady);

  ledcAttach(PIN_MIST_PWM, PWM_FREQ, PWM_RES);

  Serial.println("[setup] calibrating HX710B...");
  baseline = calibrateBaseline(PIN_HX_SCK, PIN_HX_DOUT, 40, 50);
  baselineReady = true;
  Serial.print("[setup] baseline: ");
  Serial.println(baseline);

  maxBlow   = baseline + DEADZONE_RAW;
  minInhale = baseline - DEADZONE_RAW;

  int initDutyRaw = dutyRawFromPercent(DUTY_BASELINE);
  ledcWrite(PIN_MIST_PWM, initDutyRaw);
  lastDutyRaw = initDutyRaw;

  Serial.println("[setup] done");
}

// =======================================================
// Loop
// =======================================================
void loop() {
  unsigned long now = millis();

  // ===== Button debug =====
  static unsigned long lastBtnDebugMs = 0;
  if (now - lastBtnDebugMs >= 1000) {
    lastBtnDebugMs = now;
    Serial.print("[btn] GPIO9 = ");
    Serial.println(digitalRead(PIN_CALIB_BUTTON));
  }
  int reading = digitalRead(PIN_CALIB_BUTTON);
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }
  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading == LOW && lastButtonState == HIGH) {
      Serial.println("[button] pressed → recalibrating...");
      lastButtonState = reading;
      runCalibration(5000);
      Serial.print("[button] new baseline: ");
      Serial.println(baseline);
    } else {
      lastButtonState = reading;
    }
  }

  // ===== Main Loop =====
  if (now - lastLoopMs >= LOOP_INTERVAL_MS) {
    lastLoopMs = now;

    long raw = readHX710B(PIN_HX_SCK, PIN_HX_DOUT);
    float out = 0.0f;
    float dutyPercent = DUTY_BASELINE;
    int dutyRaw = dutyRawFromPercent(DUTY_BASELINE);

    if (raw != LONG_MIN && baselineReady) {
      out = breathMap(raw, baseline, maxBlow, minInhale);
      dutyPercent = dutyPercentFromOut(out);
      dutyRaw = dutyRawFromPercent(dutyPercent);
    }


    setMistDuty(dutyRaw);

    // ===== TOF 測距 =====
    int tofValue = 0;
    if (tofReady) {
      lox.rangingTest(&measure, false);
      if (measure.RangeStatus != 4) tofValue = measure.RangeMilliMeter;
    }

    // ===== LED：底色(TOF色溫) + 旋轉白點(呼吸) =====

    // 底色：TOF → RGB + 亮度，平滑處理
    float targetR, targetG, targetB;
    float targetBri;
    if (tofValue > 0 && tofValue <= 200) {
      getTofColor((float)tofValue, targetR, targetG, targetB);
      targetBri = mapFloat((float)tofValue, 0.0f, 200.0f, 200.0f, 30.0f);
    } else {
      targetR = 0.0f; targetG = 50.0f; targetB = 255.0f; // 冷藍
      targetBri = 30.0f;
    }
    smoothTofR   += (targetR - smoothTofR) * SMOOTH_FACTOR;
    smoothTofG   += (targetG - smoothTofG) * SMOOTH_FACTOR;
    smoothTofB   += (targetB - smoothTofB) * SMOOTH_FACTOR;
    smoothTofBri += (targetBri - smoothTofBri) * SMOOTH_FACTOR;

    // 底色寫入全部 LED
    float briScale = smoothTofBri / 255.0f;
    uint8_t baseR = (uint8_t)(smoothTofR * briScale);
    uint8_t baseG = (uint8_t)(smoothTofG * briScale);
    uint8_t baseB = (uint8_t)(smoothTofB * briScale);

    pixels.setBrightness(255); // 亮度由 RGB 值本身控制
    for (int i = 0; i < NUM_LEDS; i++) {
      pixels.setPixelColor(i, pixels.Color(baseR, baseG, baseB));
    }

    // 旋轉白點：吹氣正轉、吸氣反轉、靜止消失
    // 指數曲線：小力慢轉、大力爆轉 (out^2 / 10 保持方向)
    if (fabs(out) > 0.3f) {
      float sign = (out > 0) ? 1.0f : -1.0f;
      float mag = fabs(out);
      float speed = sign * (mag * mag / 10.0f) * DOT_SPEED;
      dotPosition += speed;
      // wrap 0~12
      dotPosition = fmod(dotPosition, (float)NUM_LEDS);
      if (dotPosition < 0) dotPosition += (float)NUM_LEDS;

      // 畫白點 + 拖尾（吹越大力拖尾越長，最少2顆最多MAX_TAIL顆）
      int tailLen = 2 + (int)(fabs(out) / 10.0f * (MAX_TAIL - 2));
      tailLen = constrain(tailLen, 2, MAX_TAIL);
      for (int t = 0; t < tailLen; t++) {
        int ledIdx;
        if (out > 0) {
          ledIdx = ((int)dotPosition - t + NUM_LEDS) % NUM_LEDS;
        } else {
          ledIdx = ((int)dotPosition + t) % NUM_LEDS;
        }
        float intensity = TAIL_DECAY[t] * smoothTofBri;
        uint8_t white = (uint8_t)constrain(intensity, 0.0f, 255.0f);
        // 疊加白色到底色上
        uint32_t existing = pixels.getPixelColor(ledIdx);
        uint8_t eR = (existing >> 16) & 0xFF;
        uint8_t eG = (existing >> 8) & 0xFF;
        uint8_t eB = existing & 0xFF;
        pixels.setPixelColor(ledIdx, pixels.Color(
          min(255, eR + white),
          min(255, eG + white),
          min(255, eB + white)
        ));
      }
    }
    pixels.show();

    // OSC Output
    Serial.print("/breath ");
    Serial.print(raw == LONG_MIN ? 0 : raw);
    Serial.print(" ");
    Serial.print(out, 2);
    Serial.print(" ");
    Serial.print(dutyPercent, 1);
    Serial.print(" ");
    Serial.print(dutyRaw);
    Serial.print(" ");
    Serial.println(tofValue);
  }

}
