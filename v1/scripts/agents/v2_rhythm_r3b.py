import librosa,numpy as np
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050;h=128;fr=sr/h;ph=0.1333;P=0.49995
def L(n):return librosa.load(D+n+'.wav',sr=sr,mono=True)[0]
def db(y):return librosa.amplitude_to_db(librosa.feature.rms(y=y,frame_length=1024,hop_length=h)[0]+1e-9)
dr=db(L('drums'));ba=db(L('bass'))
def runs(x,thr,lo,hi,minlen=0.2):
    a,b=int(lo*fr),int(hi*fr);idx=np.where(x[a:b]<thr)[0]
    if not len(idx):return []
    rs=np.split(idx,np.where(np.diff(idx)>3)[0]+1)
    return [((a+r[0])/fr,(a+r[-1])/fr) for r in rs if (r[-1]-r[0])/fr>=minlen]
for name,x,thr in [('drums',dr,-35),('bass',ba,-40)]:
    print(name)
    for lo,hi in [(84,90),(154,160),(214,219),(274,282)]:
        for s,e in runs(x,thr,lo,hi):
            print('  gap %.2f-%.2f len %.2f  beat-from-grid %.2f..%.2f'%(s,e,e-s,((s-ph)/P-1)%8,((e-ph)/P-1)%8))
