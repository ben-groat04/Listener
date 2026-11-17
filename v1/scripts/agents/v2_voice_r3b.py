import librosa,numpy as np
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
v,sr=librosa.load(D+'vocals.wav',sr=22050,mono=True)
hop=256
rms=librosa.feature.rms(y=v,frame_length=1024,hop_length=hop)[0]
db=20*np.log10(rms+1e-9);t=np.arange(len(db))*hop/sr
# bursts: rising through threshold relative to local floor
def bursts(a,b,thr=-45):
    idx=np.where((t>=a)&(t<b))[0];s=db[idx];out=[];on=False
    for i,x in zip(idx,s):
        if x>thr and not on: out.append(t[i]);on=True
        elif x<thr-6: on=False
    return out
for a,b in[(208,280),(284,300)]:
    o=bursts(a,b)
    print('win',a,b,len(o))
    L=88.61
    for x in o[:60]:
        c=((x-L)%12.0);bar=((x-L)%2.0)
        print(f'{int(x//60)}:{x%60:05.2f} bar_ph={bar:.2f} cyc12_ph={c:.1f}')
# tails: decay after burst end
print('tails')
for a,b in[(208,280),(284,300)]:
    o=bursts(a,b,-40)
    for x in o[:6]:
        i=int(x*sr/hop);seg=db[i:i+int(1.2*sr/hop)];pk=seg.max();ip=seg.argmax()
        after=seg[ip:];dec=[(k*hop/sr) for k,y in enumerate(after) if y<pk-20]
        print(f'{x:.1f} peak {pk:.1f} dB, -20dB after {dec[0] if dec else None}')
