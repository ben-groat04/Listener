import numpy as np,librosa
d='data/t_birdwalk/stems_raw/htdemucs/song'
sr=22050
V,_=librosa.load(f'{d}/vocals.wav',sr=sr);O,_=librosa.load(f'{d}/other.wav',sr=sr)
def mel(y):
    return librosa.power_to_db(librosa.feature.melspectrogram(y=y,sr=sr,n_fft=2048,hop_length=512,n_mels=64))
hop=512/sr
for nm,y in(('vocals',V),('other',O)):
    M=mel(y)
    def seg(t0,L): return M[:,int(t0/hop):int((t0+L)/hop)]
    def c(a,b):
        n=min(a.shape[1],b.shape[1]);a=a[:,:n].ravel();b=b[:,:n].ravel();return np.corrcoef(a,b)[0,1]
    print(nm)
    # for each 6 s block 0:12..3:00, best earlier/later match lag (multiples search 11-13 s) 
    for t0 in np.arange(12,170,6):
        best=max(((c(seg(t0,6),seg(t0-lag,6)),lag) for lag in np.arange(11.0,13.01,0.1) if t0-lag>=0),default=None)
        print(f"{int(t0//60)}:{t0%60:04.1f} best lag-back {best[1]:.1f}s r={best[0]:.2f}" if best else '')
# edges grid residual
edges={'bass on 0:12.4':12.4,'off 0:47.2':47.2,'on 0:59.3':59.3,'off 1:59.2':119.2,'on 2:11.3':131.3,'on 2:23.5 off? ':143.5,'on 2:35.7':155.7,'voice off 2:47.5':167.5,'voice on 2:57.1':177.1}
for k,v in edges.items(): print(k, round((v-12.4)/12.0,2))
