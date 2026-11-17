import numpy as np, librosa
D='/home/user/Listener/v1/data/t_dl_mirror/'
S=D+'stems_raw/htdemucs/song/'
sr=22050
def ld(p):
    y,_=librosa.load(p,sr=sr,mono=True); return y
mix=ld(D+'audio/song.wav'); st={k:ld(S+k+'.wav') for k in ['drums','bass','vocals','other']}
hop=int(sr*0.1)
def env(y):
    return 20*np.log10(librosa.feature.rms(y=y,frame_length=hop*2,hop_length=hop)[0]+1e-9)
E={k:env(v) for k,v in st.items()}; E['mix']=env(mix)
n=len(E['mix']); print('dur',len(mix)/sr)
def seg(k,a,b):
    y=(st[k] if k!='mix' else mix)[int(a*sr):int(b*sr)]; return 10*np.log10(np.mean(y**2)+1e-12)
print('t  mix drums bass vocals other')
for a in range(0,240,5):
    print(f'{a//60}:{a%60:02d}',*[f'{seg(k,a,a+5):6.1f}' for k in ['mix','drums','bass','vocals','other']])
for k,th in [('vocals',-40),('bass',-40)]:
    on=E[k]>th; spans=[];s=None
    for i,o in enumerate(on):
        if o and s is None:s=i
        if not o and s is not None:
            spans.append((s/10,i/10)); s=None
    if s is not None: spans.append((s/10,n/10))
    m=[]
    for a,b in spans:
        if m and a-m[-1][1]<0.8: m[-1]=(m[-1][0],b)
        else: m.append((a,b))
    print(k,'on-spans >=2s:',[(round(a,1),round(b,1)) for a,b in m if b-a>=2])
print('peak mix dBFS',20*np.log10(np.abs(mix).max()))
