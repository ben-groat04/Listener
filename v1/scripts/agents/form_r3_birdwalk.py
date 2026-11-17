import numpy as np,librosa
d='data/t_birdwalk/stems_raw/htdemucs/song';sr=22050;h=0.25
def rms(n):
    y,_=librosa.load(f'{d}/{n}.wav',sr=sr);f=int(h*sr)
    k=len(y)//f;return 20*np.log10(np.sqrt((y[:k*f].reshape(k,f)**2).mean(1))+1e-9)
B,O,D,V=[rms(n) for n in['bass','other','drums','vocals']]
def edges(x,name,thr=-45):
    on=x>thr;out=[]
    for i in range(1,len(on)):
        if on[i]!=on[i-1]: out.append(f"{'on' if on[i] else 'off'}@{int(i*h//60)}:{i*h%60:05.2f}")
    print(name,thr,out)
edges(B,'bass',-45)
# inside first groove: bass dips, other and drums levels per 3s
for t in range(12,48,3):
    a=int(t/h);b=int((t+3)/h)
    print(f"{t//60}:{t%60:02d} bass {B[a:b].mean():.0f} other {O[a:b].mean():.0f} drums {D[a:b].mean():.0f} voc {V[a:b].mean():.0f} min bass {B[a:b].min():.0f}")
