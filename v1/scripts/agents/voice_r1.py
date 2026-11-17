import numpy as np, soundfile as sf, librosa, json
D='/home/user/Listener/v1/data/t_dl_mirror/'
S=D+'stems_raw/htdemucs/song/'
v,sr=sf.read(S+'vocals.wav'); 
vm=v.mean(1) if v.ndim>1 else v
m,_=sf.read(D+'audio/song.wav'); mm=m.mean(1) if m.ndim>1 else m
hop=int(0.25*sr)
def lv(x):
    n=len(x)//hop; return np.array([20*np.log10(np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2))+1e-9) for i in range(n)])
lvv=lv(vm); lvm=lv(mm)
# activity segments (vocal > -40 dB)
act=lvv>-40
segs=[];s=None
for i,a in enumerate(act):
    if a and s is None:s=i
    if not a and s is not None:
        segs.append((s*.25,i*.25));s=None
if s is not None: segs.append((s*.25,len(act)*.25))
# merge gaps<0.5
mg=[]
for a,b in segs:
    if mg and a-mg[-1][1]<0.5: mg[-1]=(mg[-1][0],b)
    else: mg.append((a,b))
f=lambda t:f"{int(t//60)}:{t%60:04.1f}"
print('vocal active spans:');
for a,b in mg: print(f(a),f(b),round(b-a,1))
# gaps >=0.5 s within 10-230
print('gaps inside vocals:')
for (a,b),(c,d) in zip(mg,mg[1:]): print(f(b),f(c),round(c-b,2))
# stereo width of vocal
print('vocal side/mid dB', 20*np.log10(np.std(v[:,0]-v[:,1])/np.std(v[:,0]+v[:,1]+1e-9)+1e-9) if v.ndim>1 else 'mono')
# end of track 10ms env
for name,x in [('mix',mm),('voc',vm)]+[(n,sf.read(S+n+'.wav')[0].mean(1)) for n in ['drums','bass','other']]:
    h=int(.01*sr);e=np.array([np.sqrt(np.mean(x[i:i+h]**2)) for i in range(len(x)-3*sr,len(x)-h,h)])
    db=20*np.log10(e+1e-9)
    t0=len(x)/sr-3
    last=np.where(db>-60)[0]
    print(name,'last >-60dB at',round(t0+last[-1]*.01,2) if len(last) else None,'level last 100ms',round(db[-10:].mean(),1),'peak',round(np.abs(x[-3*sr:]).max(),3))
print('dur',len(mm)/sr)
# pitch median per section
lead=json.load(open(D+'music_views/lead_notes.json'))
print(type(lead), (lead[:2] if isinstance(lead,list) else list(lead)[:3]))
