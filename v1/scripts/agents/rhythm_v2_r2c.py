import json,numpy as np
C=json.load(open('/home/user/Listener/v1/data/video2/music_views/chords.json'))
prev=None;rows=[]
for c in C:
    if prev and c['chord']!=prev and c['start']>28: rows.append(c['start'])
    prev=c['chord']
for a,b in [(28,88),(88,157),(157,300)]:
    s=[x for x in rows if a<=x<b]
    print(a,b,len(s),'chord-change time mod 2s (T0=.14):',[round((x-0.14)%2,2) for x in s][:30])
