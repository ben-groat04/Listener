import json,numpy as np,sys
d=json.load(open('/home/user/Listener/v1/data/video2/music_views/per_second_levels.json'))
t=np.array([x['t'] for x in d]);db=np.array([x['dbfs'] for x in d]);w=np.array([x['width'] for x in d])
dr=np.array([x['drums'] for x in d]);ba=np.array([x['bass'] for x in d]);vo=np.array([x['vocals'] for x in d]);ot=np.array([x['other'] for x in d])
def m(a,b,x):return x[(t>=a)&(t<b)].mean()
print('30s blocks: start dbfs width drums bass other; voice-active share (>-45)')
for a in range(0,306,20):
    s=(t>=a)&(t<a+20)
    print(f'{a//60}:{a%60:02d} {db[s].mean():6.1f} {w[s].mean():.2f} {dr[s].mean():6.1f} {ba[s].mean():6.1f} {ot[s].mean():6.1f} voice {np.mean(vo[s]>-45):.2f}')
# voice-active seconds
v=t[vo>-45];print('voice secs',len(v),'first',v.min(),'last',v.max())
# biggest 1s jumps in dbfs
j=np.diff(db);i=np.argsort(-np.abs(j))[:10]
print('largest 1s steps',[(int(t[k+1]),round(float(j[k]),1)) for k in sorted(i)])
# dynamic range
print('quietest/loudest 10s', min(db[k:k+10].mean() for k in range(len(db)-10)), max(db[k:k+10].mean() for k in range(len(db)-10)))
# longest gap between voice
gaps=np.diff(v);k=np.argsort(-gaps)[:4];print('longest voice gaps',[(int(v[x]),int(v[x+1])) for x in k])
