/*
 * LED Test — ESP32-C3 SuperMini
 * 逐一測試 4 顆 LED，每顆亮 500ms
 * Serial 同步印出哪一顆正在亮
 *
 * LED 1 -> GPIO5
 * LED 2 -> GPIO6
 * LED 3 -> GPIO7
 * LED 4 -> GPIO10
 */

const int NUM_LEDS = 2;
const int ledPins[NUM_LEDS] = {7, 10};  // LED3 (GPIO7), LED4 (GPIO10)

void setup() {
  Serial.begin(115200);

  for (int i = 0; i < NUM_LEDS; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }

  Serial.println("=== LED Test Start ===");
}

void loop() {
  for (int i = 0; i < NUM_LEDS; i++) {
    Serial.print("LED ");
    Serial.print(i + 1);
    Serial.print(" (GPIO");
    Serial.print(ledPins[i]);
    Serial.println(") ON");

    digitalWrite(ledPins[i], HIGH);
    delay(500);
    digitalWrite(ledPins[i], LOW);
    delay(200);
  }

  Serial.println("--- cycle ---");
  delay(1000);
}
