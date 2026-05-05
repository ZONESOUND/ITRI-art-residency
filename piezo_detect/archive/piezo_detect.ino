/*
 * ESP32 Single Channel Piezo Streamer
 * 壓電感測器 — 單通道原始波形串流
 *
 * 以 8000Hz 固定取樣率串流壓電感測器的原始 ADC 值，
 * 供 FluCoMa、MuBu、SuperCollider、Max/MSP 等工具
 * 進行即時特徵提取（MFCC、頻譜、onset 偵測等）。
 *
 * ── 硬體接線 ──────────────────────────────────────────────
 *   壓電片 正極（紅）→ GPIO36 (VP, ADC1_CH0)
 *          負極（黑）→ GND
 *   並聯電阻：5.1kΩ 或 1MΩ，接在 GPIO36 與 GND 之間
 *   （提供 DC 偏置路徑，防止 ADC 輸入浮接造成雜訊）
 *   供電：3.3V / GND
 *   注意：GPIO36 (VP) 為輸入專用腳，不可驅動輸出。
 *
 * ── 參數 ──────────────────────────────────────────────────
 *   取樣頻率 : 8000 Hz（SAMPLE_INTERVAL_US = 125 µs）
 *   波特率   : 921600 baud（降低 Serial FIFO 堵塞風險）
 *   ADC 衰減 : ADC_11db（輸入範圍 0–3.3V，12-bit，輸出 0–4095）
 *
 * ── Serial 輸出格式 ───────────────────────────────────────
 *   每個取樣輸出一行整數後換行：
 *   "2048\n"
 *   靜止雜訊值約 100–400，打擊峰值可達接近 4095。
 *
 * ── 電腦端接收（Max/MSP 範例）────────────────────────────
 *   [serial <port> 921600]
 *   → 依序取出整數作為音訊/ML 特徵輸入
 */

const int PIEZO_PIN = 36; // VP 腳位在程式中就是 36

// 採樣頻率設定為 8000Hz (適合大多數機器學習特徵提取)
const int SAMPLE_RATE_HZ = 8000;
const int SAMPLE_INTERVAL_US = 1000000 / SAMPLE_RATE_HZ;

unsigned long nextSampleTime = 0;

void setup() {
  // 設定極高波特率以降低序列埠傳輸延遲
  Serial.begin(921600); 
  
  // 設定 ADC 衰減，讓輸入範圍為 0V - 3.3V
  analogSetAttenuation(ADC_11db);
  
  nextSampleTime = micros();
}

void loop() {
  unsigned long now = micros();

  // 定時採樣確保時間間隔固定 (對 FFT/MFCC 至關重要)
  if (now >= nextSampleTime) {
    int raw = analogRead(PIEZO_PIN);
    
    // 直接輸出數值，供電腦端分析
    Serial.println(raw);

    nextSampleTime += SAMPLE_INTERVAL_US;
    
    // 預防計時溢位或處理延遲
    if (now > nextSampleTime + SAMPLE_INTERVAL_US) {
      nextSampleTime = now + SAMPLE_INTERVAL_US;
    }
  }
}