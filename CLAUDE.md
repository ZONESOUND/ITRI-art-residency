# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Code for the ITRI art-residency project「節奏繞纏 / Rhythmic Entanglements」. The artwork instruments「同動車」(an ITRI stroke-rehabilitation device using a well-hand-leads-affected-hand bimanual mechanism) with three sensors and maps user interaction into real-time Max/MSP sound synthesis.

The three sensors all share one USB hub, all run on **ESP32-C3 SuperMini @ 115200 baud**, and all implement the WHO identification protocol:

| Sensor | Folder | WHO ID | Signal |
|---|---|---|---|
| Pressure (FSR ×2 + WS2812 ring) | `pressure_sensor/` | `pressure` | grip force, 0.0–1.0 per hand |
| ToF (VL53L0X ×2) | `tof_distance_sensor/` | `tof` | handle X/Y position + normalized velocity −1..1 |
| Piezo (×4, "4-drum") | `piezo_detect/` | `piezo` | strike events (vel 1–127) + continuous activity stream |

**The performance master patch is `paired_motion/`** — a self-contained Max Project meant to be zipped and run on any Mac. The other top-level folders are firmware sources, supporting tools, and phased/experimental modules that are not necessarily integrated into the performance build.

## Architecture (the big picture)

Data flow for the performance build:

```
3× ESP32-C3 → USB hub → Mac
  paired_motion/patchers/main.maxpat
    └ [bpatcher sub_auto_detect.maxpat]
         ├ [node.script ../code/auto_detect.js]   ← scans USB ports, WHO handshake
         ├ [serial a/b/c 115200 8 1] ×3           ← driven by a [metro 20] bang (50Hz)
         └ outlets: /tof  /pressure  /piezo  /piezo/stream
    └ [bpatcher sub_tof / sub_pressure / sub_piezo]  ← per-sensor signal→sound mapping
    └ mix + dac~ → speakers
```

Key structural conventions:
- **One `sub_*.maxpat` abstraction per sensor.** Each unpacks its list, normalizes/maps, and outputs clean signals. `main.maxpat` only does wiring, mixing, and output. Sensor list formats and intended outlet layouts are documented in detail in `paired_motion/README.md` — read that before editing any `sub_*` patch.
- **Firmware already normalizes** where it matters: ToF `vXn/vYn` are −1..1 (snap-to-0 at rest), Pressure `norm1/norm2` are 0–1 (auto-calibrating, idles to 0). Max-side does **not** re-normalize these. Changing the normalize ceiling means reflashing firmware (e.g. `VEL_MAX` in `tof_c3_supermini_vel_norm`).
- **WHO protocol** solves unstable USB port enumeration: host sends `WHO\n`, ESP32 replies `ID:tof|pressure|piezo`, matched via `/ID:(tof|pressure|piezo)\b/i`. `serial_auto_detect/README.md` is the authoritative reference for the protocol, the ESP32-C3 USB-CDC boot-reset timing (`BOOT_WAIT_MS=1200`, retries every 400ms), and the Max `[serial]` gotchas.
- **`paired_motion/code/auto_detect.js` is a manually-maintained frozen copy** of `serial_auto_detect/auto_detect.js`. They are independent files; the performance build runs its own copy. Sync only via an explicit `cp` when promoting a verified change, then commit + tag. This is a deliberate safety net, not a bug — do not "fix" the duplication by symlinking or auto-syncing.

## Common tasks

**Run the performance patch:** open `paired_motion/paired_motion.maxproj` in Max/MSP 9, double-click `patchers/main.maxpat`. First run (no `node_modules/`): click the "npm install" button in the patch, then send `script restart` to `[node.script]`. `node.script` deliberately has **no `@autostart`** (it crashes at Max clone time) — start it manually with `script start`.

**npm install** is per Node folder (each has its own `package.json`): `paired_motion/code/` and `serial_auto_detect/` depend on `serialport@^12` (needs Node 16+); the `visualization/` folders have zero runtime deps (SSE, no install needed).

**Diagnose a serial/auto-detect problem:** fully quit Max (Cmd+Q) to free ports first, then `cd serial_auto_detect && node who_probe.js [/dev/tty.usbmodemXXXX]`. The full triage flow (firmware-old vs Max-side vs hardware) is in `serial_auto_detect/README.md`.

**ToF trajectory visualization:** open `paired_motion/patchers/main_viz.maxpat` (a copy of `main.maxpat` with a viz block) or add `sub_visualization.maxpat`, then `script start` the `[node.script server.js]` (port 8080, SSE → browser at http://localhost:8080). `main.maxpat` itself is never modified for viz. See `paired_motion/visualization/README.md`.

**Arduino firmware:** Board = `ESP32C3 Dev Module`, **USB CDC On Boot = Enabled** (required for all three — otherwise Serial uses the wrong channel). Libraries: `Adafruit_VL53L0X`, `Adafruit_NeoPixel`. The flashed firmware per device and the stable port-suffix→device mapping are tabulated in `paired_motion/README.md` and `serial_auto_detect/README.md`. The WHO handler lives in each `.ino`'s `handleSerialCommand()`.

## Performance version control

Rehearsal / stage / exhibition can each be a distinct version. Tag with a context prefix + date (keep it simple — no venue name), paired with a `presets/*.maxsnap` snapshot:
```
git tag 排練-YYYYMMDD   # rehearsal
git tag 演出-YYYYMMDD   # stage performance
git tag 展覽-YYYYMMDD   # exhibition / booth
git push origin --tags
```
Restore any past version with `git checkout <tag>`.

(The older `演出_YYYYMMDD_場地名` scheme in `paired_motion/README.md` is superseded by this simpler form.)

## Other modules (not in the performance build)

`breath_sensor/` (HX710B breath instrument), `duo_pulse_sonification/` (two-person pulse → p5.js Lissajous + Web Serial, plus a `ws_osc_relay/` WS→OSC bridge), `piezo_detect_fft/` (piezo FFT hit/scrub), `local_mediapipe/` (local hand tracking for the LA "Life in Motion" show), `remote_hand_tracking/` (hand data over WebSocket), `legacy_local_cv_engine/` (superseded Python OpenCV motion engine). Each has its own README with details. `arduino_template.maxpat` is a generic sensor-agnostic Arduino-over-Serial receiver to start new patches from.
