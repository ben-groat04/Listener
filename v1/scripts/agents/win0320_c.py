import numpy as np, librosa
D='/home/user/Listener/v1/data/t_cshells_cshore/'
sr=22050
y=librosa.load(D+'audio/song.wav',sr=sr,mono=True)[0]
vo=librosa.load(D+'stems_raw/htdemucs/song/vocals.wav',sr=sr,mono=True)[0]
def peaks(x,a,b,n=8):
    s=x[int(a*sr):int(b*sr)]*np.hanning(int((b-a)*sr));S=np.abs(np.fft.rfft(s,2**17));f=np.fft.rfftfreq(2**17,1/sr)
    m=(f>60)&(f<3000);idx=np.argsort(S*m)[::-1];out=[]
    for i in idx:
        if all(abs(f[i]-o)>15 for o in out): out.append(f[i])
        if len(out)>=n:break
    return [round(o) for o in out]
for a,b in [(318,322),(324,328),(330,332),(333,336)]: print('mix peaks',a,b,peaks(y,a,b))
# rolloff of speech
for a,b in [(331,333),(337,340),(341,342.8)]:
    s=vo[int(a*sr):int(b*sr)];S=np.abs(np.fft.rfft(s))**2;f=np.fft.rfftfreq(len(s),1/sr);c=np.cumsum(S)/S.sum();print('vocal stem',a,b,'85% rolloff',round(f[np.searchsorted(c,.85)]),'99%',round(f[np.searchsorted(c,.99)]))
    s=y[int(a*sr):int(b*sr)];S=np.abs(np.fft.rfft(s))**2;c=np.cumsum(S)/S.sum();print('mix',a,b,'85%',round(f[np.searchsorted(c,.85)]),'99%',round(f[np.searchsorted(c,.99)]))
h=int(.01*sr)
e=20*np.log10(np.sqrt(np.convolve(vo**2,np.ones(h)/h,'same'))[::h]+1e-9)
t=np.arange(len(e))*.01
print('vocal env 330.2..330.8',[round(e[int(x*100)],0) for x in np.arange(330.2,330.9,.1)])
print('vocal stem 10ms env bursts >-50 between 329-343:',[round(x,1) for x in t[(e>-48)&(t>329)&(t<343)][::10]][:40])
# mix env step at 330.5
em=20*np.log10(np.sqrt(np.convolve(y**2,np.ones(h)/h,'same'))[::h]+1e-9)
print('mix env 329..332 at .5s',[round(em[int(x*100)],1) for x in np.arange(329,332.1,.5)])
