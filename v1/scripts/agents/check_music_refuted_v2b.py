import json,numpy as np,soundfile as sf
from scipy.signal import butter,sosfilt
D='/home/user/Listener/v1/data/video2/'
L={r['t']:r for r in json.load(open(D+'music_views/per_second_levels.json'))}
def m(k,a,b): return np.mean([L[t][k] for t in range(a,b) if t in L])
print('bass mean 0-28',m('bass',0,28),'28-70',m('bass',28,70))
print('drums/bass 66-92:',[(t,L[t]['drums'],L[t]['bass'],L[t]['vocals']) for t in range(66,92)])
print('drums 0-30:',[(t,L[t]['drums']) for t in range(0,30)])
print('bass 274-292:',[(t,L[t]['bass'],L[t]['dbfs'],L[t]['other']) for t in range(274,292)])
print('bass 282-292',[(t,L[t]['bass']) for t in range(280,292)])
print('vocals 205-222',[(t,L[t]['vocals'],L[t]['other'],L[t]['drums']) for t in range(205,222,2)])
x,sr=sf.read(D+'audio/song.wav'); print(x.shape,sr)
p=np.abs(x).max(1); print('n>0.999',(p>0.999).sum(), 'first',np.argmax(p>0.999)/sr)
nz=np.nonzero(p)[0]; print('last nonzero',nz[-1]/sr)
i=int(300*sr); seg=p[i:]; print('peak after 300',20*np.log10(seg.max()),(i+seg.argmax())/sr)
for a in range(0,300,20):
    print(a,round(20*np.log10(p[a*sr:(a+20)*sr].max()+1e-9),2),end='; ')
print()
# stems
def ld(n): return sf.read(D+'stems_raw/htdemucs/song/%s.wav'%n)
o,sr2=ld('other'); mm=o.mean(1)
def band(sig,lo,hi):
    return sosfilt(butter(4,[lo,hi],'bp',fs=sr2,output='sos'),sig)
# L/R corr
for (a,b) in [(5,25),(120,150),(220,250)]:
    s=[]
    for lo,hi in [(100,400),(400,1600),(1600,6000)]:
        l=band(o[a*sr2:b*sr2,0],lo,hi); r=band(o[a*sr2:b*sr2,1],lo,hi); s.append(round(np.corrcoef(l,r)[0,1],2))
    print('other LR corr',a,b,s)
# 4-10k band mix vs other
xm=x.mean(1)
for t in [180,210,220,230]:
    pass
def bp(sig,t): 
    s=band(sig[t*sr2:(t+10)*sr2],4000,10000); return round(10*np.log10(np.mean(s**2)+1e-12),1)
for t in [180,210,220,230]:
    print('4-10k',t,'mix',bp(xm,t),'other',bp(mm,t))
