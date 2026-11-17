import librosa,numpy as np
y,sr=librosa.load('/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/vocals.wav',sr=22050)
S=np.abs(librosa.stft(y,n_fft=2048))**2
fr=librosa.fft_frequencies(sr=sr,n_fft=2048);hop=512
def band(a,b,lo,hi):
    i=int(a*sr/hop);j=int(b*sr/hop);m=(fr>=lo)&(fr<hi)
    return 10*np.log10(S[m][:,i:j].sum(0).mean()+1e-12)
for a,b in [(20,26),(28,31.7),(135,141),(143,146),(164,168),(79,86),(63,66),(155,158)]:
    print(a,b,[round(band(a,b,lo,hi),1) for lo,hi in [(100,500),(500,2000),(2000,5000),(5000,8000)]])
# 4kHz limited?
tot=S[:,int(20*sr/hop):int(31*sr/hop)].sum(1);c=np.cumsum(tot)/tot.sum()
print('rolloff 95%',fr[np.searchsorted(c,.95)],'99%',fr[np.searchsorted(c,.99)])
