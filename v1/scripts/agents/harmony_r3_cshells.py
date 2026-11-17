import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_cshells_cshore/stems_raw/htdemucs/song/'
sr=22050
def L(n): return librosa.load(D+n+'.wav',sr=sr,mono=True)[0]
oth,bas,voc=L('other'),L('bass'),L('vocals')
def spec(y,t0,t1,n=2**16):
    s=y[int(t0*sr):int(t1*sr)]; s=s*np.hanning(len(s))
    S=np.abs(np.fft.rfft(s,n)); f=np.fft.rfftfreq(n,1/sr); return f,S
def pk(y,t0,t1,fc,tol=1.5):
    f,S=spec(y,t0,t1); m=(f>fc*2**(-tol/12))&(f<fc*2**(tol/12)); return 20*np.log10(S[m].max()+1e-12)
def cl(y,t0,t1,name):
    f,S=spec(y,t0,t1); ref=None
    print(name,t0,t1)
# 1 chords vs stabs
ch=json.load(open('/home/user/Listener/v1/data/t_cshells_cshore/music_views/chords.json'))
stabs=[60.8,64.8,68.8,72.9,76.8,80.8,82.8,88.9,97.0,113.4]
cg=[(c['start'],c['chord']) for c in ch if 60<=c['start']<120]
print('changes 60-120',len(cg))
for s in stabs:
    near=[(round(t,2),c) for t,c in cg if abs(t-s)<0.3]; print('stab',s,near)
# collapse labels: runs of A-family
print([ (round(t,1),c) for t,c in cg][:40])
# 2 drone partials
for (a,b) in [(25.0,32.0)]:
    f0=220*2**(-22/1200)
    print('drone partials (other), dB rel p1, f0 search near 217-221')
    f,S=spec(oth,a,b)
    m=(f>205)&(f<235); fb=f[m][S[m].argmax()]; print('f0',fb)
    base=None
    for k in range(1,9):
        mm=(f>fb*k*0.985)&(f<fb*k*1.015); v=20*np.log10(S[mm].max()+1e-12)
        base=v if base is None else base; print(k,round(fb*k,1),round(v-base,1))
    for nm,fc in [('C4 261.6',261.6),('C#4 277.2',277.2),('E4 329.6',329.6),('G4 392',392.0)]:
        print(nm,round(pk(oth,a,b,fc,0.6)-pk(oth,a,b,fb,0.6),1))
# 3 final pad
for (a,b) in [(5*60+22,5*60+30),(5*60+30,5*60+38),(5*60+22,5*60+38)]:
    f,S=spec(oth,a,b); 
    print('pad',a,b)
    for nm,fc in [('A3 220',220),('C4 261.6',261.6),('C#4 277.2',277.2),('E4 329.6',329.6),('A4',440),('C#5',554.4),('E5',659.3),('G5',784)]:
        print(' ',nm,round(pk(oth,a,b,fc,0.7),1))
# 4 2:22 other stem
for (a,b) in [(141.5,142.5),(142.5,146)]:
    print('2:22 other',a,b,[ (n,round(pk(oth,a,b,fc,0.5),1)) for n,fc in [('A3',219),('E4',328),('A4',438),('E5',657)]])
    print('   vocals',[ (n,round(pk(voc,a,b,fc,0.5),1)) for n,fc in [('A3',219),('E4',328),('A4',438),('E5',657)]])
# 5 3:44, 5:12 1.2-1.6k
for t in [224,312]:
    for nm,y in [('other',oth),('vocals',voc)]:
        f,S=spec(y,t-1,t+2); m=(f>1000)&(f<1800); i=S[m].argmax(); 
        base=np.median(S[(f>300)&(f<4000)])
        print(nm,t,'peak',round(f[m][i],0),'dB over median',round(20*np.log10(S[m][i]/base),1))
# 6 bass onset sharpness before/after 3:20
for (a,b) in [(150,190),(200,225),(255,280)]:
    s=bas[int(a*sr):int(b*sr)]; o=librosa.onset.onset_strength(y=s,sr=sr,hop_length=220)
    pks=librosa.onset.onset_detect(onset_envelope=o,sr=sr,hop_length=220)
    env=librosa.feature.rms(y=s,hop_length=220)[0]
    print('bass',a,b,'onsets/s',round(len(pks)/(b-a),2),'mean onset str',round(o[pks].mean(),2) if len(pks) else 0,'crest rms dB',round(20*np.log10(np.percentile(env,95)/(np.percentile(env,20)+1e-9)),1))
