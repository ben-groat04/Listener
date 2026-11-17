import json,numpy as np,librosa
D='/home/user/Listener/v1/data/t_birdwalk/'
p=json.load(open(D+'music_views/per_second_levels.json'))
print('t dbfs width voc drums bass other')
for r in p[36:64]: print(r['t'],r['dbfs'],r['width'],r['vocals'],r['drums'],r['bass'],r['other'])
cl=json.load(open(D+'music_views/clap_tags.json'))
print([k for k in cl.keys()])
for k in cl:
    if k not in('labels','window_s'):
        v=cl[k]; print(k,str(v)[:300]) ; break
S={}
for s in ['drums','bass','vocals','other']:
    y,sr=librosa.load(D+f'stems_raw/htdemucs/song/{s}.wav',sr=22050,mono=True,offset=38,duration=24); S[s]=(y,sr)
y,sr=librosa.load(D+'audio/song.wav',sr=None,mono=False,offset=38,duration=24)
print('mix sample peak',np.abs(y).max())
for s in ['drums','bass']:
    y,sr=S[s]
    oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=256)
    on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=256,units='time',backtrack=False)+38
    on=on[(on>=40)&(on<60)]
    print(s,'onsets',np.round(on,2).tolist())
    print(s,'IOI',np.round(np.diff(on),2).tolist())
    if s=='drums': dn=on
    else: bn=on
# bass onsets IOI grid
ioi=np.diff(bn); k=ioi[(ioi>0.5)&(ioi<1.0)]
print('bass IOI 0.5-1 median',np.median(k))
# bass pyin 
y,sr=S['bass']
f0,v,_=librosa.pyin(y,fmin=30,fmax=150,sr=sr,frame_length=4096)
t=librosa.times_like(f0,sr=sr,hop_length=512)+38
for a,b in [(40,47),(47,59),(59,60)]:
    m=(t>=a)&(t<b)&~np.isnan(f0); print('bass f0',a,b,np.median(f0[m]) if m.any() else None,m.sum())
# 10ms stem energies per second rate around 47 and 59.4
for s in ['bass','drums','vocals','other']:
    y,sr=S[s]; h=int(sr*0.1)
    e=[20*np.log10(np.sqrt(np.mean(y[i:i+h]**2))+1e-9) for i in range(0,len(y)-h,h)]
    e=np.array(e); tt=np.arange(len(e))*0.1+38
    for a,b in [(46,47),(47,48),(58.5,59.5),(59.5,60.5)]:
        m=(tt>=a)&(tt<b); print(s,a,b,round(e[m].mean(),1))
