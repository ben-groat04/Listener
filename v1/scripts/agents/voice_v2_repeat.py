import numpy as np, librosa, json
y,sr=librosa.load('data/video2/stems_raw/htdemucs/song/vocals.wav',sr=16000)
M=librosa.power_to_db(librosa.feature.melspectrogram(y=y,sr=sr,n_mels=40,hop_length=160,n_fft=800),ref=np.max)
def seg(t0,L=0.8):
    a=int(t0*100);return M[:,a:a+int(L*100)]
def sim(a,b):
    a=a-a.mean(1,keepdims=True)*0; 
    a=a.flatten();b=b.flatten();return np.corrcoef(a,b)[0,1]
ts=[280.6,282.5,284.5,286.6,288.6,290.6,292.6,294.6,296.6,298.65]
print('4:40-5:00 burst similarity matrix')
S=np.array([[sim(seg(a),seg(b)) for b in ts] for a in ts]);print(np.round(S,2))
# compare early speech bursts to confirm baseline: different words
ts2=[42.6,51.2,59.1,64.5,80.0]
print(np.round(np.array([[sim(seg(a),seg(b)) for b in ts2] for a in ts2]),2))
# beat alignment
b=json.load(open('data/video2/audio_features/beat_times.json'))
b=np.array(b if isinstance(b,list) else b.get('beat_times',b.get('beats')))
for t in [280.6,282.5,284.5,286.6,288.6,290.6,292.6,294.6,296.6,298.65,208.6,212.4,216.4,218.6,220.5,224.6]:
    d=t-b[np.argmin(abs(b-t))];print(t,round(d,3),end=' | ')
print(); print('beat spacing',np.median(np.diff(b[(b>270)&(b<300)])))
