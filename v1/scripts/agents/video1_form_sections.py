import json,sys
import numpy as np
d=json.load(open('/home/user/Listener/v1/data/video1/music_views/per_second_levels.json'))
secs=[(0,10),(10,32),(32,41),(41,58),(58,75),(75,87),(87,100),(100,115),(115,118),(118,134),(134,154),(154,168),(168,188)]
secs=[(0,9),(9,32),(32,50),(50,75),(75,87),(87,100),(100,115),(115,121),(121,133),(133,158),(158,168),(168,189)]
for a,b in secs:
    r=[x for x in d if a<=x['t']<b]
    f=lambda k:np.mean([x[k] for x in r])
    bon=np.mean([x['bass']>-40 for x in r])
    von=np.mean([x['vocals']>-40 for x in r])
    print(f"{a//60}:{a%60:02d}-{b//60}:{b%60:02d} mix{f('dbfs'):6.1f} w{f('width'):.2f} oth{f('other'):6.1f} drm{f('drums'):6.1f} bass_on{bon:.2f} voice_on{von:.2f}")
mix=np.array([x['dbfs'] for x in d]);t=np.array([x['t'] for x in d])
dm=np.diff(mix)
for i in np.argsort(-np.abs(dm))[:10]: print('jump',t[i]+1,round(dm[i],1))
