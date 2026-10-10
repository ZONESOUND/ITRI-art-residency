import sys, json, numpy as np, librosa, warnings; warnings.filterwarnings("ignore")
name=sys.argv[1]; gap=0.20
y,sr=librosa.load(name+".wav",sr=16000,mono=True)
hop=160
S=np.abs(librosa.stft(y,n_fft=1024,hop_length=hop))**2
fr=librosa.fft_frequencies(sr=sr,n_fft=1024)
full=10*np.log10(S[(fr>=250)&(fr<=5000)].sum(0)+1e-12)
low=10*np.log10(S[(fr>=90)&(fr<=205)].sum(0)+1e-12)
ffloor=np.percentile(full,20); lfloor=np.percentile(low,30)
f0,vf,vp=librosa.pyin(y,fmin=80,fmax=900,sr=sr,frame_length=1024,hop_length=hop)
n=min(len(full),len(f0)); full=full[:n]; low=low[:n]; f0=f0[:n]
act=full>ffloor+10
t=lambda i:i*hop/sr
segs=[]; i=0
while i<n:
    if act[i]:
        j=i
        while j<n and act[j]: j+=1
        segs.append([i,j]); i=j
    else: i+=1
m=[]
for s in segs:
    if m and t(s[0])-t(m[-1][1])<gap: m[-1][1]=s[1]
    else: m.append(s)
m=[s for s in m if t(s[1])-t(s[0])>=0.15]
W=json.load(open("whisper/"+name+".json"))
words=[(w['start'],w['end'],w['word']) for s in W['segments'] for w in s.get('words',[])]
out=[]
print("== %s floor %.0f lowfloor %.0f"%(name,ffloor,lfloor))
for a,b in m:
    f=f0[a:b]; f=f[~np.isnan(f)]
    f=np.where(f>520,f/2,f)   # fold octave errors
    med=np.median(f) if len(f) else 0
    lowf=np.mean(f<225) if len(f) else 0
    lowband=np.mean(low[a:b]>lfloor+12)
    snr=np.percentile(full[a:b],90)-ffloor
    txt="".join(w for s,e,w in words if e>t(a)+0.05 and s<t(b)-0.05)
    out.append(dict(file=name,start=round(t(a),3),end=round(t(b),3),f0=float(med),lowf0=float(lowf),lowband=float(lowband),snr=float(snr),voiced=len(f)/(b-a),txt=txt))
    print("%7.2f-%7.2f %5.2fs F0 %3.0f lowF0 %3.0f%% lowband %3.0f%% voiced %3.0f%% snr %2.0f  %s"%(t(a),t(b),t(b)-t(a),med,lowf*100,lowband*100,100*len(f)/(b-a),snr,txt[:36]))
json.dump(out,open(name+"_seg2.json","w"),ensure_ascii=False)
