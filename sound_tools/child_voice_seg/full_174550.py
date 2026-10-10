import json, os, sys, numpy as np, soundfile as sf, noisereduce as nr, pyloudnorm as pyln, warnings
from scipy.signal import butter, sosfiltfilt
from scipy.ndimage import minimum_filter1d, uniform_filter1d
warnings.filterwarnings("ignore")
name="260808_174550"; D=os.path.expanduser("~/Desktop")
OUT=os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/Documents/03_Projects_Operations/Active/ITRI_工研院藝術進駐/錄音/20260808_小孩聲音擷取")
segs=json.load(open(f"{name}_seg2.json"))
x,sr=sf.read(f"{D}/{name}/{name}_TrMic.WAV",dtype="float32",always_2d=True)
x=sosfiltfilt(butter(2,80,"hp",fs=sr,output="sos"),x,axis=0).astype("float32")
quiet=np.ones(len(x),bool)
for s in segs: quiet[max(0,int((s["start"]-0.15)*sr)):int((s["end"]+0.15)*sr)]=False
if os.path.exists("den_full.npy"): den=np.load("den_full.npy")
else:
    den=np.stack([nr.reduce_noise(y=x[:,c],sr=sr,y_noise=x[quiet][:,c],stationary=True,prop_decrease=0.8,n_fft=2048,
        n_std_thresh_stationary=1.0,freq_mask_smooth_hz=120,time_mask_smooth_ms=25) for c in range(2)],axis=1).astype("float32"); np.save("den_full.npy",den)
m=pyln.Meter(sr,block_size=0.1)
def L(a,b): 
    c=den[int(a*sr):int(b*sr)]; c=np.concatenate([c,np.zeros((max(0,24000-len(c)),2),dtype=c.dtype)]); return m.integrated_loudness(c)
kid=[s for s in segs if s["f0"]>=250 and s["voiced"]>=0.4 and s["lowf0"]<=0.06 and s["end"]-s["start"]>=0.3]
adult=[s for s in segs if 0<s["f0"]<225 and s["end"]-s["start"]>=0.5]
kl=np.array([L(s["start"],s["end"]) for s in kid]); al=np.array([L(s["start"],s["end"]) for s in adult])
print("小孩段 %d 個 響度 p10 %.1f median %.1f p90 %.1f LUFS"%(len(kl),*np.percentile(kl,[10,50,90])))
print("大人段 %d 個 響度 p10 %.1f median %.1f p90 %.1f LUFS"%(len(al),*np.percentile(al,[10,50,90])))
pk=np.abs(den).max(1); print("整軌峰值 %.1f dBFS；底噪(安靜段 RMS) %.1f dBFS"%(20*np.log10(pk.max()),20*np.log10(np.sqrt((den[quiet]**2).mean()))))
if len(sys.argv)<2:
    for G in (24,27,30,33):
        over=pk*10**(G/20)>10**(-1/20)
        # 以 50 ms 視窗算有多少時間會被限幅
        w=uniform_filter1d(over.astype(float),int(0.05*sr))>0
        print("增益 +%d dB：小孩中位 %.1f LUFS，超過 -1 dBFS 的時間 %.2f s（%.1f%%），最大需壓 %.1f dB"%(G,np.median(kl)+G,w.sum()/sr,100*w.mean(),20*np.log10(pk.max())+G+1))
    sys.exit()
G=float(sys.argv[1]); ceil=10**(-1/20); y=den*10**(G/20)
need=np.minimum(1.0,ceil/np.maximum(np.abs(y).max(1),1e-9))
la=int(0.005*sr); g=minimum_filter1d(need,size=2*la+1)        # 5 ms 前視
g=uniform_filter1d(g,size=la)                                   # 平滑 attack
rel=np.exp(-1/(0.12*sr)); out=np.empty_like(g); cur=1.0         # 120 ms release
for i in range(len(g)):
    cur=g[i] if g[i]<cur else min(g[i],1-(1-cur)*rel)
    out[i]=cur
y=(y*out[:,None]).astype("float32")
fi=int(0.02*sr); y[:fi]*=np.linspace(0,1,fi)[:,None]; y[-fi:]*=np.linspace(1,0,fi)[:,None]
fn=f"{OUT}/{name}_整軌_降噪增益.wav"; sf.write(fn,y,sr,subtype="PCM_24")
r,_=sf.read(fn); red=20*np.log10(out)
print("寫出",os.path.basename(fn),"%.1f s"%(len(r)/sr),"峰值 %.2f dBFS"%(20*np.log10(np.abs(r).max())),"整軌 %.1f LUFS"%pyln.Meter(sr).integrated_loudness(r))
print("限幅器動作時間（壓超過 0.5 dB）%.2f s，最大壓 %.1f dB"%((red<-0.5).sum()/sr,-red.min()))
# 哪些時間點被壓超過 3 dB
idx=np.where(red<-3)[0]
if len(idx):
    t=idx/sr; grp=[[t[0],t[0]]]
    for v in t[1:]:
        if v-grp[-1][1]>0.3: grp.append([v,v])
        else: grp[-1][1]=v
    print("壓超過 3 dB 的位置：",", ".join("%.1f–%.1f s"%(a,b) for a,b in grp))
