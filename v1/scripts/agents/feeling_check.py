import json,numpy as np,soundfile as sf,librosa
b='/home/user/Listener/v1/data/t_cshells_cshore/'
d=json.load(open(b+'music_views/per_second_levels.json'))
db=np.array([x['dbfs'] for x in d]);voc=np.array([x['vocals'] for x in d]);bas=np.array([x['bass'] for x in d]);dr=np.array([x['drums'] for x in d]);w=np.array([x['width'] for x in d])
print('mix dB per 10s mean (nonzero):')
for s in range(0,360,10):
    seg=db[s:s+10]; print(s//60,s%60,round(seg.max(),1),round(seg.min(),1),'bass',round(bas[s:s+10].mean(),1),'drums',round(dr[s:s+10].mean(),1),'voc',round(voc[s:s+10].max(),1))
y,sr=sf.read(b+'audio/song.wav');m=y.mean(1) if y.ndim>1 else y
print('peak',abs(y).max())
# 20s-window chord/energy changes: biggest 1s drops/rises
dd=np.diff(db[11:343]);idx=np.argsort(dd)
print('biggest drops',[(int(i)+11,round(dd[i],1)) for i in idx[:8]]);print('biggest rises',[(int(i)+11,round(dd[i],1)) for i in idx[-8:]])
# kick IOI in drum stem 2:00-4:00
k,_=sf.read(b+'stems_raw/htdemucs/song/drums.wav');k=k.mean(1)
from scipy.signal import butter,sosfilt
lo=sosfilt(butter(4,150,'low',fs=sr,output='sos'),k)
for a,e in [(120,140),(200,220),(280,300)]:
    seg=lo[a*sr:e*sr];o=librosa.onset.onset_detect(y=seg,sr=sr,units='time',backtrack=False)
    ioi=np.diff(o);print(a,'kick onsets',len(o),'median IOI',round(float(np.median(ioi)),3),'frac within 0.49±0.04 or x2/0.5x', round(float(np.mean([min(abs(i-0.488*n) for n in (0.5,1,2))<0.04 for i in ioi])),2))
