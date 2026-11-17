import numpy as np, soundfile as sf
D='/home/user/Listener/v1/data/t_dl_mirror/'; sr=44100
S={k:sf.read(D+f'stems_raw/htdemucs/song/{k}.wav')[0].mean(1) for k in ['drums','bass','vocals','other']}
S['mix']=sf.read(D+'audio/song.wav')[0].mean(1)
def lv(y,a,b): return round(20*np.log10(np.sqrt((y[int(a*sr):int(b*sr)]**2).mean())+1e-9),1)
for t in [10.4,152.5,214.7,224.3,229.0,236.0]:
    print(t,{k:(lv(v,t-1,t),lv(v,t,t+1)) for k,v in S.items()})
