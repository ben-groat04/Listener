import librosa,numpy as np
D='/home/user/Listener/v1/data/video2/'
def bands(path,sr=22050):
    y,sr=librosa.load(path,sr=sr,mono=True)
    S=np.abs(librosa.stft(y,n_fft=2048,hop_length=512))**2
    f=librosa.fft_frequencies(sr=sr,n_fft=2048)
    fr=sr/512
    out={}
    for n,(a,b) in {'body':(60,500),'mid':(1000,2000),'hi2':(2000,4000),'top':(4000,8000)}.items():
        m=(f>=a)&(f<b); out[n]=10*np.log10(S[m].sum(0)+1e-12)
    return out,fr
mix,fr=bands(D+'audio/song.wav'); oth,_=bands(D+'stems_raw/htdemucs/song/other.wav')
def avg(o,k,a,b): return np.mean(o[k][int(a*fr):int(b*fr)])
if __name__=='__main__':
    print('mix top 0:38..0:46 per 0.5s', [round(float(mix['top'][int(t*fr)]),0) for t in np.arange(38,46,0.5)])
    print('other top at 0:42', [round(float(oth['top'][int(t*fr)]),0) for t in np.arange(38,46,0.5)])
    for a in range(0,300,12):
        print(f"{a//60}:{a%60:02d}", ' '.join(f"{k}{avg(oth,k,a,a+12):.0f}" for k in oth),' mixtop',round(avg(mix,'top',a,a+12)))
