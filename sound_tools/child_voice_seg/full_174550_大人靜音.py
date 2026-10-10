# 整軌降噪＋增益，大人說話的段落靜音（用 seg2 的分段結果判斷）
import json, os, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy.ndimage import minimum_filter1d, uniform_filter1d
name="260808_174550"; G=30.0; sr=48000
OUT=os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/Documents/03_Projects_Operations/Active/ITRI_工研院藝術進駐/錄音/20260808_小孩聲音擷取")
segs=json.load(open(f"{name}_seg2.json")); den=np.load("den_full.npy"); total=len(den)/sr
def adult(s):
    if 0<s["f0"]<225: return "大人音高"
    if s["lowf0"]>=0.25: return "大人音高的幀多"
    if s["lowband"]>=0.30: return "低頻帶有能量"
    if s["voiced"]<0.2 and s["txt"].strip(): return "轉錄有字、幾乎無音高"
    return None
for s in segs: s["why"]=adult(s)
# 相鄰的大人段（中間沒有保留段、間隔 < 1.5 s）連成一塊
blocks=[]
for i,s in enumerate(segs):
    if not s["why"]: continue
    if blocks and blocks[-1]["last"]==i-1 and s["start"]-blocks[-1]["end"]<1.5: blocks[-1]["end"]=s["end"]; blocks[-1]["last"]=i; blocks[-1]["why"].add(s["why"])
    else: blocks.append(dict(start=s["start"],end=s["end"],first=i,last=i,why={s["why"]}))
gain=np.ones(len(den),dtype="float32"); F=int(0.08*sr)
for b in blocks:
    lo=segs[b["first"]-1]["end"]+0.05 if b["first"]>0 else 0.0
    hi=segs[b["last"]+1]["start"]-0.05 if b["last"]+1<len(segs) else total
    a=max(lo,b["start"]-0.20,0.0); e=min(hi,b["end"]+0.30,total); a=min(a,b["start"]); e=max(e,b["end"])
    b["a"],b["e"]=a,e; ia,ie=int(a*sr),int(e*sr)
    gain[ia:ie]=0
    # 淡出、淡入放在靜音區外側，不吃到保留的聲音以外的範圍
    f0=max(0,ia-F); gain[f0:ia]=np.minimum(gain[f0:ia],0.5+0.5*np.cos(np.linspace(0,np.pi,ia-f0)))
    f1=min(len(den),ie+F); gain[ie:f1]=np.minimum(gain[ie:f1],0.5-0.5*np.cos(np.linspace(0,np.pi,f1-ie)))
y=den*gain[:,None]*10**(G/20); ceil=10**(-1/20)
need=np.minimum(1.0,ceil/np.maximum(np.abs(y).max(1),1e-9)); la=int(0.005*sr)
g=uniform_filter1d(minimum_filter1d(need,size=2*la+1),size=la); rel=np.exp(-1/(0.12*sr)); out=np.empty_like(g); cur=1.0
for i in range(len(g)):
    cur=g[i] if g[i]<cur else min(g[i],1-(1-cur)*rel); out[i]=cur
y=(y*out[:,None]).astype("float32"); fi=int(0.02*sr); y[:fi]*=np.linspace(0,1,fi)[:,None]; y[-fi:]*=np.linspace(1,0,fi)[:,None]
fn=f"{OUT}/{name}_整軌_降噪增益_大人靜音.wav"; sf.write(fn,y,sr,subtype="PCM_24")
r,_=sf.read(fn); red=20*np.log10(out)
muted=sum(b["e"]-b["a"] for b in blocks)
print("寫出",os.path.basename(fn),"%.1f s  峰值 %.2f dBFS"%(len(r)/sr,20*np.log10(np.abs(r).max())))
print("靜音 %d 塊，共 %.1f s（%.0f%%）；留下 %.1f s"%(len(blocks),muted,100*muted/total,total-muted))
print("限幅器動作（壓超過 0.5 dB）%.2f s，最大壓 %.1f dB"%((red<-0.5).sum()/sr,-red.min()))
for b in blocks:
    ia,ie=int(b["a"]*sr),int(b["e"]*sr); assert np.abs(r[ia:ie]).max()==0
    print("  %6.1f–%6.1f s  %4.1f s  %s"%(b["a"],b["e"],b["e"]-b["a"],"、".join(sorted(b["why"]))))
print("靜音區讀回全為 0：通過")
# 保留但有疑慮的段
print("保留但有疑慮：")
for s in segs:
    if not s["why"] and s["f0"]>=225 and (s["lowf0"]>0.06 or s["lowband"]>0.12): print("  %6.1f–%6.1f s  F0 %d  低音高幀 %d%%  低頻帶 %d%%"%(s["start"],s["end"],s["f0"],s["lowf0"]*100,s["lowband"]*100))
m=pyln.Meter(sr,block_size=0.1); keep=r[gain>0.99]; print("留下的部分響度 %.1f LUFS"%m.integrated_loudness(keep))
