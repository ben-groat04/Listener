import numpy as np, soundfile as sf
D='/home/user/Listener/v1/data/t_dl_mirror/'; S=D+'stems_raw/htdemucs/song/'; sr=44100
m=sf.read(D+'audio/song.wav')[0].mean(1)
st={k:sf.read(S+k+'.wav')[0].mean(1) for k in ['vocals','drums','bass','other']}
def rms(x,a,b): s=x[int(a*sr):int(b*sr)]; return round(20*np.log10(np.sqrt((s**2).mean())+1e-9),1)
for t in [152.5,153.5,193.5,214.5,215.5,228.5]:
    print(t,{k:(rms(x,t-1.5,t-0.1),rms(x,t+0.1,t+1.5)) for k,x in [('mix',m)]+list(st.items())})
