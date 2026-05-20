/**
 * ToF Visualization — Node for Max version (paired_motion build)
 *
 * Max 接法：
 *   主 patch 內接到 sub_auto_detect 的 TOF 訊號：
 *     [r tof] → [prepend /tof] → [node.script ../visualization/server.js]
 *
 *   ⚠ sub_auto_detect 的 [route /tof] 會把 /tof 前綴剝掉，所以這裡要 prepend 回去；
 *      server.js 的 handler 是註冊在 '/tof'，第一個 atom 必須是 /tof 才會匹配。
 *
 * 瀏覽器開 http://localhost:8080
 * 資料透過 SSE (Server-Sent Events) 推送，零外部依賴。
 */

const maxApi = require('max-api');
const http = require('http');
const fs = require('fs');
const path = require('path');

const HTTP_PORT = 8080;

// ── SSE clients ────────────────────────────────────────────────
let sseClients = [];

function broadcast(data) {
  const payload = `data: ${JSON.stringify(data)}\n\n`;
  sseClients = sseClients.filter((res) => {
    try {
      res.write(payload);
      return true;
    } catch (e) {
      return false; // client disconnected
    }
  });
}

// ── HTTP server ────────────────────────────────────────────────
const server = http.createServer((req, res) => {
  if (req.url === '/events') {
    // SSE endpoint
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*'
    });
    res.write('\n'); // flush headers
    sseClients.push(res);
    maxApi.post(`[SSE] client connected (${sseClients.length} total)`);

    req.on('close', () => {
      sseClients = sseClients.filter((c) => c !== res);
      maxApi.post(`[SSE] client disconnected (${sseClients.length} total)`);
    });
    return;
  }

  // Serve index.html
  const filePath = path.join(__dirname, 'index.html');
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(500);
      res.end('Error loading index.html');
      return;
    }
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(data);
  });
});

server.listen(HTTP_PORT, () => {
  maxApi.post(`[HTTP] http://localhost:${HTTP_PORT}`);
  maxApi.post('Ready! 開瀏覽器即可看到視覺化');
});

// ── Receive data from Max ──────────────────────────────────────
// 訊號形式：fX fY rX rY [vX vY [vXn vYn]]
// 相容三種韌體輸出：
//   tof_c3_supermini          → 4 atoms (fX fY rX rY)
//   tof_c3_supermini_vel      → 6 atoms (... vX vY)
//   tof_c3_supermini_vel_norm → 8 atoms (... vXn vYn)   ← paired_motion 用這版
//
// 兩種 Max 接法都支援：
//   ① [fromsymbol] → [node.script server.js]               （第一個 atom 是 /tof，吃 '/tof' handler）
//   ② [r tof] → [node.script server.js]                    （sub_auto_detect 的 send/receive；裸 list，吃 'list' handler）
//   ③ [r tof] → [prepend /tof] → [node.script server.js]   （手動補回 /tof 前綴，也走 '/tof' handler）
function handleTof(args) {
  broadcast({
    type: 'tof',
    fX: args[0],
    fY: args[1],
    rX: args[2],
    rY: args[3],
    vX: args[4] !== undefined ? args[4] : 0,
    vY: args[5] !== undefined ? args[5] : 0,
    vXn: args[6] !== undefined ? args[6] : 0,
    vYn: args[7] !== undefined ? args[7] : 0
  });
}

maxApi.addHandler('/tof', (...args) => handleTof(args));
maxApi.addHandler('list', (...args) => handleTof(args));

// /status calibrating 4, /status running, etc.
maxApi.addHandler('/status', (...args) => {
  broadcast({ type: 'status', args });
});

// /cal_done offsetX offsetY samplesX samplesY
maxApi.addHandler('/cal_done', (...args) => {
  broadcast({ type: 'cal_done', args });
});
