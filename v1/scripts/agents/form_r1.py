import numpy as np, soundfile as sf, json, sys
D='/home/user/Listener/v1/data/t_cshells_cshore/'
def load(p):
    x,sr=sf.read(p,always_2d=True); return x.mean(1),sr
mix,sr=load(D+'audio/song.wav')
st={k:load(D+f'stems_raw/htdemucs/song/{k}.wav')[0] for k in ['drums','bass','vocals','other']}
st['mix']=mix
def env(x,hop=0.01):
    n=int(sr*hop); m=len(x)//n
    return 20*np.log10(np.sqrt((x[:m*n].reshape(m,n)**2).mean(1))+1e-12)
E={k:env(v) for k,v in st.items()}
np.savez('/tmp/form_env.npz',**E)
print('sr',sr,'len',len(mix)/sr,'peak',np.abs(mix).max(), 20*np.log10(np.abs(mix).max()))
nz=np.nonzero(mix)[0]; print('first nz',nz[0]/sr,'last nz',nz[-1]/sr, 'last amp',mix[nz[-1]])
# last 3 s env
e=E['mix']; print('mix last 3 s max env', e[-300:].max())
# tail near end of sound: 10ms env from 5:38 to 5:43
for t in np.arange(338,343.2,0.5):
    i=int(t*100); print('%.1f'%t, ' '.join('%s %.1f'%(k[:2],E[k][i:i+50].mean()) for k in E))
# peak count in last 3 s all stems
for k,v in st.items():
    seg=v[-3*sr:]; print(k,'max abs last3s',np.abs(seg).max())
# peaks of mix 10ms env near the end of sound
from scipy.signal import find_peaks
seg=E['mix'][33800:34300]; p,_=find_peaks(seg,prominence=3); print('env peaks 338-343', [(33800+i)/100 for i in p][:30])
