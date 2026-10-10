"""平靜呼吸層（第二版）：只用平順的吸吐檔，剪、疊、淡入淡出、音量。每分鐘約 11 次，吐氣長、吸氣短、中間留停頓。"""
import numpy as np, soundfile as sf, pathlib
from scipy.signal import resample_poly
from math import gcd
SR=44100; rng=np.random.default_rng(7)
R=pathlib.Path("/Users/zonesound/Library/Mobile Documents/com~apple~CloudDocs/Documents/03_Projects_Operations/Active/ITRI_工研院藝術進駐/錄音")
S=R/"Splice素材"
def rd(p):
    x,sr=sf.read(p,always_2d=True)
    if sr!=SR: g=gcd(SR,sr); x=resample_poly(x,SR//g,sr//g,axis=0)
    if x.shape[1]==1: x=np.repeat(x,2,axis=1)   # 單聲道檔複製成立體聲
    return x/ (np.max(np.abs(x))+1e-9)
def fade(x,fi,fo):
    x=x.copy(); k=int(fi*SR); x[:k]*=np.sin(np.linspace(0,np.pi/2,k))[:,None]**2
    k=int(fo*SR); x[-k:]*=np.cos(np.linspace(0,np.pi/2,k))[:,None]**2; return x
def seg(x,a,b): return x[int(a*SR):int(b*SR)]
inh=[fade(seg(rd(S/"02_呼吸_近距吸吐/EX_BR_Vocal_FX_Inhale_Mouth_Male_Wet.wav"),0,2.6),0.3,0.8),
     fade(seg(rd(S/"02_呼吸_近距吸吐/EX_AI_90_vocal_breath_dry.wav"),0,2.4),0.3,0.8)]
exh=[fade(seg(rd(S/"02_呼吸_近距吸吐/EX_BR_Vocal_FX_Exhale_Calm_Male_Dry.wav"),0.2,5.8),0.5,1.5),
     fade(seg(rd(S/"02_呼吸_近距吸吐/EX_BR_Vocal_FX_Exhale_Calm_Male_Dry.wav"),5.6,11.0),0.5,1.5),
     fade(seg(rd(S/"02_呼吸_近距吸吐/EX_AI_90_vocal_breath_dry.wav"),2.4,5.2),0.5,1.2),
     fade(seg(rd(S/"05_呼吸_長段與運動緩和/BRS_Human_F_Breaths_Exercise_Cool_Down_3.wav"),1.0,5.5),0.5,1.5)]
grp=fade(rd(S/"02_呼吸_近距吸吐/EX_BR_FX_Group_Vocals_One_Breath_In_Out_Andrea.wav"),1.0,2.0)   # 多人同吸同吐，當偶爾的第二聲部
def place(c,x,t,g=1.0):
    o=int(t*SR); n=min(len(x),len(c)-o)
    if n>0: c[o:o+n]+=x[:n]*g
def build(length):
    c=np.zeros((int(length*SR)+5*SR,2)); t=1.0
    while t<length:
        i=inh[rng.integers(len(inh))]; e=exh[rng.integers(len(exh))]
        place(c,i,t,rng.uniform(0.5,0.7))
        place(c,e,t+len(i)/SR*0.85,rng.uniform(0.8,1.0))
        t+=rng.uniform(4.8,6.2)                      # 每口氣 5 到 6 秒 = 每分鐘 10 到 12 次
    for t2 in np.arange(20,length-14,rng.uniform(38,50)):
        place(c,grp,t2,0.35)
    return c[:int(length*SR)]
def loopable(x,xf=3.0):
    k=int(xf*SR); a=np.cos(np.linspace(0,np.pi/2,k))**2
    body=x[:-k].copy(); body[:k]=body[:k]*(1-a)[:,None]+x[-k:]*a[:,None]; return body
out=R/"背景pad_20260908"
b240=loopable(build(243.0)); b240*=0.45/np.max(np.abs(b240))       # 峰值約 −7 dBFS，跟舊檔一致
sf.write(out/"00_待機_呼吸層_loop.wav",b240,SR,subtype="PCM_24")
end=build(24.0)[:20*SR]; k=12*SR; end[-k:]*=np.cos(np.linspace(0,np.pi/2,k))[:,None]**2; end*=0.45/np.max(np.abs(end))
sf.write(out/"05_結尾_呼吸收尾_20s.wav",end,SR,subtype="PCM_24")
sf.write(out/"素材/呼吸層_平靜版_240s_loop.wav",b240,SR,subtype="PCM_24")
# 候選呼吸試聽：五支各放原檔，中間 1.5 秒靜音
cands=["02_呼吸_近距吸吐/EX_AI_90_vocal_breath_dry.wav","02_呼吸_近距吸吐/EX_BR_Vocal_FX_Inhale_Mouth_Male_Wet.wav","02_呼吸_近距吸吐/EX_BR_Vocal_FX_Exhale_Calm_Male_Dry.wav","05_呼吸_長段與運動緩和/BRS_Human_F_Breaths_Exercise_Cool_Down_3.wav","02_呼吸_近距吸吐/EX_BR_FX_Group_Vocals_One_Breath_In_Out_Andrea.wav"]
parts=[]
for cnd in cands: parts+= [rd(S/cnd)*0.7, np.zeros((int(1.5*SR),2))]
sf.write(out/"拼貼demo/呼吸候選_試聽_依序五支.wav",np.concatenate(parts),SR,subtype="PCM_16")
print("breath ok")
