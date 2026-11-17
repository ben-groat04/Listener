import json,numpy as np
D='/home/user/Listener/v1/data/t_birdwalk/'
b=np.array(json.load(open(D+'audio_features/beat_times.json')))
ib=np.diff(b)
print('beats',len(b),'median ibi',np.median(ib),'bpm',60/np.median(ib))
for a in range(0,188,20):
    m=(b[:-1]>=a)&(b[:-1]<a+20)
    print(a,round(60/np.median(ib[m]),1),round(ib[m].std(),3))
for s in ['drums','bass']:
    on=np.load(f'/tmp/on_{s}.npy')
    print(s)
    for a in [0,12,30,50,75,100,125,140,150,165]:
        o=on[(on>=a)&(on<a+12)]
        print(' ',a,[round(x,2) for x in o][:30])
    d=np.diff(on)
    print(' IOI hist (s) 0.1 bins:',np.histogram(d,bins=np.arange(0,2.6,0.1))[0])
