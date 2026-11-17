import numpy as np, librosa, scipy.signal as sg
D='data/video1/stems_raw/htdemucs/song/'
sr=22050
L=lambda n: librosa.load(D+n+'.wav',sr=sr,mono=True)[0]
dr,ba,ot=L('drums'),L('bass'),L('other')
db=lambda x:20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
# 1 kick shape similarity 0:20-1:00
k=sg.sosfilt(sg.butter(4,[40,120],'bp',fs=sr,output='sos'),dr)
env=np.abs(sg.hilbert(k)); pk,_=sg.find_peaks(env[:int(60*sr)],height=0.3*env[:int(60*sr)].max(),distance=int(.2*sr))
pk=pk[pk>20*sr]
seg=[dr[p-int(.005*sr):p+int(.08*sr)] for p in pk]
seg=[s/ (np.abs(s).max()+1e-9) for s in seg if len(s)==len(seg[0])]
M=np.array(seg); c=np.corrcoef(M); print('kicks',len(M),'mean pairwise waveform corr',round((c.sum()-len(M))/(len(M)**2-len(M)),3))
# kick pitch in first 60ms
f=[]
for p in pk[:60]:
    x=k[p:p+int(.06*sr)]; X=np.abs(np.fft.rfft(x*np.hanning(len(x)),8192)); fr=np.fft.rfftfreq(8192,1/sr); m=(fr>35)&(fr<130); f.append(fr[m][X[m].argmax()])
print('kick peak freq med/std',np.median(f),np.std(f))
# kick tail decay: rms 20-60ms after / 0-20
r=[db(k[p+int(.04*sr):p+int(.08*sr)])-db(k[p:p+int(.02*sr)]) for p in pk[:60]]
print('kick decay dB med/std',np.median(r),np.std(r))
# 2 sub vs kick onset at drops
for t in [121,127,133,139,145,151]:
    a=int((t-.3)*sr);b=int((t+.6)*sr)
    kb=np.abs(sg.hilbert(k[a:b])); sb=np.abs(sg.hilbert(sg.sosfilt(sg.butter(4,[35,55],'bp',fs=sr,output='sos'),ba[a:b])))
    tk=kb.argmax()/sr-.3+t; ts=(np.argmax(sb>0.5*sb.max()))/sr-.3+t
    print('drop',t,'kick-band peak',round(tk,3),'sub 50%-point',round(ts,3))
# 3 line 1:15-1:40 attack: other 200-600Hz envelope onsets
o=sg.sosfilt(sg.butter(4,[200,600],'bp',fs=sr,output='sos'),ot[int(75*sr):int(100*sr)])
e=np.abs(sg.hilbert(o)); e=sg.medfilt(e,101)
oe=librosa.onset.onset_strength(y=o,sr=sr); on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,units='time')+0
rise=[]
for t in on:
    i=int(t*sr); w=e[max(0,i-int(.05*sr)):i+int(.4*sr)]
    if len(w)<int(.4*sr): continue
    pkk=w.argmax(); rise.append(pkk/sr)
print('1:15-1:40 other onsets',len(on),'time-to-peak med',np.median(rise) if rise else None)
# 4 noise floor at edit points: min 50ms rms in each stem near edits
for t in [75.3,100.0,114.9,167.8]:
    for n,x in [('other',ot),('drums',dr),('bass',ba)]:
        w=x[int((t-1)*sr):int((t+1)*sr)]; fr=[db(w[i:i+int(.05*sr)]) for i in range(0,len(w)-int(.05*sr),int(.05*sr))]
        print(t,n,'min/med/max dB',round(min(fr),1),round(np.median(fr),1),round(max(fr),1))
