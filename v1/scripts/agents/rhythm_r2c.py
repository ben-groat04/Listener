import numpy as np, librosa
exec(open('rhythm_r2.py').read().split('# fit grid')[0])
P=0.1923; ph=0.16
def slot(tm): 
    x=(tm-ph)/P; return x, int(round(x))%32, (x-round(x))*P
# bass onsets 2:00-2:35 using rms at hop
rms=librosa.feature.rms(y=bs,frame_length=2048,hop_length=hop)[0]
db=20*np.log10(rms+1e-9); tt=np.arange(len(db))/fr
print('sub hit onsets (rise above -45 dB after silence):')
prev=False; hits=[]
for i in range(len(db)):
    on=db[i]>-38
    if on and not prev and 118<tt[i]<160: hits.append(tt[i])
    prev=on
for h in hits: print(round(h,3), [round(v,2) if isinstance(v,float) else v for v in slot(h)])
# events
ev={'1:15.3 bass out':75.3,'1:27.4 wall':87.4,'1:40.0 bass in':100.0,'1:55.5 bass out':115.5,'2:14 reignite':134.0,'2:38.4':158.4,'2:47.8 stop start':167.8,'2:48.2 stop end':168.2,'0:00.7 hit':0.7,'0:31.7 voice off':31.7}
for k,v in ev.items(): print(k, [round(x,2) if isinstance(x,float) else x for x in slot(v)])
