import numpy as np, soundfile as sf
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
x,sr=sf.read(D+'other.wav');x=x.mean(1)
def bd(a,b,lo,hi):
    s=x[int(a*sr):int(b*sr)];F=np.abs(np.fft.rfft(s*np.hanning(len(s))))**2;f=np.fft.rfftfreq(len(s),1/sr)
    m=(f>=lo)&(f<hi);return 10*np.log10(F[m].sum()+1e-12)-10*np.log10(len(s))
for name,(a,b),(c,d) in [('1:27 wall vs 1:15-1:27',(76,86),(89,99)),('2:13 vs 2:00-2:12',(121,132),(135,146))]:
    for lo,hi in [(100,500),(500,2000),(2000,5000),(5000,10000)]:
        print(name,lo,hi,round(bd(c,d,lo,hi)-bd(a,b,lo,hi),1))
# width at 3:05-> mid/side of other at 1:30 and 2:50
y,sr2=sf.read(D+'other.wav')
for a,b in [(90,100),(170,180)]:
    s=y[int(a*sr):int(b*sr)];m=(s[:,0]+s[:,1])/2;sd=(s[:,0]-s[:,1])/2
    print(a,'side-mid dB',round(20*np.log10(np.sqrt((sd**2).mean())/np.sqrt((m**2).mean())),1))
