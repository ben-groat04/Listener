import numpy as np, librosa
D='/home/user/Listener/v1/data/video1/'
v,sr=librosa.load(D+'stems_raw/htdemucs/song/vocals.wav',sr=22050)
def env(a,b):
    y=v[int(a*sr):int(b*sr)];return librosa.feature.rms(y=y,hop_length=441)[0]
a=env(27.9,31.8);b=env(2*60+44.3,2*60+48.2)
n=min(len(a),len(b));print('env corr',np.corrcoef(a[:n],b[:n])[0,1])
for lag in range(-10,11,5):
    x=a[max(0,lag):n+min(0,lag)];y=b[max(0,-lag):n-max(0,lag)];m=min(len(x),len(y));print(lag,np.corrcoef(x[:m],y[:m])[0,1].round(2))
# pitch contour corr
def f(a,b):
    f0,_,_=librosa.pyin(v[int(a*sr):int(b*sr)],fmin=70,fmax=400,sr=sr,hop_length=441);return f0
fa=f(27.9,31.8);fb=f(2*60+44.3,2*60+48.2);m=min(len(fa),len(fb));ok=~np.isnan(fa[:m])&~np.isnan(fb[:m])
print('f0 corr',np.corrcoef(fa[:m][ok],fb[:m][ok])[0,1],'n',ok.sum(),'medians',np.nanmedian(fa),np.nanmedian(fb))
# mix level 3:00-3:08 vocal rms
print('vocals rms dB 2:50-3:08', 20*np.log10(env(170,188).max()+1e-9))
# first-vs-last words: duck test: mix dBFS during speech vs prior second via other stem
import json
L=json.load(open(D+'music_views/per_second_levels.json'))
sp=[(10,16),(20,31),(41,42),(51,56),(79,87),(144,156),(164,168)]
for a_,b_ in sp:
    print(a_, 'other stem mean',np.mean([L[t]['other'] for t in range(a_,b_)]).round(1),'drums',np.mean([L[t]['drums'] for t in range(a_,b_)]).round(1),'vox',np.mean([L[t]['vocals'] for t in range(a_,b_)]).round(1),'width',np.mean([L[t]['width'] for t in range(a_,b_)]).round(2))
