# 降噪（stationary spectral gating，噪音樣本取自同一支檔的無聲段）→ 放寬邊界重切 → 統一響度
import json, os, sys, numpy as np, soundfile as sf, noisereduce as nr, pyloudnorm as pyln, librosa, warnings
from scipy.signal import butter, sosfiltfilt
warnings.filterwarnings("ignore")
OUT=os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/Documents/03_Projects_Operations/Active/ITRI_工研院藝術進駐/錄音/20260808_小孩聲音擷取")
D=os.path.expanduser("~/Desktop"); SEGDIR=os.path.dirname(os.path.abspath(__file__))
FILES=["260808_165520","260808_165551","260808_170005","260808_174550"]
KIND={"260808_165520":"念注音與說話","260808_165551":"念注音","260808_170005":"念注音","260808_174550":"幼兒聲"}
FORCE_UNSURE={("260808_174550",115.16),("260808_165520",19.34),("260808_174550",41.46)}
PROP=0.80          # 降噪比例：噪音最多壓 14 dB，不做到全黑
PRE,POST=0.12,0.30 # 邊界外再留的秒數
def classify(s):
    d=s["end"]-s["start"]
    if d<0.3 or s["snr"]<15 or s["voiced"]<0.40 or s["f0"]<225: return None
    if (s["file"],s["start"]) in FORCE_UNSURE or s["file"]=="260808_170005": return "unsure"
    if s["f0"]>=250 and s["lowf0"]<=0.06 and s["lowband"]<=0.12: return "sure"
    if s["lowf0"]<=0.25 and s["lowband"]<=0.35: return "unsure"
    return None
def env_db(x,sr,hop):
    r=librosa.feature.rms(y=x,frame_length=hop*4,hop_length=hop)[0]; return 20*np.log10(r+1e-9)
clips=[]; stats=[]
for name in FILES:
    segs=json.load(open(f"{SEGDIR}/{name}_seg2.json"))
    for s in segs: s["cls"]=classify(s)
    x,sr=sf.read(f"{D}/{name}/{name}_TrMic.WAV",dtype="float32",always_2d=True); total=len(x)/sr
    sos=butter(2,80,"hp",fs=sr,output="sos"); x=sosfiltfilt(sos,x,axis=0).astype("float32")
    # 噪音樣本：離任何有聲段 0.15 秒以上的部分
    quiet=np.ones(len(x),bool)
    for s in segs: quiet[max(0,int((s["start"]-0.15)*sr)):int((s["end"]+0.15)*sr)]=False
    noise=x[quiet]
    den=np.stack([nr.reduce_noise(y=x[:,c],sr=sr,y_noise=noise[:,c],stationary=True,prop_decrease=PROP,
                  n_fft=2048,n_std_thresh_stationary=1.0,freq_mask_smooth_hz=120,time_mask_smooth_ms=25) for c in range(x.shape[1])],axis=1).astype("float32")
    hop=int(0.01*sr); e0=env_db(x.mean(1),sr,hop); e1=env_db(den.mean(1),sr,hop)
    n=min(len(e0),len(e1),len(quiet[::hop])); e0=e0[:n]; e1=e1[:n]; qf=quiet[::hop][:n]; act=np.zeros(n,bool)
    for s in segs:
        if s["cls"]: act[int(s["start"]*sr/hop):int(s["end"]*sr/hop)]=True
    loud=act&(e0>np.percentile(e0[act],60))
    stats.append((name,len(noise)/sr,np.median(e0[qf])-np.median(e1[qf]),np.median(e0[loud])-np.median(e1[loud])))
    floor=np.percentile(e1,20)
    groups=[]
    for i,s in enumerate(segs):
        if not s["cls"]: continue
        if groups and groups[-1]["idx"][-1]==i-1 and groups[-1]["cls"]==s["cls"] and s["start"]-groups[-1]["end"]<0.6:
            g=groups[-1]; g["end"]=s["end"]; g["idx"].append(i); g["f0s"].append(s["f0"])
        else: groups.append(dict(cls=s["cls"],start=s["start"],end=s["end"],idx=[i],f0s=[s["f0"]]))
    for g in groups:
        i0,i1=g["idx"][0],g["idx"][-1]
        lo=(segs[i0-1]["end"]+0.03) if i0>0 else 0.0
        hi=(segs[i1+1]["start"]-0.03) if i1+1<len(segs) else total
        # 沿著包絡把頭尾延伸到聲音真的掉回底噪為止
        a=g["start"]; k=int(a*sr/hop)
        while k>0 and a>max(lo,g["start"]-0.25) and e1[k-1]>floor+6: k-=1; a=k*hop/sr
        b=g["end"]; k=int(b*sr/hop)
        while k<len(e1)-1 and b<min(hi,g["end"]+0.60) and e1[k]>floor+6: k+=1; b=k*hop/sr
        A=max(lo,a-PRE,0.0); B=min(hi,b+POST,total); A=min(A,g["start"]); B=max(B,g["end"])
        clips.append(dict(name=name,cls=g["cls"],start=g["start"],end=g["end"],A=A,B=B,pre=a-A,post=B-b,
                          f0=float(np.median(g["f0s"])),raw=x[int(A*sr):int(B*sr)].copy(),den=den[int(A*sr):int(B*sr)].copy(),
                          cut_by_file_end=(B>=total-0.01), tight=(hi-g["end"]<0.15)))
sr=48000
def fade(c,pre,post):
    fi=int(np.clip(pre,0.015,0.08)*sr); fo=int(np.clip(post,0.08,0.30)*sr); fo=min(fo,len(c)//2); fi=min(fi,len(c)//4)
    c=c.copy(); c[:fi]*=(0.5-0.5*np.cos(np.linspace(0,np.pi,fi)))[:,None]; c[-fo:]*=(0.5+0.5*np.cos(np.linspace(0,np.pi,fo)))[:,None]; return c
meter=pyln.Meter(sr,block_size=0.1)
def lufs(c):
    pad=np.concatenate([c,np.zeros((max(0,int(0.5*sr)-len(c)),c.shape[1]),dtype=c.dtype)])
    return meter.integrated_loudness(pad)
for c in clips:
    c["den"]=fade(c["den"],c["pre"],c["post"]); c["raw"]=fade(c["raw"],c["pre"],c["post"])
    c["L"]=lufs(c["den"]); c["pk"]=20*np.log10(np.abs(c["den"]).max())
head=[-1.0-(c["pk"]-c["L"]) for c in clips]   # 每段在 -1 dBFS 峰值下能到的最大響度
TARGET=float(sys.argv[1]) if len(sys.argv)>1 else -20.0
print("各段在峰值 -1 dBFS 下可達的最大響度：min %.1f  p10 %.1f  median %.1f LUFS"%(min(head),np.percentile(head,10),np.median(head)))
print("目標 %.1f LUFS；到不了目標的段數：%d"%(TARGET,sum(h<TARGET for h in head)))
if "--dry" in sys.argv:
    for n,dur,nred,vchg in stats: print("%s 噪音樣本 %.1f s  底噪降 %.1f dB  人聲響段變化 %.1f dB"%(n,dur,nred,-vchg))
    sys.exit()
for sub in ("確定","待確認"):
    os.makedirs(f"{OUT}/{sub}",exist_ok=True)
    for f in os.listdir(f"{OUT}/{sub}"):
        if f.endswith(".wav"): os.remove(f"{OUT}/{sub}/{f}")
for f in os.listdir(OUT):
    if f.startswith("_試聽_") and f.endswith(".wav"): os.remove(f"{OUT}/{f}")
seq={"sure":0,"unsure":0}; cat={"sure":[],"unsure":[],"sure_raw":[]}; rows=[]
gap=np.zeros((int(0.5*sr),2),dtype="float32")
for c,h in zip(clips,head):
    tgt=min(TARGET,h); g=tgt-c["L"]; out=c["den"]*10**(g/20); rawout=c["raw"]*10**(g/20)
    seq[c["cls"]]+=1; sub="確定" if c["cls"]=="sure" else "待確認"
    fn="%02d_%s_%07.2fs_%.1fs.wav"%(seq[c["cls"]],c["name"][7:],c["start"],len(out)/sr)
    sf.write(f"{OUT}/{sub}/{fn}",out,sr,subtype="PCM_24")
    cat[c["cls"]]+=[out,gap]
    if c["cls"]=="sure": cat["sure_raw"]+=[np.clip(rawout,-1,1),gap]
    note=[]
    if c["cut_by_file_end"]: note.append("錄音到這裡就停了")
    elif c["tight"]: note.append("後面緊接大人，尾巴留不長")
    if h<TARGET: note.append("峰值受限，比目標小 %.1f LU"%(TARGET-h))
    rows.append([sub,fn,c["name"],c["start"],c["end"],len(out)/sr,c["f0"],float(tgt),float(20*np.log10(np.abs(out).max())),float(g),KIND[c["name"]],"；".join(note)])
sf.write(f"{OUT}/_試聽_確定_全部串接.wav",np.concatenate(cat["sure"]),sr,subtype="PCM_24")
sf.write(f"{OUT}/_試聽_待確認_全部串接.wav",np.concatenate(cat["unsure"]),sr,subtype="PCM_24")
sf.write(f"{OUT}/_試聽_確定_全部串接_未降噪對照.wav",np.concatenate(cat["sure_raw"]),sr,subtype="PCM_24")
json.dump(dict(rows=rows,stats=[list(map(lambda v: float(v) if not isinstance(v,str) else v,s)) for s in stats],target=TARGET,prop=PROP),open(f"{SEGDIR}/rows2.json","w"),ensure_ascii=False)
for n,dur,nred,vchg in stats: print("%s 噪音樣本 %.1f s  底噪降 %.1f dB  人聲響段變化 %.1f dB"%(n,dur,nred,-vchg))
print("確定",seq["sure"],"待確認",seq["unsure"])
