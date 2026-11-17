import numpy as np, librosa, json, sys
D='/home/user/Listener/v1/data/video1/'
y,sr=librosa.load(D+'audio/song.wav',sr=22050,mono=True)
hop=512
oenv=librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
ft=librosa.frames_to_time(np.arange(len(oenv)),sr=sr,hop_length=hop)
secs=[(0,15),(15,40),(40,66),(66,76),(76,88),(88,109),(109,118),(118,134),(134,159),(159,172),(172,189)]
out={}
for a,b in secs:
    seg=oenv[(ft>=a)&(ft<b)]; seg=seg-seg.mean()
    ac=np.correlate(seg,seg,'full')[len(seg)-1:]; ac/=ac[0]
    lag=np.arange(len(ac))*hop/sr
    # top peaks between 0.25 and 3.5s
    m=(lag>0.25)&(lag<3.5)
    idx=np.where(m)[0]
    pk=[i for i in idx[1:-1] if ac[i]>ac[i-1] and ac[i]>=ac[i+1]]
    pk=sorted(pk,key=lambda i:-ac[i])[:5]
    out[f'{a}-{b}']=[(round(lag[i],3),round(60/lag[i],1),round(float(ac[i]),2)) for i in pk]
    print(a,b,out[f'{a}-{b}'])
# tempo from beat_times
bt=json.load(open(D+'audio_features/beat_times.json'))
print(type(bt), str(bt)[:200])
# stems per section
st=json.load(open(D+'stems/stem_rms_per_second.json'))
for a,b in secs:
    print(a,b,{k:round(float(np.mean(v[a:b])),3) for k,v in st.items() if isinstance(v,list)}, 'vox active frac', round(float(np.mean(np.array(st['vocals'][a:b])>0.01)),2))
# hpss
H,P=librosa.effects.hpss(y)
for a,b in secs:
    s=slice(int(a*sr),int(b*sr))
    print(a,b,'H/P dB',round(10*np.log10((H[s]**2).mean()/(P[s]**2).mean()),1))
