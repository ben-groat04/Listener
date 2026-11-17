import json,numpy as np,librosa
y,sr=librosa.load('audio/song.wav',sr=None,mono=True)
def rms(x,a,b,w=0.1):
    out=[]
    t=a
    while t<b:
        s=x[int(t*sr):int((t+w)*sr)]
        out.append((round(t,1),round(20*np.log10(np.sqrt(np.mean(s**2))+1e-9),1)));t+=w
    return out
print('2:47.4-2:48.4',rms(y,167.4,168.4))
print('3:07.6-3:08.7',rms(y,187.6,188.7))
d,_=librosa.load('stems_raw/htdemucs/song/drums.wav',sr=sr,mono=True)
print('drum 2:47.4',rms(d,167.4,168.4))
print('drum 3:07.6',rms(d,187.6,188.4))
ch=json.load(open('music_views/chords.json'))
print(type(ch), (list(ch.items())[:2] if isinstance(ch,dict) else ch[:3]))
L=json.load(open('music_views/per_second_levels.json'))
print(type(L), (list(L.items())[:1] if isinstance(L,dict) else L[:1]))
