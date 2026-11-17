import numpy as np, soundfile as sf
D='/home/user/Listener/v1/data/t_cshells_cshore/'
def ld(p):
    x,sr=sf.read(p); 
    return (x.mean(1) if x.ndim>1 else x),sr
mix,sr=ld(D+'audio/song.wav')
st={k:ld(D+f'stems_raw/htdemucs/song/{k}.wav')[0] for k in ['vocals','other']}
def db(x): return 10*np.log10(np.mean(x**2)+1e-20)
print('sr',sr)
for a in range(326,343,2):
    s=slice(int(a*sr),int((a+2)*sr))
    print(a, 'mix %.1f other %.1f vocals %.1f voc-other %.1f'%(db(mix[s]),db(st['other'][s]),db(st['vocals'][s]),db(st['vocals'][s])-db(st['other'][s])))
print('2:20-2:30')
for a in range(140,150,2):
    s=slice(int(a*sr),int((a+2)*sr))
    print(a,'mix %.1f voc %.1f voc-mix %.1f'%(db(mix[s]),db(st['vocals'][s]),db(st['vocals'][s])-db(mix[s])))
# end step in 10ms envelope
e=np.array([db(mix[i:i+int(.01*sr)]) for i in range(int(342.4*sr),int(343.1*sr),int(.01*sr))])
print(np.round(e,0))
# modulation rate of murmur (syllable) 5:31-5:41 voc env
v=st['vocals'][int(331*sr):int(341*sr)]
h=int(.02*sr); env=np.sqrt(np.convolve(v**2,np.ones(h)/h,'same'))[::h]
env=env-env.mean(); f=np.fft.rfftfreq(len(env),.02); P=abs(np.fft.rfft(env))
m=(f>0.5)&(f<12); print('mod peak Hz',f[m][P[m].argmax()])
