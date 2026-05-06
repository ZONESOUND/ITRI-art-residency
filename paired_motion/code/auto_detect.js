/*
 * auto_detect.js — ESP32 多裝置 Serial Port 自動辨識
 *
 * 為三顆 ESP32 裝置設計：
 *   - tof_c3_supermini_vel  (115200 baud, "ID:tof")
 *   - pressure_2hands       (115200 baud, "ID:pressure")
 *   - piezo_4drum           (115200 baud, "ID:piezo")
 *
 * 三顆 baud rate 一致，掃描只需要試 115200。
 *
 * ── 工作原理 ─────────────────────────────────────────
 *   1. 列出所有 serial 裝置，過濾 usbmodem / usbserial
 *   2. 對每個 port 開 115200，送 "WHO\n"，等回應 "ID:xxx"
 *   3. 識別出 tof / pressure / piezo 後關掉 port
 *   4. 透過 outlet 把 port 名（短名，去掉 /dev/tty.）送給 Max
 *
 * ── Max 端 outlet ───────────────────────────────────
 *   "tof"      <port_name>     如 "usbmodem1423101"
 *   "pressure" <port_name>
 *   "piezo"    <port_name>
 *   "missing"  <id>            某 ID 沒掃到（"tof" / "pressure" / "piezo"）
 *   "done"                     掃描結束（不論成功或部分失敗都會發）
 *   "error"    <msg>           發生例外
 *
 * ── Max 端 input ────────────────────────────────────
 *   "scan"  → 重新掃描
 *   bang    → 重新掃描
 *
 * ── 安裝依賴 ────────────────────────────────────────
 *   在此資料夾執行：
 *     nvm use 20  (或 16+)
 *     npm install
 */

const { SerialPort } = require('serialport');
const Max = require('max-api');

// ESP32-C3 USB CDC 在 port 開啟瞬間會被 DTR 訊號重置，
// 從 reset 到 Serial 真正能接收指令大約要 1~1.5 秒。
// 所以開 port 後先等 BOOT_WAIT_MS，再送第一發 WHO，
// 之後每 RETRY_INTERVAL_MS 重送一次，總共等到 SCAN_TIMEOUT_MS。
const BOOT_WAIT_MS = 1200;
const RETRY_INTERVAL_MS = 400;
const SCAN_TIMEOUT_MS = 3000;
const POST_CLOSE_DELAY_MS = 250;
const KNOWN_IDS = ['tof', 'pressure', 'piezo'];
const PORT_PATTERN = /usbmodem|usbserial|wchusbserial|SLAB_USB|UART/i;

function probePort(path, baudRate = 115200) {
  return new Promise((resolve) => {
    let resolved = false;
    let buffer = '';
    let port;
    let retryTimer = null;

    const finish = (result) => {
      if (resolved) return;
      resolved = true;
      if (retryTimer) clearInterval(retryTimer);
      try {
        if (port && port.isOpen) {
          port.close(() => resolve({ id: result, buffer }));
        } else {
          resolve({ id: result, buffer });
        }
      } catch (e) {
        resolve({ id: result, buffer });
      }
    };

    try {
      port = new SerialPort({ path, baudRate, autoOpen: false });
    } catch (e) {
      return resolve({ id: null, buffer: '' });
    }

    port.on('error', () => finish(null));

    port.open((err) => {
      if (err) return finish(null);

      port.on('data', (data) => {
        buffer += data.toString('utf8');
        // 只接受白名單內的 ID
        const match = buffer.match(/ID:(tof|pressure|piezo)\b/i);
        if (match) finish(match[1].toLowerCase());
      });

      const sendWho = () => {
        try { port.write('WHO\n'); } catch (e) {}
      };

      // 等 boot reset 過後送第一發
      setTimeout(sendWho, BOOT_WAIT_MS);

      // 每 RETRY_INTERVAL_MS 再重送（從 BOOT_WAIT_MS 之後開始）
      setTimeout(() => {
        retryTimer = setInterval(sendWho, RETRY_INTERVAL_MS);
      }, BOOT_WAIT_MS + 100);

      setTimeout(() => finish(null), SCAN_TIMEOUT_MS);
    });
  });
}

async function scanAll() {
  Max.post('--- 開始掃描 serial ports ---');

  let allPorts;
  try {
    allPorts = await SerialPort.list();
  } catch (e) {
    Max.post(`SerialPort.list() 失敗: ${e.message}`);
    Max.outlet('error', e.message);
    return;
  }

  const candidates = allPorts.filter(p => PORT_PATTERN.test(p.path));

  Max.post(`找到 ${candidates.length} 個候選 port`);
  candidates.forEach(p => Max.post(`  ${p.path}`));

  if (candidates.length === 0) {
    Max.post('沒有找到 USB 裝置，請檢查線材是否插好');
    KNOWN_IDS.forEach(id => Max.outlet('missing', id));
    Max.outlet('done');
    return;
  }

  const results = {};

  for (const p of candidates) {
    Max.post(`探測 ${p.path}...`);
    const { id, buffer } = await probePort(p.path);
    if (id && KNOWN_IDS.includes(id)) {
      Max.post(`  ✓ ${p.path} → ID:${id}`);
      results[id] = p.path;
    } else {
      Max.post(`  ✗ ${p.path} → 無 ID 匹配`);
      if (buffer && buffer.length > 0) {
        // 顯示 ESP32 實際吐了什麼，方便 debug
        const preview = buffer
          .slice(0, 200)
          .replace(/\r/g, '\\r')
          .replace(/\n/g, '\\n');
        Max.post(`     收到 ${buffer.length} bytes: "${preview}${buffer.length > 200 ? '...' : ''}"`);
      } else {
        Max.post(`     buffer 是空的（ESP32 沒在吐資料 — 檢查 baud rate / 線路 / 韌體）`);
      }
    }
    // 給 OS 一點時間徹底釋放 port
    await new Promise(r => setTimeout(r, 200));
  }

  // 等 port 完全釋放，給 [serial] 物件 reopen 用
  await new Promise(r => setTimeout(r, POST_CLOSE_DELAY_MS));

  Max.post('--- 掃描結果 ---');
  for (const id of KNOWN_IDS) {
    if (results[id]) {
      // Max [serial] 物件吃 port 名稱不帶 /dev/tty. 或 /dev/cu. 前綴
      const maxPortName = results[id].replace(/^\/dev\/(tty|cu)\./, '');
      Max.post(`  ${id}: ${results[id]} → ${maxPortName}`);
      Max.outlet(id, maxPortName);
    } else {
      Max.post(`  ${id}: 未找到`);
      Max.outlet('missing', id);
    }
  }

  Max.outlet('done');
}

Max.addHandler('scan', () => {
  scanAll().catch(e => {
    Max.post(`Scan error: ${e.message}`);
    Max.outlet('error', e.message);
  });
});

Max.addHandler('bang', () => {
  scanAll().catch(e => {
    Max.post(`Scan error: ${e.message}`);
    Max.outlet('error', e.message);
  });
});

// Auto-run on load
scanAll().catch(e => {
  Max.post(`Initial scan error: ${e.message}`);
  Max.outlet('error', e.message);
});
