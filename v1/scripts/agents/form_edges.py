import numpy as np,librosa,sys
d=sys.argv[1]
sr=22050;hop=2205 # 0.1 s
for st in ['bass','vocals','other','drums']:
    y,_=librosa.load(f'{d}/{st}.wav',sr=sr,mono=True)
    r=librosa.feature.rms(y=y,frame_length=4410,hop_length=hop)[0]
    db=20*np.log10(r+1e-9)
    on=db>-45 if st!='drums' else db>-50
    ch=np.flatnonzero(np.diff(on.astype(int)))
    out=[]
    for c in ch:
        t=(c+1)*0.1
        out.append(f"{'on' if on[c+1] else 'off'}@{int(t//60)}:{t%60:04.1f}")
    print(st,' '.join(out))
