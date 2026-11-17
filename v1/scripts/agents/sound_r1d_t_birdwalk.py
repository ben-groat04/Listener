import numpy as np, soundfile as sf
D='data/t_birdwalk/'; S=D+'stems_raw/htdemucs/song/'; sr=44100
st={n:soundfile.mean(1) if False else sf.read(S+n+'.wav')[0].mean(1) for n in ['drums','bass','vocals','other']}
mix=sf.read(D+'audio/song.wav')[0].mean(1)
def db(s,a,b): return 20*np.log10(np.sqrt((s[int(a*sr):int(b*sr)]**2).mean())+1e-9)
B=[('0:00.8',0.8),('0:12.1',12.1),('0:23.9',23.9),('0:46.9',46.9),('0:59.4',59.4),('1:10.5',70.5),('1:23.0',83.0),('1:33.1',93.1),('1:41.3',101.3),('1:46.0',106.0),('1:58.7',118.7),('2:11.4',131.4),('2:15.0',135.0),('2:23.4',143.4),('2:35.7',155.7),('2:47.3',167.3),('2:50.3',170.3),('2:56.5',176.5),('3:01.5',181.5)]
print('boundary | drums | bass | vocals | other | mix (dB, 1.0 s before -> 1.0 s after, 0.1 s guard)')
for l,t in B:
    r=[]
    for n in ['drums','bass','vocals','other']:
        a=db(st[n],max(t-1.1,0),t-0.1); b=db(st[n],t+0.1,t+1.1); r.append('%.1f->%.1f (%+.1f)'%(a,b,b-a))
    a=db(mix,max(t-1.1,0),t-0.1); b=db(mix,t+0.1,t+1.1); r.append('%.1f->%.1f (%+.1f)'%(a,b,b-a))
    print(l,'|',' | '.join(r))
