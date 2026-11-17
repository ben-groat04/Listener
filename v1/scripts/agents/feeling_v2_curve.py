import json,numpy as np
d=json.load(open('/home/user/Listener/v1/data/video2/music_views/per_second_levels.json'))
for s in range(0,len(d),20):
    w=d[s:s+20]; f=lambda k:np.mean([x[k] for x in w])
    print(f"{s//60}:{s%60:02d} mix {f('dbfs'):.1f} w {f('width'):.2f} voc {f('vocals'):.0f} dr {f('drums'):.0f} bs {f('bass'):.0f} oth {f('other'):.0f}")
print('len',len(d))
for t in [27,28,29,85,86,87,88,89,299,300,301,302,303,304]:
    print(t,d[t] if t<len(d) else None)
# 5s smoothed mix level max diff
m=np.array([x['dbfs'] for x in d]);print('range',m.min(),m.max(), 'quiet<-20 secs',(m<-20).sum())
