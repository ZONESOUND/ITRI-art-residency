"""soundtools 指令列。每個子命令的參數用 --help 看。"""
import argparse
import json
import os
import sys

import numpy as np

from . import io, varispeed as vs, tape, collage, analysis


def _out(args, default):
    return args.out or default


def cmd_drift(a):
    x, sr = io.load(a.input, mono=True)
    x = io.fade(x, sr, 0.012, 0.012)
    r = vs.drift_ensemble(x, sr, a.dur, voices=a.voices, sigma=a.sigma, theta=a.theta, max_dev=a.max_dev,
                          coupling=a.coupling, t_sync=a.sync, tau=a.tau, seed=a.seed,
                          rate_base=[a.rate] * a.voices if a.rate != 1.0 else None)
    base = os.path.splitext(a.input)[0]
    if a.stems:
        for i, v in enumerate(r["voices"]):
            io.write(f"{_out(a, base)}_drift_v{i+1}.wav", v, sr, peak_db=-1)
    pans = np.linspace(-0.8, 0.8, a.voices) if a.voices > 1 else [0.0]
    mix = vs.pan_mix(r["voices"], pans, sr)
    p = io.write(f"{_out(a, base)}_drift_mix.wav", mix, sr, peak_db=-1)
    rs = r["reset_sample"]
    print("wrote", p)
    if rs is not None and rs < len(r["pos"][0]):
        print(f"sync {a.sync}s, hard align at {rs/sr:.2f}s; lag before {vs.lag_ms(r['pos'], sr, rs/sr-0.1)} after {vs.lag_ms(r['pos'], sr, rs/sr+1)} ms")
    else:
        print("lag at end (ms):", vs.lag_ms(r["pos"], sr, a.dur - 0.5))


def cmd_tape(a):
    x, sr = io.load(a.input)
    y = tape.tape(x, sr, a.wow, a.wow_theta, a.flutter_hz, a.flutter_cents, a.drive, a.head, a.seed)
    if a.echo:
        y = tape.echo(y, sr, a.echo, fb=0.45, mix=0.6)
    if a.reverb:
        y = tape.reverb(y, sr, rt60=a.reverb, mix=0.3)
    p = io.write(_out(a, os.path.splitext(a.input)[0] + "_tape.wav"), y, sr, peak_db=-1)
    print("wrote", p)


def cmd_stretch(a):
    x, sr = io.load(a.input)
    y = collage.paulstretch(x, a.factor, a.win, a.seed)
    if a.lowpass:
        y = tape.lowpass(y, sr, a.lowpass)
    p = io.write(_out(a, os.path.splitext(a.input)[0] + f"_x{a.factor:g}.wav"), y, sr, peak_db=-1)
    print("wrote", p, f"{len(y)/sr:.1f}s")


def cmd_phrases(a):
    x, sr = io.load(a.input, sr=22050, mono=True)
    pats = [tuple(int(v) for v in grp.split(",")) for grp in a.intervals.split(";")]
    ph, nl, hits = analysis.phrases_by_motif(x, sr, pats, lead_s=a.lead, min_gap=a.min_gap)
    print(f"{len(nl)} notes, motif hits at:", [f"{t:.2f}s {analysis.NOTE[m % 12]}{m // 12 - 1}" for t, m in hits])
    for s, e in ph:
        print(f"  phrase {s:7.2f} – {e:7.2f}  ({e - s:.2f}s)")
    if a.notes:
        for s, e, m in nl:
            print(f"    {s:6.2f}-{e:6.2f} {analysis.NOTE[m % 12]}{m // 12 - 1}")
    if a.cut:
        full, sr0 = io.load(a.input)
        base = os.path.splitext(a.input)[0]
        for i, (s, e) in enumerate(ph):
            seg = io.fade(full[int(s * sr0):int(e * sr0)], sr0, 0.012, 0.012)
            io.write(f"{base}_phrase{i+1:02d}_{s:.2f}-{e:.2f}s.wav", seg, sr0)
        print("cut", len(ph), "files")


def cmd_syllables(a):
    x, sr = io.load(a.input, sr=22050, mono=True)
    expected = [int(v) for v in a.expected.split(",")] if a.expected else None
    r = analysis.syllables(x, sr, expected=expected, with_phones=a.phones)
    for s in r["segments"]:
        flag = "" if "ok" not in s else ("  OK" if s["ok"] else f"  MISMATCH expected {s['expected']}")
        print(f"seg {s['idx']:2d} {s['start']:6.2f}-{s['end']:6.2f}  peaks {s['n_peaks']}{flag}  {' '.join(s['phones'])}")
    if a.json:
        json.dump(r["segments"], open(a.json, "w"), ensure_ascii=False, indent=1)
        print("wrote", a.json)


def cmd_stems(a):
    rows = analysis.match_stems(a.stems, a.sources)
    for r in rows:
        extra = "  pieces " + str(r["pieces"]) if r["pieces"] else ""
        print(f"{r['stem']:30s} {r['start']:8.2f}-{r['end']:8.2f}  ← {r['source']} @ {r['src_start']:.2f}s  ncc {r['ncc']:.2f}{extra}")
    if a.json:
        json.dump(rows, open(a.json, "w"), ensure_ascii=False, indent=1)


def main(argv=None):
    p = argparse.ArgumentParser(prog="soundtools", description="離線聲音工具：漂移、磁帶、拉伸、樂句、音節、stems")
    sp = p.add_subparsers(dest="cmd", required=True)

    d = sp.add_parser("drift", help="一段 loop 做多聲部 varispeed 漂移（可耦合、回歸、硬對齊）")
    d.add_argument("input"); d.add_argument("--dur", type=float, default=100)
    d.add_argument("--voices", type=int, default=5); d.add_argument("--sigma", type=float, default=7.0)
    d.add_argument("--theta", type=float, default=0.03); d.add_argument("--max-dev", type=float, default=16.0)
    d.add_argument("--coupling", type=float, default=0.0); d.add_argument("--sync", type=float, default=None, help="幾秒觸發回歸")
    d.add_argument("--tau", type=float, default=2.5); d.add_argument("--rate", type=float, default=1.0)
    d.add_argument("--seed", type=int, default=1); d.add_argument("--stems", action="store_true", help="各聲部另存單軌")
    d.add_argument("--out"); d.set_defaults(fn=cmd_drift)

    t = sp.add_parser("tape", help="磁帶鏈：wow flutter、飽和、磁頭衰減，可加 echo 與殘響")
    t.add_argument("input"); t.add_argument("--wow", type=float, default=10); t.add_argument("--wow-theta", type=float, default=0.4)
    t.add_argument("--flutter-hz", type=float, default=7); t.add_argument("--flutter-cents", type=float, default=1.5)
    t.add_argument("--drive", type=float, default=1.4); t.add_argument("--head", type=float, default=8000)
    t.add_argument("--echo", type=float, default=0, help="delay 秒數，0 關"); t.add_argument("--reverb", type=float, default=0, help="rt60 秒，0 關")
    t.add_argument("--seed", type=int, default=0); t.add_argument("--out"); t.set_defaults(fn=cmd_tape)

    s = sp.add_parser("stretch", help="paulstretch 極慢拉伸")
    s.add_argument("input"); s.add_argument("--factor", type=float, default=8); s.add_argument("--win", type=int, default=16384)
    s.add_argument("--lowpass", type=float, default=0); s.add_argument("--seed", type=int, default=0); s.add_argument("--out"); s.set_defaults(fn=cmd_stretch)

    ph = sp.add_parser("phrases", help="旋律型態找樂句邊界（預設小星星兩種句頭）")
    ph.add_argument("input"); ph.add_argument("--intervals", default="0,7,9,7;0,-2,-3,-5", help="音程型態，多個用分號隔開")
    ph.add_argument("--min-gap", type=float, default=8.0, help="句首之間最短秒數，更近的命中視為半句"); ph.add_argument("--lead", type=float, default=0.05)
    ph.add_argument("--notes", action="store_true"); ph.add_argument("--cut", action="store_true", help="切出各句存檔"); ph.set_defaults(fn=cmd_phrases)

    sy = sp.add_parser("syllables", help="語音音節：停頓段、能量峰數、可選音素辨識")
    sy.add_argument("input"); sy.add_argument("--expected", help="每段預期音節數，逗號分隔")
    sy.add_argument("--phones", action="store_true", help="跑 allosaurus"); sy.add_argument("--json"); sy.set_defaults(fn=cmd_syllables)

    st = sp.add_parser("stems", help="DAW 匯出的 stems 回對原始素材")
    st.add_argument("--stems", nargs="+", required=True); st.add_argument("--sources", nargs="+", required=True)
    st.add_argument("--json"); st.set_defaults(fn=cmd_stems)

    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
