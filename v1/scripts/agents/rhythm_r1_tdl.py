import numpy as np, librosa, json, sys
D='/home/user/Listener/v1/data/t_dl_mirror/'
sr=22050
dr,_=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=sr,mono=True)
mix,_=librosa.load(D+'audio/song.wav',sr=sr,mono=True)
hop=256
fr=sr/hop
# tempo via drums onset envelope autocorrelation, whole track, in 3 segments
oe=librosa.onset.onset_strength(y=dr,sr=sr,hop_length=hop)
def acf(x):
    x=x-x.mean(); a=np.correlate(x,x,'full')[len(x)-1:]; return a/a[0]
for (a,b) in [(0,240),(30,70),(70,130),(130,200),(200,230)]:
    seg=oe[int(a*fr):int(b*fr)]
    ac=acf(seg); lags=np.arange(len(ac))/fr
    m=(lags>0.25)&(lags<3.2)
    idx=np.where(m)[0]
    pk=[i for i in idx[1:-1] if ac[i]>ac[i-1] and ac[i]>ac[i+1] and ac[i]>0.15]
    print(a,b,[(round(lags[i],3),round(ac[i],2)) for i in pk][:10])
# fine tempo: bar-lag estimation by sub-sample peak refine on 2.5 s
seg=oe[int(30*fr):int(215*fr)]
ac=acf(seg); lags=np.arange(len(ac))/fr
for L in [0.627,1.254,2.51,5.02,10.04]:
    w=(lags>L*0.96)&(lags<L*1.04); i=np.argmax(np.where(w,ac,-1)); print('lag near',L,round(lags[i],4),round(ac[i],3), 'bpm of beat',round(60/(lags[i]/(L/0.627)),2))
# tempo curve from tracker beats
b=np.array(json.load(open(D+'audio_features/beat_times.json')))
ioi=np.diff(b)
print('beats',len(b),'median ioi',np.median(ioi),'std',ioi.std(), 'pct within 5% of median',np.mean(abs(ioi/np.median(ioi)-1)<0.05))
for s in range(0,240,30):
    m=(b[:-1]>=s)&(b[:-1]<s+30)
    if m.sum(): print(s,'bpm',round(60/np.median(ioi[m]),2),'std ms',round(ioi[m].std()*1000,1))
# linear fit of beats to check drift
n=np.arange(len(b)); p=np.polyfit(n,b,1); print('lin fit period',p[0],'bpm',60/p[0],'resid std ms',np.std(b-np.polyval(p,n))*1000, 'max',np.max(abs(b-np.polyval(p,n)))*1000)
