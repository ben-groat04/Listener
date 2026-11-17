import numpy as np, soundfile as sf, scipy.signal as ss, json
D='/home/user/Listener/v1/data/video1/'
x,sr=sf.read(D+'stems_raw/htdemucs/song/drums.wav');x=x.mean(1)
bt=np.array(json.load(open(D+'audio_features/beat_times.json')))
def band(lo,hi):
    sos=ss.butter(4,[lo,hi],'bp',fs=sr,output='sos');return ss.sosfilt(sos,x)
hb=band(2000,8000); lb=band(40,200)
def db(s):return 20*np.log10(np.sqrt(np.mean(s**2))+1e-9)
# per-beat: energy in 40ms after beat in hi band (click) and low band
print('beat, hi dB(0-50ms), low dB(0-100ms) for beats 2:30-2:48')
for b in bt:
    if 150<=b<=168:
        print(round(b,2), round(db(hb[int(b*sr):int((b+0.05)*sr)]),1), round(db(lb[int(b*sr):int((b+0.1)*sr)]),1))
