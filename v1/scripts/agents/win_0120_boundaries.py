import numpy as np,librosa
D='/home/user/Listener/v1/data/t_cshells_cshore/';S=D+'stems_raw/htdemucs/song/'
sr=22050
X={n:librosa.load(S+n+'.wav',sr=sr,mono=True)[0] for n in['vocals','drums','bass','other']}
X['mix']=librosa.load(D+'audio/song.wav',sr=sr,mono=True)[0]
def db(x):return 20*np.log10(np.sqrt((x**2).mean())+1e-9)
def cen(x):return librosa.feature.spectral_centroid(y=x,sr=sr)[0].mean()
def hf(x):
    S_=np.abs(librosa.stft(x,n_fft=2048))**2;f=librosa.fft_frequencies(sr=sr,n_fft=2048);return 10*np.log10(S_[f>5000].sum()/S_.sum()+1e-12)
for b in[123.0,125.4,127.5,129.5,133.5,137.6]:
    print('boundary',b)
    for n,x in X.items():
        a=x[int((b-1.5)*sr):int(b*sr)];c=x[int(b*sr):int((b+1.5)*sr)]
        print(f' {n:7s} before {db(a):6.1f} after {db(c):6.1f} d={db(c)-db(a):+5.1f}  cen {cen(a):5.0f}->{cen(c):5.0f}  HF(>5k) share {hf(a):5.1f}->{hf(c):5.1f}')
# dropout detail
x=X['mix'];e=np.sqrt(np.convolve(x**2,np.ones(220)/220,'same'))
for t in np.arange(122.5,126,0.25):print(round(t,2),round(db(x[int(t*sr):int((t+.25)*sr)]),1),round(db(X['other'][int(t*sr):int((t+.25)*sr)]),1))
# loop regularity: correlation of bass env bar-to-bar (bar=4 beats=1.952s)
bar=60/123.047*4
def seg(x,t):return x[int(t*sr):int((t+bar)*sr)]
for st in [120,123,127.5]:
    a=seg(X['bass'],st);b=seg(X['bass'],st+bar);ea=np.abs(a)[:min(len(a),len(b))];eb=np.abs(b)[:len(ea)]
    print('bass bar corr',st,np.corrcoef(ea,eb)[0,1])
    a=seg(X['drums'],st);b=seg(X['drums'],st+bar);n=min(len(a),len(b));print('drums bar corr',st,np.corrcoef(np.abs(a[:n]),np.abs(b[:n]))[0,1])
