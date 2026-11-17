# Feeling R2: 0.1 s mix RMS around each bass re-entry; looks for a pre-hit dip and the size of the jump.
import numpy as np, soundfile as sf
y,sr=sf.read('/home/user/Listener/v1/data/t_birdwalk/audio/song.wav'); y=y.mean(1) if y.ndim>1 else y
hop=int(sr*0.1); n=len(y)//hop
r=20*np.log10(np.sqrt((y[:n*hop].reshape(n,hop)**2).mean(1))+1e-9)
for t in [12.4,59.3,131.3,155.7]:
    i=int(t*10); print(t, ' '.join(f'{v:.0f}' for v in r[i-15:i+8]))
b=sf.read('/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/bass.wav')[0]; b=b.mean(1)
nb=len(b)//hop; rb=20*np.log10(np.sqrt((b[:nb*hop].reshape(nb,hop)**2).mean(1))+1e-9)
for t in [12.4,59.3,131.3,155.7]:
    i=int(t*10); print('bass',t,' '.join(f'{v:.0f}' for v in rb[i-15:i+8]))
