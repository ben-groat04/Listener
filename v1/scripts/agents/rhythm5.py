import numpy as np,json
D='/home/user/Listener/v1/data/t_birdwalk/'
on=np.load('/tmp/on_bass.npy')
for a,b in [(12.5,30),(30,47),(59,84),(94,120),(131,143),(155,188)]:
    o=on[(on>=a)&(on<b)]; d=np.diff(o)
    print(a,b,'IOI/eighth(0.1965):',' '.join(f'{x/0.1965:.1f}' for x in d[:28]))
# stem RMS per second
r=json.load(open(D+'stems/stem_rms_per_second.json'))
print(type(r), list(r)[:6] if isinstance(r,dict) else r[:2])
