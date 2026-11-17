import numpy as np, soundfile as sf, json
D='/home/user/Listener/v1/data/t_dl_mirror/'
S=D+'stems_raw/htdemucs/song/'
sr=44100
st={n:sf.read(S+n+'.wav')[0].mean(1) for n in ['vocals','drums','bass','other']}
m=sf.read(D+'audio/song.wav')[0].mean(1)
def rms(x,a,b): s=x[int(a*sr):int((b+0)*sr)]; return round(20*np.log10(np.sqrt(np.mean(s**2))+1e-9),1)
for a in [3*60+30,3*60+34,3*60+36,3*60+40,3*60+44,3*60+48,3*60+52,3*60+54,3*60+56]:
    print(f"{a//60}:{a%60:02d}",'mix',rms(m,a,a+2),{k:rms(x,a,a+2) for k,x in st.items()})
b=json.load(open(D+'audio_features/beat_times.json')); b=b if isinstance(b,list) else list(b.values())[0]
b=np.array(b); print('beats',b[:3],len(b))
for t in [10.4,12.3,14.5,23.8,24.8,30.3,71.9,73.0,84.0,89.5,131.9,134,194,]:
    k=np.argmin(abs(b-t)); print(t,'nearest beat',round(b[k],2),'off',round(t-b[k],2))
# verse line starts at 30.38 +2.508*k vs beats
ib=np.diff(b); print('median ibi',np.median(ib))
