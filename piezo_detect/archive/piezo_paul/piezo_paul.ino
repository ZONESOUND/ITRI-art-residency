/*
 * ESP32-C3 SuperMini
 * 4x Piezo Drum + 4x LED
 *
 * Serial output format:
 * <channel> <velocity> <rawPeak>
 * Example:
 * 1 88 3084
 * 3 112 3560
 *
 * Features:
 * 1) Dynamic baseline tracking
 * 2) Relative threshold trigger
 * 3) Consecutive hit debounce
 * 4) IIR filter
 * 5) Non-blocking LED flash
 */

// =========================
// Pin assignment
// =========================
const int NUM_PIEZOS = 4;

// Piezo pins (ADC capable)
const int piezoPins[NUM_PIEZOS] = {4, 3, 0, 1};

// LED pins
const int ledPins[NUM_PIEZOS]   = {6, 5, 10, 7};

// =========================
// Tunable params
// =========================
// 每組 Piezo 的相對門檻
const int THRESHOLD_DELTA[NUM_PIEZOS] = {250, 250, 250, 250};

// 每組 Piezo 的最大峰值，用來映射成 velocity 1~127
const int MAX_READING[NUM_PIEZOS] = {3000, 3000, 3000, 3000};

// 峰值偵測時間
const int SCAN_TIME_MS = 15;

// 冷卻時間（避免一次敲擊連續觸發）
const int COOLDOWN_MS = 120;

// 需要連續幾次超門檻才算有效
const int HITS_REQUIRED = 4;

// baseline 追蹤速度：越大越慢
const int BASELINE_ALPHA_SHIFT = 6;   // baseline += (filtered - baseline) / 64

// IIR filter 強度：越大越平滑，但反應越慢
const int FILTER_SHIFT = 2;           // filtered += (raw - filtered) / 4

// LED 亮多久（非阻塞）
const int LED_ON_MS = 30;

// =========================
// State
// =========================
struct PiezoState {
  int baseline = 0;
  int filtered = 0;
  int hitCount = 0;
  bool inited = false;
};

PiezoState states[NUM_PIEZOS];
unsigned long lastTriggerTime[NUM_PIEZOS] = {0, 0, 0, 0};
unsigned long ledOffTime[NUM_PIEZOS]      = {0, 0, 0, 0};

// =========================
// Setup
// =========================
void setup() {
  Serial.begin(115200);

  // LED pins init
  for (int i = 0; i < NUM_PIEZOS; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }

  // ADC settings
  analogReadResolution(12);       // 12-bit ADC => 0~4095
  analogSetAttenuation(ADC_11db); // 量測範圍較接近 0~3.3V

  // 初始化每組 Piezo baseline
  for (int i = 0; i < NUM_PIEZOS; i++) {
    initPiezo(states[i], piezoPins[i]);
  }

  Serial.println("Ready");
}

// =========================
// Main loop
// =========================
void loop() {
  for (int i = 0; i < NUM_PIEZOS; i++) {
    checkPiezo(i);
  }

  updateLEDs();
}

// =========================
// Init baseline
// =========================
void initPiezo(PiezoState &st, int pin) {
  long sum = 0;
  const int N = 50;

  for (int i = 0; i < N; i++) {
    sum += analogRead(pin);
    delay(2);
  }

  int avg = (int)(sum / N);
  st.baseline = avg;
  st.filtered = avg;
  st.hitCount = 0;
  st.inited = true;
}

// =========================
// Check one piezo
// =========================
void checkPiezo(int index) {
  int pin = piezoPins[index];
  PiezoState &st = states[index];

  int raw = analogRead(pin);

  // 1) IIR filter
  st.filtered += (raw - st.filtered) >> FILTER_SHIFT;

  // 2) slowly update baseline
  st.baseline += (st.filtered - st.baseline) >> BASELINE_ALPHA_SHIFT;

  int diff = st.filtered - st.baseline;

  // 3) consecutive hit debounce
  if (diff > THRESHOLD_DELTA[index]) {
    st.hitCount++;
  } else {
    st.hitCount = 0;
  }

  // 4) trigger when enough hits and cooldown passed
  if (st.hitCount >= HITS_REQUIRED &&
      (millis() - lastTriggerTime[index] > COOLDOWN_MS)) {

    int peakValue = raw;
    unsigned long t0 = millis();

    while (millis() - t0 < SCAN_TIME_MS) {
      int v = analogRead(pin);
      if (v > peakValue) peakValue = v;
      delayMicroseconds(50);
    }

    sendSimpleMessage(index, peakValue);

    lastTriggerTime[index] = millis();
    st.hitCount = 0;
  }
}

// =========================
// Serial output + LED flash
// Format:
// <channel> <velocity> <rawPeak>
// =========================
void sendSimpleMessage(int index, int rawPeak) {
  int effectiveThreshold = states[index].baseline + THRESHOLD_DELTA[index];

  int velocity = map(rawPeak, effectiveThreshold, MAX_READING[index], 1, 127);
  velocity = constrain(velocity, 1, 127);

  int channel = index + 1;

  // 與原本範例相同的 serial 格式
  Serial.print(channel);
  Serial.print(" ");
  Serial.print(velocity);
  Serial.print(" ");
  Serial.println(rawPeak);

  // 對應 LED 亮一下
  digitalWrite(ledPins[index], HIGH);
  ledOffTime[index] = millis() + LED_ON_MS;
}

// =========================
// Non-blocking LED update
// =========================
void updateLEDs() {
  unsigned long now = millis();

  for (int i = 0; i < NUM_PIEZOS; i++) {
    if (ledOffTime[i] > 0 && now >= ledOffTime[i]) {
      digitalWrite(ledPins[i], LOW);
      ledOffTime[i] = 0;
    }
  }
}