import librosa, numpy as np
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
y,sr=librosa.load(D+'other.wav',sr=22050,mono=True)
H=2048
C=librosa.feature.chroma_cqt(y=y,sr=sr,hop_length=H,n_chroma=12,tuning=0)
t=librosa.frames_to_time(np.arange(C.shape[1]),sr=sr,hop_length=H)
N='C C# D D# E F F# G G# A A# B'.split()
def seg(a,b,show=(2,9,0,1,3,4,5,6,7,10,11)):
    m=C[:,(t>=a)&(t<b)].mean(1); m=m/m[2]; return ' '.join(f'{N[i]}{m[i]:.2f}' for i in show)
print('Q feeling: 1:40-1:55 vs 2:48-3:08')
for a,b in [(100,112),(112,115),(115,121),(168,188)]: print(a,b,seg(a,b))
print('Q sound: C in thin vs dense blocks')
for lab,a,b in [('thin 75-87',79,87),('thin 120-133',121,133),('dense 87-100',87,100),('dense 100-115',100,115),('dense 168-188',168,188),('0:40-1:00',40,60)]:
    m=C[:,(t>=a)&(t<b)].mean(1); print(lab,'C/D %.2f C#/D %.2f A/D %.2f C/A %.2f'%(m[0]/m[2],m[1]/m[2],m[9]/m[2],m[0]/m[9]))
print('Q form: 1:15-1:40 two halves, 4 bars each; bar 3.077 from 0.74')
b0=0.74;bar=3.077
for k in range(0,8):
    a=75.5+k*bar-0.0; print(k, round(a,1), seg(a,a+bar,(2,9,0,10,3,4,11)))
print('1:18.7 downbeat check: bar index',(78.7-b0)/bar, ' 1:15.5:',(75.5-b0)/bar)
print('Q form: 2:13-2:38 per-bar dominant chroma')
for k in range(0,8):
    a=133.0+k*bar; m=C[:,(t>=a)&(t<a+bar)].mean(1); top=np.argsort(-m)[:3]; print(round(a,1),[N[i] for i in top],' '.join(f'{N[i]}{m[i]/m[2]:.2f}' for i in (2,9,4,7,0)))
# loop self-similarity 133-158 at bar multiples
Cs=C[:,(t>=133)&(t<158)]
for nb in [1,2,4]:
    k=int(round(nb*bar/(H/sr)));a=Cs[:,:-k];b=Cs[:,k:]
    print('lag bars',nb,round(np.mean([np.corrcoef(a[:,i],b[:,i])[0,1] for i in range(a.shape[1])]),2))
