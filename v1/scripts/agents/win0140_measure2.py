import librosa, numpy as np
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
sr=22050
b=librosa.load(D+'bass.wav',sr=sr,offset=140,duration=4)[0]
S=np.abs(librosa.stft(b,n_fft=8192,hop_length=512))
fr=librosa.fft_frequencies(sr=sr,n_fft=8192)
m=(fr>25)&(fr<300)
pk=fr[m][S[m].argmax(0)]; print('bass peak freq 140-144',np.round(np.percentile(pk,[10,50,90]),1))
b=librosa.load(D+'bass.wav',sr=sr,offset=156,duration=4)[0]
S=np.abs(librosa.stft(b,n_fft=8192,hop_length=512));pk=fr[m][S[m].argmax(0)];print('bass 156-160',np.round(np.percentile(pk,[10,50,90]),1))
v=librosa.load(D+'vocals.wav',sr=sr,offset=140,duration=20)[0]
on=librosa.onset.onset_detect(y=v,sr=sr,hop_length=256,units='time')+140
seg=on[(on>144)&(on<155)];print('vocal onsets 144-155',np.round(seg,2));print('IOI median',np.median(np.diff(seg)))
# stereo width of full mix by segment
import soundfile as sf
x,s=sf.read('/home/user/Listener/v1/data/t_birdwalk/audio/song.wav');print(x.shape,s)
for a,bb in[(140,143.4),(144,155),(156,160)]:
    seg=x[int(a*s):int(bb*s)]; M=(seg[:,0]+seg[:,1])/2;Sd=(seg[:,0]-seg[:,1])/2
    print(a,'side/mid dB',round(20*np.log10(np.sqrt((Sd**2).mean())/np.sqrt((M**2).mean())),1),'peak',round(20*np.log10(np.abs(seg).max()),2))
