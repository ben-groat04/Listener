import numpy as np, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'
sr=22050
def load(n): return librosa.load(D+'stems_raw/htdemucs/song/%s.wav'%n,sr=sr,mono=True)[0]
dr=load('drums'); ot=load('other')
bar=2.554
def best(x,t0,L,lagr=0.08):
    a=x[int(t0*sr):int((t0+L)*sr)]
    L0=int(lagr*sr); out=[]
    for rep in (bar,2*bar,4*bar):
        s=int((t0+rep)*sr)
        seg=x[s-L0:s+len(a)+L0]
        if len(seg)<len(a)+2*L0: return None
        c=ss.fftconvolve(seg,a[::-1],'valid'); 
        # normalised
        cs=np.sqrt(np.convolve(seg**2,np.ones(len(a)),'valid'))*np.linalg.norm(a)+1e-12
        r=c/cs; i=np.argmax(r); out.append((round(float(r[i]),2),round((i-L0)/sr*1000,1)))
    return out
for name,x in (('drums',dr),('other',ot)):
    print(name)
    for t0 in (40,60,100,120,150,170,200):
        print(' ',t0,'1,2,4-bar best normalised xcorr (r, lag ms):',best(x,t0,bar))
# envelope-level: drum hi band (2-9k) magnitude env at 5ms; correlate bar to bar
S=np.abs(librosa.stft(dr,n_fft=512,hop_length=110)); f=librosa.fft_frequencies(sr=sr,n_fft=512)
e=S[(f>2000)&(f<9000)].sum(0); fr=sr/110
n=int(bar*fr)
rs=[]
for t0 in np.arange(30,200,bar):
    a=e[int(t0*fr):int(t0*fr)+n]; b=e[int((t0+bar)*fr):int((t0+bar)*fr)+n]
    if len(a)==n and len(b)==n: rs.append(np.corrcoef(a,b)[0,1])
print('hi-band drum env adjacent-bar corr: mean %.2f median %.2f min %.2f max %.2f n %d'%(np.mean(rs),np.median(rs),min(rs),max(rs),len(rs)))
# do the same with 4-bar spacing
rs=[]
for t0 in np.arange(30,200,bar):
    a=e[int(t0*fr):int(t0*fr)+n]; b=e[int((t0+4*bar)*fr):int((t0+4*bar)*fr)+n]
    if len(a)==n and len(b)==n: rs.append(np.corrcoef(a,b)[0,1])
print('4-bar spacing: mean %.2f'%np.mean(rs))
