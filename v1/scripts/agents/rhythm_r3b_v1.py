import numpy as np, librosa
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
y,sr=librosa.load(D+'drums.wav',sr=22050)
b,_=librosa.load(D+'bass.wav',sr=22050)
def env(x,w=0.05): return 20*np.log10(np.sqrt(np.convolve(x**2,np.ones(int(w*sr))/int(w*sr),'same'))+1e-9)
ed,eb=env(y),env(b)
def seg(a,bb,step=0.25):
    for t in np.arange(a,bb,step):
        i=int(t*sr); print('%d:%05.2f drum max/0.25s %.1f  bass %.1f'%(t//60,t%60,ed[i:i+int(step*sr)].max(),eb[i:i+int(step*sr)].max()))
seg(155,163);print();seg(186.0,189.0)
# drum peak level per beat across 2:30-2:48
ph=0.164;P=0.7692
print([ (round(ph+n*P,1), round(float(ed[int((ph+n*P)*sr):int((ph+n*P)*sr)+int(0.1*sr)].max()),0)) for n in range(int(150/P),int(168/P))])
