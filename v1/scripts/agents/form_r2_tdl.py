import numpy as np, soundfile as sf
D='/home/user/Listener/v1/data/t_dl_mirror/'
def load(p):
    x,sr=sf.read(p,always_2d=True); return x.mean(1),sr
S={}
for n,p in [('mix',D+'audio/song.wav')]+[(k,D+'stems_raw/htdemucs/song/%s.wav'%k) for k in ['drums','bass','vocals','other']]:
    x,sr=load(p); h=int(sr*0.01); n10=len(x)//h
    r=np.sqrt((x[:n10*h].reshape(n10,h)**2).mean(1)+1e-20); S[n]=20*np.log10(r+1e-10)
def m(n,a,b):
    e=S[n][int(a*100):int(b*100)]; return 20*np.log10(np.sqrt(np.mean(10**(e/10)))+1e-12)  # rms of 10ms rms
def spans(n,th=-40,gap=0.8,minl=2):
    on=S[n]>th; out=[];s=None;t=0
    idx=np.where(on)[0]
    if len(idx)==0:return out
    st=idx[0];pv=idx[0]
    for i in idx[1:]:
        if (i-pv)/100>gap: out.append((st/100,pv/100)); st=i
        pv=i
    out.append((st/100,pv/100)); return [(a,b) for a,b in out if b-a>=minl]
print('VOCAL spans',[(round(a,1),round(b,1)) for a,b in spans('vocals',-45,1.6,2)])
B=[('0:10.4',10.4),('0:30.4',30.4),('1:11.3',71.3),('1:31.4',91.4),('2:12.0',132.0),('2:14.0',134.0),('2:32.4',152.4),('2:34',154),('3:13.1',193.1),('3:15.09',195.09),('3:33.5',213.5),('3:35.3',215.3),('3:49.0',229.0)]
print('boundary | W=1.5s before->after dB  drums bass vocals other mix')
for lab,t in B:
    row=[]
    for n in ['drums','bass','vocals','other','mix']:
        row.append('%s %.1f>%.1f(%+.1f)'%(n[:2],m(n,t-1.5,t-0.05),m(n,t+0.05,t+1.5),m(n,t+0.05,t+1.5)-m(n,t-1.5,t-0.05)))
    print(lab,' | '.join(row))
# bass on fraction per section
secs=[('intro',0,10.4),('hook1',10.4,30.4),('verse1',30.4,71.3),('hook2',71.3,91.4),('verse2',91.4,132.0),('hook3',132.0,152.4),('verse3',152.4,193.1),('hook4',193.1,213.5),('outro',215.3,236.5)]
for nm,a,b in secs:
    bo=(S['bass'][int(a*100):int(b*100)]>-40).mean(); vo=(S['vocals'][int(a*100):int(b*100)]>-45).mean()
    print(nm,a,b,'len %.1f s=%.2f bars(2.553)'%(b-a,(b-a)/2.553),'bass on %.0f%% voc on %.0f%%'%(bo*100,vo*100),'mix %.1f drums %.1f other %.1f'%(m('mix',a,b),m('drums',a,b),m('other',a,b)))
# end
for n in ['mix','drums','bass','other','vocals']:
    e=S[n][-300:]; print('end',n,'max last3s %.1f'%e.max())
# bass-on spans
print('BASS spans',[(round(a,1),round(b,1)) for a,b in spans('bass',-40,0.8,1.5)])
# hook period: where does voice end after hook 4
v=S['vocals']; 
for a,b in [(3200,3600),(3340,3600)]:
    pass
for t in np.arange(205,218,0.5): print('%.1f voc %.1f'%(t,m('vocals',t,t+0.5)),end=' ; ')
