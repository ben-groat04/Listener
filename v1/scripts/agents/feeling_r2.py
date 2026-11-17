import json,numpy as np
d=json.load(open('/home/user/Listener/v1/data/video1/music_views/per_second_levels.json'))
g=lambda k:np.array([x[k] for x in d],float)
mix,w,b,o,dr=g('dbfs'),g('width'),g('bass'),g('other'),g('drums')
ev={'1:15 bass out':75,'1:27 widen':87,'1:40 bass slam':100,'1:55 collapse':115,'2:00 thin block':120,'2:38 lock':158,'2:48 gasp/bright':168,'3:08 cut':188}
def m(a,t0,t1):return np.mean(a[max(t0,0):t1])
print('event | d mix dB | d width | d bass dB | d other dB (4s after vs 4s before)')
for k,t in ev.items():
  t=min(t,len(d)-4)
  print(k,'|',round(m(mix,t,t+4)-m(mix,t-4,t),1),'|',round(m(w,t,t+4)-m(w,t-4,t),2),'|',round(m(np.maximum(b,-70),t,t+4)-m(np.maximum(b,-70),t-4,t),1),'|',round(m(o,t,t+4)-m(o,t-4,t),1))
print('mix P10,P90',np.percentile(mix,[10,90]),'width P10,P90',np.percentile(w,[10,90]))
