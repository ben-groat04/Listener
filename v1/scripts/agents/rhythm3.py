import json,numpy as np,librosa
D='/home/user/Listener/v1/data/t_birdwalk/'
b=np.array(json.load(open(D+'audio_features/beat_times.json')))
ib=np.diff(b)
# IBI outliers
for i in range(len(ib)):
    if abs(ib[i]-0.394)>0.03: print('ibi odd',round(b[i],2),round(ib[i],3))
# regression of beat grid: is it a single constant grid?
n=np.arange(len(b)); p=np.polyfit(n,b,1); print('fit',p, 'bpm',60/p[0]); res=b-np.polyval(p,n)
for a in range(0,188,20):
    m=(b>=a)&(b<a+20); print(a,'resid mean ms',round(res[m].mean()*1000),'sd',round(res[m].std()*1000))
# phase in grid of 16ths of drum low/high band onsets
sr=22050
y,_=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=sr,mono=True)
S=np.abs(librosa.stft(y,n_fft=2048,hop_length=256))
f=librosa.fft_frequencies(sr=sr,n_fft=2048)
low=S[(f<150)].sum(0); hi=S[(f>3000)].sum(0); t=librosa.times_like(low,sr=sr,hop_length=256)
def flux(x):
    d=np.maximum(np.diff(np.log1p(x*10)),0); return np.r_[0,d]
for name,x in [('kick<150',low),('hat>3k',hi)]:
    e=flux(x); pk=librosa.util.peak_pick(e,pre_max=6,post_max=6,pre_avg=20,post_avg=20,delta=np.percentile(e,90)*0.5,wait=8)
    tt=t[pk]
    print(name,len(tt))
    # phase relative to beat grid with 4 subdiv per beat -> units of 16ths; bar = 16 positions; need downbeat. use beat index mod 4
    for lo,hi_ in [(12,47),(47,60),(60,83),(94,119),(132,143),(156,188)]:
        sel=tt[(tt>=lo)&(tt<hi_)]
        bi=np.searchsorted(b,sel)-1; bi=np.clip(bi,0,len(b)-2)
        frac=(sel-b[bi])/ib[bi]
        pos=(bi%4)+frac  # beat-in-bar guess
        h=np.histogram(pos,bins=np.arange(0,4.01,0.25))[0]
        print('  ',lo,hi_,h)
