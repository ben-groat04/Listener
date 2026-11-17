import json,numpy as np,librosa
D='/home/user/Listener/v1/data/t_cshells_cshore/'
R=D+'stems_raw/htdemucs/song/'
names=['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
# 1 third test: other stem, narrow-band ratio of C (3rd harm region) vs C# using high-res CQT, per section, in dB re A
y,sr=librosa.load(R+'other.wav',sr=22050)
for a,b in [(25,32),(65,100),(100,140),(140,200),(200,240),(240,280),(280,320),(325,340)]:
    seg=y[int(a*sr):int(b*sr)]
    C=np.abs(librosa.cqt(seg,sr=sr,fmin=librosa.note_to_hz('A1'),n_bins=36*5,bins_per_octave=36))**2
    m=C.mean(1)
    def pk(semi_from_A,octs=(1,2,3,4)):
        v=0
        for o in octs:
            k=int(round((semi_from_A+12*o)*3))
            if k+2<len(m): v+=m[k-1:k+2].max()
        return v
    A=pk(0);print('other',a,b,'dB re A: '+' '.join(f'{n}:{10*np.log10(pk(i)/A+1e-12):.0f}' for i,n in enumerate(names) if n in('C','C#','E','G','G#','F','F#','D','B')))
# 2 bass pitch class counts via pyin per section
yb,sb=librosa.load(R+'bass.wav',sr=22050)
for a,b in [(120,140),(140,160),(160,180),(180,200),(200,225),(225,240),(240,252),(252,280),(300,322)]:
    seg=yb[int(a*sb):int(b*sb)]
    f,v,p=librosa.pyin(seg,fmin=35,fmax=300,sr=sb,frame_length=2048)
    m=~np.isnan(f)&(p>0.5)
    if m.sum()<10: print('bass',a,b,'few');continue
    # cents relative to A
    c=1200*np.log2(f[m]/55.0)
    pc=np.round(c/100).astype(int)%12
    cnt=np.bincount(pc,minlength=12)
    print('bass',a,b,m.sum(),' '.join(f'{names[i]}:{cnt[i]}' for i in np.argsort(-cnt)[:5]),'median offset cents from nearest semitone',round(np.median(c-np.round(c/100)*100)))
# 3 stab attacks vs chord change: other onsets 60-120 and chord.json changes
ch=json.load(open(D+'music_views/chords.json'))
seg=y[60*sr:120*sr]
on=librosa.onset.onset_detect(y=seg,sr=sr,units='time',backtrack=False,delta=0.3)+60
oenv=librosa.onset.onset_strength(y=seg,sr=sr)
print('stab onsets',np.round(on,1)[:30])
cc=[c['start'] for c in ch if 60<=c['start']<=120]
print('chord changes 60-120',np.round(cc,1))
d=[min(abs(x-o) for o in on) for x in cc]
print('chord changes within 0.15s of an other-onset',sum(1 for x in d if x<0.15),'of',len(d),'median dist',np.median(d))
# 4 section 3:20-3:45 vs 4:00-4:40 chord stats
for a,b in [(200,225),(240,280)]:
    import collections
    s=collections.Counter()
    for c in ch:
        o=min(c['end'],b)-max(c['start'],a)
        if o>0:s[c['chord']]+=o
    t=sum(s.values());print(a,b,[(k,round(v/t*100)) for k,v in s.most_common(6)],'n changes',sum(1 for c in ch if a<=c['start']<b))
