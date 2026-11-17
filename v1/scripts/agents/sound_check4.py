import numpy as np, soundfile as sf, scipy.signal as ss, librosa
D='/home/user/Listener/v1/data/t_cshells_cshore/'
s,sr=sf.read(D+'stems_raw/htdemucs/song/drums.wav'); dr=s.mean(1)
sos=ss.butter(4,[35,120],'bp',fs=sr,output='sos'); lo=ss.sosfiltfilt(sos,dr)
for a,b in [(130,160),(250,300)]:
    seg=lo[a*sr:b*sr]; env=np.sqrt(np.convolve(seg**2,np.ones(441)/441,'same'))
    pk,pr=ss.find_peaks(env,height=np.percentile(env,90),distance=int(0.12*sr)); t=pk/sr+a
    ioi=np.diff(t); print(a,b,'n',len(t),'IOI hist (0.05 bins):')
    h,e=np.histogram(ioi,bins=np.arange(0,1.3,0.05)); print([ (round(e[i],2),int(h[i])) for i in range(len(h)) if h[i]>2])
    # autocorr of env for tempo
    ee=env[::441]; ee=ee-ee.mean(); ac=np.correlate(ee,ee,'full')[len(ee)-1:]; ac/=ac[0]
    lag=np.arange(len(ac))*0.01; sel=(lag>0.3)&(lag<1.2); i=np.argmax(ac[sel]); print('drum low-band autocorr peak lag',lag[sel][i],'=>',60/lag[sel][i],'BPM')
    # deviation from tempo grid using peaks near multiples of 0.2438
    T=60/123.0
    for ph_t in [T/2]:
        gd=(((t-t[0]+ph_t/2)%ph_t)-ph_t/2)*1000
        print('dev from 8th grid (period %.0f ms) after phase at first hit: mean|dev| %.1f ms sd %.1f; random expectation mean|dev| %.0f'%(ph_t*1000,np.abs(gd).mean(),gd.std(),ph_t*250))
