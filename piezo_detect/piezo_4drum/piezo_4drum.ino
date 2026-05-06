/*
 * Piezo 4-Drum — ESP32-C3 SuperMini + 4x Piezo + 4x LED
 *
 * Based on Paul's original working code, with additions:
 *   - WHO identification protocol
 *   - Continuous stream output (/piezo/stream)
 *   - Output format: /piezo <channel> <velocity> <rawPeak>
 *
 * -- Serial Output Format -------------------------------------
 *   Hit event:  /piezo <channel> <velocity> <rawPeak>
 *   Stream:     /piezo/stream d1 d2 d3 d4  (50Hz)
 *   WHO:        Send "WHO\n" -> responds "ID:piezo"
 */

// =========================
// Device ID (for WHO identification)
// =========================
const char* DEVICE_ID = "piezo";

// =========================
// Pin assignment
// =========================
const int NUM_PIEZOS = 4;

const int piezoPins[NUM_PIEZOS] = {4, 3, 0, 1};
const int ledPins[NUM_PIEZOS]   = {6, 5, 10, 7};

// =========================
// Tunable params (same as original)
// =========================
const int THRESHOLD_DELTA[NUM_PIEZOS] = {250, 250, 250, 250};
const int MAX_READING[NUM_PIEZOS]     = {3000, 3000, 3000, 3000};

const int SCAN_TIME_MS = 15;
const int COOLDOWN_MS = 120;
const int HITS_REQUIRED = 4;
const int BASELINE_ALPHA_SHIFT = 6;
const int FILTER_SHIFT = 2;

// LED duration: mapped by hit/touch strength
const int LED_MIN_MS = 30;       // 輕觸最短
const int LED_MAX_MS = 1000;     // 重擊最長
const int LED_ACTIVITY_THRESHOLD = 66; // raw-baseline 超過此值就亮 LED（刮、摸）。從 30 提到 100 抑制環境 spike 引起的誤觸發
const int LED_HITS_REQUIRED = 2; // 連續 N 幀過 threshold 才點 LED。單發 spike 不會點。改成 3 / 4 更嚴

// Stream output interval
const unsigned long STREAM_INTERVAL_MS = 20;  // 50Hz

// =========================
// State (same as original)
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
int ledActHitCount[NUM_PIEZOS]            = {0, 0, 0, 0}; // LED debounce 用：連續過 threshold 的幀數
unsigned long lastStreamTime = 0;

// =========================
// Setup (same as original)
// =========================
void setup() {
  Serial.begin(115200);

  for (int i = 0; i < NUM_PIEZOS; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }

  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);

  for (int i = 0; i < NUM_PIEZOS; i++) {
    initPiezo(states[i], piezoPins[i]);
  }

  Serial.println("Ready");
}

// =========================
// Main loop
// =========================
void loop() {
  handleSerialCommand();

  for (int i = 0; i < NUM_PIEZOS; i++) {
    checkPiezo(i);
  }

  sendStream();
  updateLEDs();
}

// =========================
// Init baseline (same as original)
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
// Check one piezo (same as original — blocking scan)
// =========================
void checkPiezo(int index) {
  int pin = piezoPins[index];
  PiezoState &st = states[index];

  int raw = analogRead(pin);

  st.filtered += (raw - st.filtered) >> FILTER_SHIFT;
  st.baseline += (st.filtered - st.baseline) >> BASELINE_ALPHA_SHIFT;

  // Activity LED: use filtered (IIR smoothed) value, plus consecutive-frame
  // debounce so that single-sample EMI spikes don't fire the LED.
  // Real touches sustain across multiple frames so they trigger normally.
  int actDiff = st.filtered - st.baseline;
  if (actDiff < 0) actDiff = 0;

  if (actDiff > LED_ACTIVITY_THRESHOLD) {
    ledActHitCount[index]++;
  } else {
    ledActHitCount[index] = 0;
  }

  if (ledActHitCount[index] >= LED_HITS_REQUIRED) {
    int tailMs = map(actDiff, LED_ACTIVITY_THRESHOLD, MAX_READING[index], LED_MIN_MS, LED_MAX_MS);
    tailMs = constrain(tailMs, LED_MIN_MS, LED_MAX_MS);
    digitalWrite(ledPins[index], HIGH);
    ledOffTime[index] = millis() + tailMs;
  }

  int diff = st.filtered - st.baseline;

  if (diff > THRESHOLD_DELTA[index]) {
    st.hitCount++;
  } else {
    st.hitCount = 0;
  }

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
// LED logic is IDENTICAL to original (LED after serial print)
// =========================
void sendSimpleMessage(int index, int rawPeak) {
  int effectiveThreshold = states[index].baseline + THRESHOLD_DELTA[index];

  int velocity = map(rawPeak, effectiveThreshold, MAX_READING[index], 1, 127);
  velocity = constrain(velocity, 1, 127);

  int channel = index + 1;

  // Serial output (format changed to /piezo prefix)
  Serial.print("/piezo ");
  Serial.print(channel);
  Serial.print(" ");
  Serial.print(velocity);
  Serial.print(" ");
  Serial.println(rawPeak);

  // LED ON with variable duration (stronger hit = longer fade)
  int ledMs = map(rawPeak, effectiveThreshold, MAX_READING[index], LED_MIN_MS, LED_MAX_MS);
  ledMs = constrain(ledMs, LED_MIN_MS, LED_MAX_MS);
  digitalWrite(ledPins[index], HIGH);
  ledOffTime[index] = millis() + ledMs;
}

// =========================
// Non-blocking LED update (same as original)
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

// =========================
// Continuous stream output (NEW — 50Hz)
// =========================
void sendStream() {
  unsigned long now = millis();
  if (now - lastStreamTime < STREAM_INTERVAL_MS) return;
  lastStreamTime = now;

  if (Serial.availableForWrite() < 40) return;

  Serial.print("/piezo/stream");
  for (int i = 0; i < NUM_PIEZOS; i++) {
    int diff = states[i].filtered - states[i].baseline;
    if (diff < 0) diff = 0;
    Serial.print(" ");
    Serial.print(diff);
  }
  Serial.println();
}

// =========================
// WHO protocol handler (NEW)
// =========================
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
        }
        cmdBufIdx = 0;
      }
    } else if (cmdBufIdx < 15) {
      cmdBuf[cmdBufIdx++] = c;
    }
  }
}
