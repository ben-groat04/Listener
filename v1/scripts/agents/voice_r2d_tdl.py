import numpy as np, librosa
D='/home/user/Listener/v1/data/t_dl_mirror/'
sr=22050
v,_=librosa.load(D+'stems_raw/htdemucs/song/vocals.wav',sr=sr,mono=True)
hop=110 # 5ms
n=len(v)//hop; e=20*np.log10(np.sqrt((v[:n*hop].reshape(n,hop)**2).mean(1))+1e-9)
gaps=[(10.94,12.29),(13.44,14.48),(23.56,24.83),(71.89,72.96),(84.38,85.59),(132.81,133.91),(145.35,146.49),(193.33,194.65),(206.04,207.3)]
for a,b in gaps:
    i=int(a/0.005); j=int(b/0.005)
    # fall: from level 100ms before a (max) to first frame below -50
    pre=e[i-20:i].max(); 
    k=i-20+np.argmax(e[i-20:i+20]<pre-30) if (e[i-20:i+20]<pre-30).any() else None
    fall=(k-(i-20+np.argmax(e[i-20:i+20]))) *5 if k else None
    post=e[j:j+30].max(); r=j-10+np.argmax(e[j-10:j+30]>post-30)
    print(f'gap {a}-{b}: pre {pre:.0f} dB, 30 dB fall time ms {fall}, floor in gap {e[i+10:j-10].mean():.0f} dB, rise 30 dB from {e[j-10]:.0f} -> {post:.0f} within ms {(r-(j-10))*5}')
