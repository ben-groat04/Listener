import numpy as np, soundfile as sf
D='/home/user/Listener/v1/data/t_dl_mirror/'
x,sr=sf.read(D+'stems_raw/htdemucs/song/bass.wav',always_2d=True); x=x.mean(1)
h=int(sr*0.01); n=len(x)//h; e=20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-10)
on=e>-40
# edges with gap merge 0.5s
idx=np.where(on)[0]; st=[idx[0]]; en=[]
for a,b in zip(idx[:-1],idx[1:]):
    if (b-a)>50: en.append(a); st.append(b)
en.append(idx[-1])
st=np.array(st)/100; en=np.array(en)/100
for a,b in zip(st,en): print('%.2f-%.2f (%.2f)'%(a,b,b-a),end=' | ')
print()
# verse-period short blocks: length 2.5-4.5
short=[(a,b) for a,b in zip(st,en) if 2.5<=b-a<=4.5]
s=np.array([a for a,b in short]); print('short starts',s)
k=np.round((s-s[0])/10.15)
A=np.vstack([k,np.ones_like(k)]).T; p,res,_,_=np.linalg.lstsq(A,s,rcond=None)
print('loop period %.3f s -> bar %.4f s -> %.2f BPM; resid std %.3f s'%(p[0],p[0]/4,240/(p[0]/4)/4*1,np.std(s-A@p)))
print('k',k)
print('BPM from 4-bar loop:',60*16/p[0])
e_=np.array([b for a,b in short]); k2=np.round((e_-e_[0])/10.15); A2=np.vstack([k2,np.ones_like(k2)]).T; p2=np.linalg.lstsq(A2,e_,rcond=None)[0]; print('ends period %.3f'%p2[0], 60*16/p2[0])
# hook starts from voice analysis: 10.4,71.3,132.0,193.1 -> phase in loop
for t in [10.4,71.3,132.0,193.1,215.3]: print(t,'loop phase %.2f s of %.2f'%(((t-p[1])%p[0]),p[0]))
# bass-on blocks long: starts/ends relative
