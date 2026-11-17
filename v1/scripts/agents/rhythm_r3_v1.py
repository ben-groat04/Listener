import numpy as np, librosa
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
y,sr=librosa.load(D+'drums.wav',sr=22050)
P=0.7692;ph=0.164
hop=64;fr=sr/hop
S=np.abs(librosa.stft(y,n_fft=1024,hop_length=hop));f=librosa.fft_frequencies(sr=sr,n_fft=1024)
def band(a,b):
    e=S[(f>=a)&(f<b)].sum(0);o=np.diff(e,prepend=0);o[o<0]=0;return o
ol,om,oh=band(30,150),band(150,2500),band(3000,10000)
g=P/4
def slot(o,k):
    c=int(round((ph+k*g)*fr));w=o[max(c-1,0):c+2];return w.max() if len(w) else 0.0
def fold(o,a,b,n=16):
    pr=np.zeros(n);c=np.zeros(n)
    for k in range(int(np.ceil((a-ph)/g)),int((b-ph)/g)):
        pr[k%n]+=slot(o,k);c[k%n]+=1
    return pr/np.maximum(c,1)
ref={k:np.percentile(o[int(3*fr):int(165*fr)],99.5) for k,o in [('l',ol),('m',om),('h',oh)]}
np.set_printoptions(precision=2,suppress=True,linewidth=200)
def pr(a,b,label):
    print(label,a,b)
    for k,o in [('l',ol),('m',om),('h',oh)]: print('  ',k,fold(o,a,b)/ref[k])
# per-bar similarity + beat accents in 2:38-2:48 and last bars
# bar start phase: beat position 2 -> beat index n with n%4==2 ; n=(t-ph)/P
def bars(a,b):
    out=[]
    n0=int(np.ceil((a-ph)/P))
    for n in range(n0,int((b-ph)/P)):
        if n%4==2: out.append(n)
    return out
print('--- bar-by-bar beat strengths (mid, beat slots) and low-thump total, bar = beat pos 2 start')
for a,b in [(150,170),(183,189.5)]:
    for n in bars(a,b):
        t0=ph+n*P
        mids=[slot(om,4*(n+j))/ref['m'] for j in range(4)]
        lows=sum(slot(ol,4*n+i) for i in range(16))/ref['l']
        his=sum(slot(oh,4*n+i) for i in range(16))/ref['h']
        print('bar@%d:%05.2f mid beats %s low_sum %.1f hi_sum %.1f'%(t0//60,t0%60,np.round(mids,2),lows,his))
# click spectral centroid on beats: 0:05-0:32 vs 0:34-1:00 vs 2:50-3:05
def click_centroid(a,b):
    cs=[];ws=[]
    for n in range(int(np.ceil((a-ph)/P)),int((b-ph)/P)):
        c=int((ph+n*P)*sr); seg=y[c:c+int(0.03*sr)]
        if len(seg)<600: continue
        sp=np.abs(np.fft.rfft(seg*np.hanning(len(seg)),2048))**2;ff=np.fft.rfftfreq(2048,1/sr)
        m=ff>150;cs.append((sp[m]*ff[m]).sum()/sp[m].sum());ws.append(sp[m].sum())
    return np.median(cs),len(cs)
for a,b in [(5,32),(34,60),(120,160),(170,185)]: print('click centroid',a,b,click_centroid(a,b))
# third-beat accent: mid band strength at beat pos 0..3 relative to bar-phase (n%4)
def beatpos(a,b):
    v=np.zeros(4);c=np.zeros(4)
    for n in range(int(np.ceil((a-ph)/P)),int((b-ph)/P)):
        v[n%4]+=slot(om,4*n)/ref['m'];c[n%4]+=1
    return v/c
for a,b in [(33,66),(66,108),(120,168),(170,187)]: print('mid by beat-pos n%4',a,b,beatpos(a,b))
# drum stem dB around 3:06 roll and 2:47
env=20*np.log10(np.sqrt(np.convolve(y**2,np.ones(int(.02*sr))/int(.02*sr),'same'))+1e-9)
for t0 in [166.5,166.9,167.3,167.7,168.0,168.25,168.6]: print('drum dB %.2f %.1f'%(t0,env[int(t0*sr)]))
# onsets 185-189 times
on=librosa.onset.onset_detect(onset_envelope=ol+om+oh,sr=sr,hop_length=hop,units='time',backtrack=False)
print('onsets 185.5-188.8',np.round(on[(on>185.5)&(on<188.8)],2))
pr(33,108,'main');pr(108,115,'swell');pr(168,188,'final');pr(0,32,'intro')
