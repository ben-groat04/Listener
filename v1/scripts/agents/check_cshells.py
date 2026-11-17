import numpy as np, soundfile as sf, json, collections
y,sr=sf.read('audio/song.wav'); m=np.abs(y).max(1) if y.ndim>1 else np.abs(y)
for th in (0.99,0.999): print(th, np.argmax(m>=th)/sr)
s=int(11.299*sr); print('first10ms dB',20*np.log10(m[s:s+int(.01*sr)].max()),'0.5s',20*np.log10(m[s:s+sr//2].max()),'prologue',20*np.log10(m[s:int(24.4*sr)].max()))
d=json.load(open('music_views/per_second_levels.json'));print(type(d), list(d)[:3] if isinstance(d,dict) else d[0])
