import numpy as np, librosa, json, sys
D='/home/user/Listener/v1/data/t_dl_mirror/'
sr=22050
def ld(p): return librosa.load(p,sr=sr,mono=True)[0]
mix=ld(D+'audio/song.wav'); S={k:ld(D+f'stems_raw/htdemucs/song/{k}.wav') for k in ['vocals','drums','bass','other']}
full,_=librosa.load(D+'audio/song.wav',sr=None,mono=False); print('native peak dBFS',20*np.log10(np.abs(full).max()),'dur',full.shape[-1]/_)
a,b=int(220*sr),int(240*sr)
def env(x,hop=int(.01*sr)):
    n=len(x)//hop; return np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))
db=lambda v:20*np.log10(v+1e-9)
# end
print('--- last 3s 10ms env')
dur=len(mix)/sr
for nm,x in [('mix',mix)]+list(S.items()):
    e=env(x[int((dur-3.5)*sr):]); t=dur-3.5+np.arange(len(e))*.01
    audible=np.where(db(e)>-60)[0]; 
    print(nm,'last>-60dB',round(t[audible[-1]],2) if len(audible) else None,'last>-50',round(t[np.where(db(e)>-50)[0][-1]],2) if (db(e)>-50).any() else None,'end level',round(db(e[-5:]).mean(),1))
e=env(mix[int((dur-3.5)*sr):]); t=dur-3.5+np.arange(len(e))*.01
from scipy.signal import find_peaks
pk,_=find_peaks(e,height=e.max()*0.15,distance=8); print('mix env peaks',[(round(t[i],2),round(db(e[i]),1)) for i in pk])
print('duration',dur)
# per-0.5 s mix/stem levels 3:48..3:58
for s in np.arange(228,238,0.5):
    i,j=int(s*sr),int((s+.5)*sr); print(s, round(db(np.sqrt((mix[i:j]**2).mean())),1), {k:round(db(np.sqrt((v[i:j]**2).mean())),1) for k,v in S.items()})
# kicks from drums low band
import scipy.signal as sg
sos=sg.butter(4,[40,120],'bp',fs=sr,output='sos'); k=sg.sosfilt(sos,S['drums'][a:b])
oe=librosa.onset.onset_strength(y=k,sr=sr,hop_length=256); on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=256,units='time',backtrack=False)
print('kick onsets(rel)',np.round(on,2)); ioi=np.diff(on); print('IOI median',np.median(ioi),'bpm',60/np.median(ioi))
bt=np.array(json.load(open(D+'audio_features/beat_times.json')) if not isinstance(json.load(open(D+'audio_features/beat_times.json')),dict) else json.load(open(D+'audio_features/beat_times.json'))['beats'])
bt=bt[(bt>=220)&(bt<240)]-220; print('beat ioi',np.median(np.diff(bt)),60/np.median(np.diff(bt)))
dev=[min(abs(o-bt))*1000 for o in on]; print('kick-to-beat dev ms median',np.median(dev),'max',max(dev))
# drum onsets full band
o2=librosa.onset.onset_detect(y=S['drums'][a:b],sr=sr,units='time'); print('drum onsets n',len(o2),np.round(o2,2))
# drum band energy by region
for (s,e_) in [(0,8),(8,16)]:
    x=S['drums'][a+int(s*sr):a+int(e_*sr)]; print(s,e_,'drums rms',db(np.sqrt((x**2).mean())))
# spectral centroid/bands mix
for s in [0,5,10,14,16,17,18]:
    x=mix[a+int(s*sr):a+int((s+1)*sr)]; sp=np.abs(np.fft.rfft(x))**2; f=np.fft.rfftfreq(len(x),1/sr)
    print(s,'centroid',round((f*sp).sum()/sp.sum()),'>4k share',round(sp[f>4000].sum()/sp.sum(),4),'>8k',round(sp[f>8000].sum()/sp.sum(),5))
# loop regularity: bar = 4 beats ~2.5 s; correlation of consecutive bars of mix, other
bar=2.5
mel=lambda x:librosa.feature.melspectrogram(y=x,sr=sr,hop_length=512)
for nm,x in [('mix',mix),('drums',S['drums']),('other',S['other'])]:
    m=np.log(mel(x[a:b])+1e-6); bl=int(round(bar*sr/512*1))
    # estimate bar length from beats*4
    bl=int(round(4*np.median(np.diff(bt))*sr/512))
    cs=[np.corrcoef(m[:,i*bl:(i+1)*bl].ravel(),m[:,(i+1)*bl:(i+2)*bl].ravel())[0,1] for i in range(0,5)]
    print(nm,'bar',bl,'consecutive-bar mel corr',np.round(cs,3))
# peak in this window, native
print('win peak',20*np.log10(np.abs(full[:,int(220*_):int(240*_)]).max()))
