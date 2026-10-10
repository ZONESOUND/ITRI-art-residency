"""素材拼貼 demo：只做剪、疊、淡入淡出、音量、pan。不濾波、不拉伸、不變調、不合成。"""
import numpy as np, soundfile as sf, pathlib
SR=44100
R=pathlib.Path("/Users/zonesound/Library/Mobile Documents/com~apple~CloudDocs/Documents/03_Projects_Operations/Active/ITRI_工研院藝術進駐/錄音")
OUT=R/"背景pad_20260908/拼貼demo"; OUT.mkdir(exist_ok=True)
from scipy.signal import resample_poly
from math import gcd
def rd(p):
    x,sr=sf.read(p,always_2d=True)
    if sr!=SR:                      # 只做取樣率轉換（例如 48k → 44.1k），不是音色處理
        g=gcd(SR,sr); x=resample_poly(x,SR//g,sr//g,axis=0)
    return x
def db(d): return 10**(d/20)
def fade(x,fi=0,fo=0):
    x=x.copy(); n=len(x)
    if fi: k=int(fi*SR); x[:k]*=np.sin(np.linspace(0,np.pi/2,k))[:,None]**2
    if fo: k=int(fo*SR); x[-k:]*=np.cos(np.linspace(0,np.pi/2,k))[:,None]**2
    return x
def place(canvas,x,t,gain_db=0.0):
    o=int(t*SR); n=min(len(x),len(canvas)-o)
    if n>0: canvas[o:o+n]+=x[:n]*db(gain_db)
def bed_from_decay(src,seg=(1.5,17.5),chunk=10.0,overlap=6.0,length=120.0):
    """把一次敲擊的衰減尾巴切成 10 秒段，段與段以 6 秒交叉淡化重疊鋪成連續底層；每段只用音量拉平。"""
    a,b=int(seg[0]*SR),int(seg[1]*SR); tail=src[a:b]
    canvas=np.zeros((int(length*SR)+SR,2)); t=0.0; i=0
    while t<length:
        st=int((i*3.7)%(len(tail)/SR-chunk)*SR)             # 每段從尾巴不同位置起，避免固定循環感
        piece=tail[st:st+int(chunk*SR)]
        piece=piece/ (np.sqrt(np.mean(piece**2))+1e-9)*0.05  # 段內只做整體音量對齊
        place(canvas,fade(piece,overlap,overlap),t); t+=chunk-overlap; i+=1
    return canvas[:int(length*SR)]
def loop_fill(src,length,xf=4.0,trim_end=0.0):
    if trim_end: src=src[:-int(trim_end*SR)]
    canvas=np.zeros((int(length*SR)+SR,2)); t=0.0; L=len(src)/SR
    while t<length: place(canvas,fade(src,xf,xf),t); t+=L-xf
    return canvas[:int(length*SR)]

bowl=rd(R/"背景pad_20260908/素材/_splice/MYS_CrystalBowl_Percussive_C_266Hz.wav")
breath=rd(R/"背景pad_20260908/素材/呼吸層_平靜版_240s_loop.wav")   # 第二版平靜呼吸層（breath_layer.py）
night=rd("/Users/zonesound/Documents/GitHub/ITRI-art-residency/live_demo/Live_Demo Project/Night animals.wav")
hum=rd(R/"背景pad_20260908/素材/小星星_主音C_音框拼接_5.5s.wav")
hum_note=fade(hum[int(0.0*SR):int(1.4*SR)],0.25,0.6)      # 第一個吟唱 C 音，原長度

def mix(layers,length,peak_db=-3.0):
    c=np.zeros((int(length*SR),2))
    for x,g in layers: c[:len(x)]+=x[:len(c)]*db(g)
    return c*(db(peak_db)/np.max(np.abs(c)))

L=120
bowl_bed=bed_from_decay(bowl,length=L)
br=loop_fill(breath,L,xf=3.0)
ni=loop_fill(night,L,xf=8.0)
hum_track=np.zeros((L*SR,2))
for t in (35.0,82.0): place(hum_track,hum_note,t)
A=mix([(bowl_bed,0),(br,-14),(ni,-20),(hum_track,-4)],L)
sf.write(OUT/"拼貼demoA_第一幕_水晶缽C+呼吸+夜聲+吟唱殘影_120s.wav",A,SR,subtype="PCM_24")
B=mix([(bed_from_decay(bowl,length=60),0),(loop_fill(breath,60,3.0),-20)],60)
sf.write(OUT/"拼貼demoB_第三幕地板_水晶缽C+呼吸_60s.wav",B,SR,subtype="PCM_24")
C=mix([(bowl_bed,0)],L,-6)
sf.write(OUT/"拼貼demoC_只有水晶缽底層_120s.wav",C,SR,subtype="PCM_24")
# 疊講話
sp=rd("/private/tmp/claude-501/-Users-zonesound-Library-Application-Support-Claude-scratch-workspaces-ae7a6576-568b-4e61-9ed1-513d12b6d16d-33c77634-13c4-48ad-88b2-07fb30802efc-scratch-2026-09-08-6f8d58/a56f7396-a641-4341-86a4-52a742d9ebbe/scratchpad/speech_0812_0055-0250.wav")
def rms(x): return np.sqrt(np.mean(x**2))
pad=A[:len(sp)]; g=db(-20)*rms(sp)/rms(pad); m=sp+pad*g; m=m/max(1,np.max(np.abs(m))/0.98)
sf.write(OUT/"拼貼demoA_疊8月12日講話_低20dB.wav",m,SR,subtype="PCM_16")
print("ok")
