import numpy as np,librosa
D='stems_raw/htdemucs/song/'
hop=0.1
def rms(n):
    y,sr=librosa.load(D+n+'.wav',sr=22050);h=int(hop*sr)
    r=np.sqrt((y[:len(y)//h*h].reshape(-1,h)**2).mean(1));return 20*np.log10(r+1e-9)
R={n:rms(n) for n in ['drums','bass','vocals','other']}
np.save('/tmp/claude-0/r.npy',R,allow_pickle=True)
def span(n,a,b,th):
    x=R[n][int(a/hop):int(b/hop)];lo=np.where(x<th)[0]
    return a+lo[0]*hop if len(lo) else None, a+lo[-1]*hop if len(lo) else None
print('bass<-50 in 60-90',span('bass',60,92,-50))
print('drums<-45 in 66-90',span('drums',66,92,-45))
# bass hole 4:30-4:50
x=R['bass'];
for a,b in [(270,285),(295,301)]:
    print('bass',a,[ (round(a+i*hop,1)) for i in np.where(x[int(a/hop):int(b/hop)]<-45)[0]][:3],'..')
print('bass<-45 in 275-282', [round(275+i*hop,1) for i in np.where(x[2750:2820]<-45)[0]][::1][:40])
