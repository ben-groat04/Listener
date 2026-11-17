import numpy as np, librosa
o=np.load('/tmp/ons.npy',allow_pickle=True).item()
tb,td,to=o['b'],o['d'],o['o']
def hist(t,a,b,u=0.1965):
    s=t[(t>=a)&(t<b)]; i=np.diff(s)/u
    r=np.round(i).astype(int); r=r[(r>=1)&(r<=20)]
    return np.bincount(r,minlength=21)
for a,b in [(12,47),(60,83),(95,118),(131,143),(155,167)]:
    print('bass IOI sixteenth units',a,b,hist(tb,a,b)[1:17])
# triplet test on drums: IOIs in 0.1 - 0.3 s
for a,b in [(0,200)]:
    s=td; i=np.diff(s); i=i[(i>0.09)&(i<0.5)]
    h,e=np.histogram(i,bins=np.arange(0.09,0.5,0.02)); print('drum IOI hist',list(zip(np.round(e[:-1],2),h)))
# bass triples summing to 16 units in groove
s=tb[(tb>=12)&(tb<47)]; i=np.round(np.diff(s)/0.1965).astype(int)
print(i.tolist())
# other stem onsets during 143.5-155.7
x=to[(to>=143.5)&(to<155.7)]; print('other onsets in stop',np.round(x,2).tolist(), np.round(np.diff(x),2).tolist())
# bass gate length: time bass rms falls below -40dB after onset
y,_=librosa.load('/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/bass.wav',sr=22050)
r=librosa.feature.rms(y=y,frame_length=1024,hop_length=256)[0]; db=20*np.log10(r+1e-9); tt=np.arange(len(r))*256/22050
L=[]
for t0 in tb[(tb>=20)&(tb<45)]:
    k=int(t0*22050/256); pk=db[k:k+6].max(); j=k
    while j<len(db)-1 and db[j]>pk-20: j+=1
    L.append((j-k)*256/22050)
print('bass 20dB-decay time median',np.median(L).round(2),np.percentile(L,[10,90]).round(2))
