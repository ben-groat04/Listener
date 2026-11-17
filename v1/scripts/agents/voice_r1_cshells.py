import json,numpy as np,soundfile as sf,scipy.signal as ss
B='/home/user/Listener/v1/data/t_cshells_cshore/'
L=json.load(open(B+'music_views/per_second_levels.json'))
v=np.array([x['vocals'] for x in L]);m=np.array([x['dbfs'] for x in L]);o=np.array([x['other'] for x in L])
print('n',len(L))
# vocal-stem seconds above -65 dB
print('vocals > -65:',[(i,round(v[i],1),round(m[i],1)) for i in range(len(v)) if v[i]>-65])
voc,sr=sf.read(B+'stems_raw/htdemucs/song/vocals.wav');voc=voc.mean(1) if voc.ndim>1 else voc
mix,_=sf.read(B+'audio/song.wav');mix=mix.mean(1) if mix.ndim>1 else mix
oth,_=sf.read(B+'stems_raw/htdemucs/song/other.wav');oth=oth.mean(1) if oth.ndim>1 else oth
print(sr,len(voc)/sr)
def seg(a,b):
    x=voc[int(a*sr):int(b*sr)];y=oth[int(a*sr):int(b*sr)];z=mix[int(a*sr):int(b*sr)]
    f,P=ss.welch(x,sr,nperseg=4096);Pn=P/P.sum()
    cen=(f*Pn).sum()
    fl=np.exp(np.mean(np.log(P+1e-20)))/np.mean(P)
    # envelope correlation vs other
    h=int(sr*0.05);n=len(x)//h
    ex=np.sqrt((x[:n*h].reshape(n,h)**2).mean(1));ey=np.sqrt((y[:n*h].reshape(n,h)**2).mean(1))
    c=np.corrcoef(ex,ey)[0,1]
    pk=20*np.log10(abs(x).max()+1e-12)
    # vocal-stem share above 1 kHz
    return dict(rms=round(20*np.log10(np.sqrt((x**2).mean())+1e-12),1),peak=round(pk,1),cent=round(cen),flat=round(fl,4),envcorr_other=round(c,2),mixrms=round(20*np.log10(np.sqrt((z**2).mean())+1e-12),1))
for a,b in [(141,147),(142,146),(224,226),(227.5,229.5),(295,299),(312,313.5),(316,318),(330,343),(343,350),(100,110),(60,70),(250,258),(268.5,270)]:
    print(a,b,seg(a,b))
