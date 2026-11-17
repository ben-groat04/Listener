import librosa,numpy as np
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050
v,_=librosa.load(D+'vocals.wav',sr=sr); o,_=librosa.load(D+'other.wav',sr=sr)
hop=256
rms=librosa.feature.rms(y=v,frame_length=1024,hop_length=hop)[0]; db=20*np.log10(rms+1e-9)
t=np.arange(len(db))*hop/sr
def bursts(a,b,th=-48,minl=0.15):
    m=(db>th)&(t>=a)&(t<b); out=[];s=None
    for i,x in enumerate(m):
        if x and s is None:s=i
        if not x and s is not None:
            if t[i]-t[s]>=minl: out.append(t[s])
            s=None
    return out
def phase(on,period=2.0,off=0.14,q=0.125):
    p=((np.array(on)-off)%period); return p
for a,b,n in [(30,160,'speech'),(208,262,'chops1'),(284,300,'chops2')]:
    on=bursts(a,b); p=phase(on)
    print(n,len(on)); print(' onsets',np.round(on,2)[:40]); print(' bar phase (s)',np.round(p,2)[:40])
    # fraction within 0.06 of a semiquaver grid and of beat
    d=np.abs(((p+0.0625)%0.125)-0.0625); print(' mean dist to 16th',round(d.mean(),3),'(chance .031)')
    db_=np.abs(((p+0.25)%0.5)-0.25); print(' mean dist to beat',round(db_.mean(),3),'(chance .125)')
# pitch checks
for a,b in [(269,276),(282,285),(250,256)]:
    f0,vf,_=librosa.pyin(v[int(a*sr):int(b*sr)],fmin=70,fmax=1400,sr=sr)
    f=f0[~np.isnan(f0)]
    print('vox',a,b,round(float(vf.mean()),2),len(f), librosa.midi_to_note(np.round(librosa.hz_to_midi(np.median(f)))) if len(f) else None, sorted(set(librosa.midi_to_note(np.round(librosa.hz_to_midi(f))))) if len(f) else '')
    f0,vf,_=librosa.pyin(o[int(a*sr):int(b*sr)],fmin=70,fmax=1400,sr=sr)
    f=f0[~np.isnan(f0)]
    print('oth',a,b,round(float(vf.mean()),2),len(f), librosa.midi_to_note(np.round(librosa.hz_to_midi(np.median(f)))) if len(f) else None)
# burst-wise stem correlation: vocal vs other levels at bursts (bleed test)
ro=20*np.log10(librosa.feature.rms(y=o,frame_length=1024,hop_length=hop)[0]+1e-9)
for a,b in [(212,260),(284,300)]:
    m=(t>=a)&(t<b); print('corr vox-other dB',a,b,round(np.corrcoef(db[m],ro[m])[0,1],2))
# spectral edges of speech vs chops
S=np.abs(librosa.stft(v,n_fft=2048))**2; fr=librosa.fft_frequencies(sr=sr,n_fft=2048); st=librosa.frames_to_time(np.arange(S.shape[1]),sr=sr,hop_length=512)
for a,b in [(64,70),(110,116),(212,220),(250,256)]:
    m=(st>=a)&(st<b); ps=S[:,m].mean(1); c=np.cumsum(ps)/ps.sum()
    print('rolloff85/95 Hz',a,b,fr[np.searchsorted(c,.85)],fr[np.searchsorted(c,.95)],'centroid',round(float((fr*ps).sum()/ps.sum())))
