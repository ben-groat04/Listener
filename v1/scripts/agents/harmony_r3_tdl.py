import numpy as np, librosa
d='data/t_dl_mirror/stems_raw/htdemucs/song/'; sr=22050
oth=librosa.load(d+'other.wav',sr=sr,mono=True)[0]
voc=librosa.load(d+'vocals.wav',sr=sr,mono=True)[0]
bas=librosa.load(d+'bass.wav',sr=sr,mono=True)[0]
k=1.0081
def band(y,t0,t1,f):
    s=y[int(t0*sr):int(t1*sr)]; n=8192*4
    S=np.abs(np.fft.rfft(s*np.hanning(len(s)),n)); fr=np.fft.rfftfreq(n,1/sr)
    m=(fr>f*k*0.985)&(fr<f*k*1.015); return 20*np.log10(S[m].max()+1e-9)
print('bed F5(698) vs F#5(740) vs A5 880, dB; verse(0:40-1:10) / hook-nonwalk / walk windows')
for lab,(a,b) in {'verse 0:40-1:10':(40,70),'verse 2:40-3:10':(160,190),'hook1 nonwalk 0:20-0:25':(20,25),'hook4 nonwalk 3:14.5-3:18.5':(194.5,198.5),'walk 3:19.1-3:22.3':(199.1,202.3),'walk 3:28.8-3:31.9':(208.8,211.9),'outro 3:40-3:50':(220,230)}.items():
    print(lab,[round(band(oth,a,b,f),1) for f in (698.5,740,880,587.3,392)])
# voice pyin on hook4 around walks
for a,b in [(197,204),(206.5,213)]:
    f0,v,_=librosa.pyin(voc[int(a*sr):int(b*sr)],fmin=130,fmax=700,sr=sr,hop_length=1024,frame_length=4096)
    t=a+np.arange(len(f0))*1024/sr
    print('voice',a,b)
    print(' '.join(f'{x:.1f}:{librosa.hz_to_note(y/k) if y==y else "-"}' for x,y in zip(t,f0)))
# bass fundamental by 0.25s around walk
for a,b in [(198.5,203.5),(207.5,213)]:
    out=[]
    for t in np.arange(a,b,0.25):
        s=bas[int(t*sr):int((t+0.25)*sr)]; n=1<<16
        S=np.abs(np.fft.rfft(s*np.hanning(len(s)),n)); fr=np.fft.rfftfreq(n,1/sr)
        m=(fr>30)&(fr<120); out.append(f'{t:.2f}:{fr[m][S[m].argmax()]:.0f}')
    print('bass',' '.join(out))
# bass energy >100Hz vs <100Hz in hook
s=bas[int(194*sr):int(210*sr)];S=np.abs(np.fft.rfft(s))**2;fr=np.fft.rfftfreq(len(s),1/sr)
print('bass share >100Hz dB',10*np.log10(S[fr>100].sum()/S[fr<100].sum()))
