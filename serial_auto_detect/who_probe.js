/*
 * who_probe.js — 單 port 互動式 WHO 探測，給診斷用
 *
 * 用法：
 *   node who_probe.js /dev/tty.usbmodem1423101
 *   node who_probe.js  (列出所有 usbmodem port)
 *
 * 行為：
 *   1. 開 port (115200)，listen 5 秒
 *   2. t=1.5s 送一發 WHO\n
 *   3. t=2.5s 再送一發 WHO\n
 *   4. 把每筆 raw bytes（含時間戳）印出來
 *   5. 結束時印出統計：總 byte 數、是否看到 ID:xxx
 */

const { SerialPort } = require('serialport');

const TARGET = process.argv[2];

async function listPorts() {
  const ports = await SerialPort.list();
  console.log('找到的 USB ports:');
  ports
    .filter(p => /usbmodem|usbserial/i.test(p.path))
    .forEach(p => console.log(`  ${p.path}` + (p.manufacturer ? `  [${p.manufacturer}]` : '')));
  console.log('\n用法: node who_probe.js <path>');
}

async function probe(path) {
  console.log(`\n=== 探測 ${path} ===`);
  console.log(`baud: 115200, 監聽 5 秒，t=1.5s 與 2.5s 送 WHO\\n\n`);

  const t0 = Date.now();
  const ts = () => `[${(Date.now() - t0).toString().padStart(4)}ms]`;

  const port = new SerialPort({ path, baudRate: 115200, autoOpen: false });
  let totalBytes = 0;
  let buffer = '';
  let seenID = null;

  port.open((err) => {
    if (err) {
      console.error(`${ts()} 開啟失敗: ${err.message}`);
      process.exit(1);
    }
    console.log(`${ts()} port opened`);
  });

  port.on('data', (data) => {
    totalBytes += data.length;
    buffer += data.toString('utf8');
    const printable = data.toString('utf8')
      .replace(/\r/g, '\\r')
      .replace(/\n/g, '\\n');
    console.log(`${ts()} RX (${data.length}B): "${printable}"`);

    const m = buffer.match(/ID:(tof|pressure|piezo)\b/i);
    if (m && !seenID) {
      seenID = m[1].toLowerCase();
      console.log(`${ts()} *** 偵測到 ID:${seenID} ***`);
    }
  });

  port.on('error', (err) => {
    console.error(`${ts()} error: ${err.message}`);
  });

  setTimeout(() => {
    console.log(`${ts()} TX: WHO\\n`);
    port.write('WHO\n');
  }, 1500);

  setTimeout(() => {
    console.log(`${ts()} TX: WHO\\n (2nd)`);
    port.write('WHO\n');
  }, 2500);

  setTimeout(() => {
    console.log(`\n--- 結果 ---`);
    console.log(`總共收到: ${totalBytes} bytes`);
    if (seenID) {
      console.log(`ID 偵測: ID:${seenID} ✓`);
    } else if (totalBytes > 0) {
      console.log(`ID 偵測: 沒看到 "ID:..." 字樣`);
      console.log(`診斷: ESP32 在送資料但沒回 WHO → 韌體可能沒 WHO 處理或 handler 有 bug → 需重燒最新版`);
    } else {
      console.log(`ID 偵測: 完全沒收到資料`);
      console.log(`診斷: ESP32 沒在送資料 → 線材 / 供電 / baud rate / 韌體沒在跑`);
    }
    port.close(() => process.exit(0));
  }, 5000);
}

if (!TARGET) {
  listPorts();
} else {
  probe(TARGET);
}
