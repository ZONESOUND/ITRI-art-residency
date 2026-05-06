/*
 * bootstrap.js — paired_motion 演出 patch 的進入點
 *
 * 工作流程：
 *   1. 檢查 node_modules/serialport 是否存在
 *   2. 不存在 → 跑 npm install，等完成（首次執行可能 30~60 秒）
 *   3. 存在或裝完後 → require('./auto_detect.js') 載入主邏輯
 *
 * 為什麼需要這個 wrapper：
 *   auto_detect.js 一進入就 require('serialport')，如果第一次執行的人還沒
 *   裝過依賴，會直接 throw "Cannot find module 'serialport'"。bootstrap 負責
 *   先把依賴準備好再載入主邏輯，user 從頭到尾不用開 Terminal。
 *
 * 本身不依賴任何 npm 套件 — 只用 Node 內建 (fs / path / child_process)
 * 跟 Node-for-Max 內建的 max-api。所以無論 node_modules 狀態如何都能跑。
 *
 * Max 端使用：
 *   [node.script bootstrap.js @autostart 1]
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const Max = require('max-api');

const NODE_MODULES = path.join(__dirname, 'node_modules');
const KEY_DEP = path.join(NODE_MODULES, 'serialport');

function depsReady() {
  return fs.existsSync(KEY_DEP);
}

function runNpmInstall() {
  return new Promise((resolve, reject) => {
    Max.post('paired_motion: 首次執行，正在安裝依賴...');
    Max.post('paired_motion: 過程約 30~60 秒，請稍候，請勿關閉 patch');

    const child = exec('npm install', { cwd: __dirname, maxBuffer: 10 * 1024 * 1024 });

    child.stdout && child.stdout.on('data', (data) => {
      // 把 npm 輸出拋到 Max console（每行一筆，方便追蹤進度）
      data.toString().split('\n').forEach(line => {
        if (line.trim()) Max.post(`  npm: ${line.trim()}`);
      });
    });

    child.stderr && child.stderr.on('data', (data) => {
      data.toString().split('\n').forEach(line => {
        if (line.trim()) Max.post(`  npm[err]: ${line.trim()}`);
      });
    });

    child.on('close', (code) => {
      if (code === 0) {
        Max.post('paired_motion: 依賴安裝完成');
        resolve();
      } else {
        const msg = `npm install 失敗 (exit code ${code})`;
        Max.post(`paired_motion: ${msg}`);
        reject(new Error(msg));
      }
    });
  });
}

async function main() {
  try {
    if (depsReady()) {
      Max.post('paired_motion: 依賴已就緒');
    } else {
      await runNpmInstall();
    }

    Max.post('paired_motion: 載入 auto_detect.js...');
    require('./auto_detect.js');
  } catch (err) {
    Max.post(`paired_motion: bootstrap 失敗: ${err.message}`);
    Max.outlet('error', err.message);
  }
}

main();
