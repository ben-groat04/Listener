import sys, json, numpy as np, librosa
d=sys.argv[1]; out=d+'/audio_features/extra'
y2,sr=librosa.load(d+'/audio/song.wav',sr=22050,mono=False)
m=y2.mean(0); L,R=y2[0],y2[1]
S=np.abs(librosa.stft(m,n_fft=2048,hop_length=512)); f=librosa.fft_frequencies(sr=sr,n_fft=2048)
H,P=librosa.decompose.hpss(S)
hop=512; fps=sr/hop
bands={'sub(<80)':(20,80),'bass(80-250)':(80,250),'mid(250-2k)':(250,2000),'presence(2-5k)':(2000,5000),'air(5k+)':(5000,11000)}
res={}
n=int(S.shape[1]/fps)
def sec(a): return np.array([a[int(i*fps):int((i+1)*fps)].mean() for i in range(n)])
rows={}
for k,(lo,hi) in bands.items():
    idx=(f>=lo)&(f<hi); rows[k]=sec((S[idx]**2).sum(0))
rows['perc_ratio']=sec((P**2).sum(0)/((P**2).sum(0)+(H**2).sum(0)+1e-9))
# stereo
M=(L+R)/2; Sd=(L-R)/2
fr=sr
def rms(x): return np.sqrt((x**2).mean()+1e-12)
rows['side_to_mid_dB']=np.array([20*np.log10(rms(Sd[i*fr:(i+1)*fr])/rms(M[i*fr:(i+1)*fr])) for i in range(n)])
rows['rms']=np.array([rms(m[i*fr:(i+1)*fr]) for i in range(n)])
# tempo
oenv=librosa.onset.onset_strength(y=m,sr=sr)
tg=librosa.feature.tempogram(onset_envelope=oenv,sr=sr)
ac=librosa.autocorrelate(oenv,max_size=400)
tempos=librosa.tempo_frequencies(tg.shape[0],sr=sr)
mean_tg=tg.mean(1)
cand=[(round(float(tempos[i]),1),round(float(mean_tg[i]),3)) for i in np.argsort(-mean_tg)[:8] if tempos[i]>0]
# beat-phase of drums stem: onset hist at 1/16 grid
bt=json.load(open(d+'/audio_features/beat_times.json'))
bt=np.array(bt if isinstance(bt,list) else bt.get('beat_times',bt))
res['tempo_candidates_tempogram']=cand
res['median_beat_interval_s']=float(np.median(np.diff(bt)))
# sections of 8 bars-ish: use 15s blocks
blocks=[]
for s in range(0,n,10):
    e=min(n,s+10); b={'t':f'{s//60}:{s%60:02d}'}
    for k in rows: b[k]=round(float(np.mean(rows[k][s:e])),4)
    blocks.append(b)
res['blocks10s']=blocks
res['overall_side_to_mid_dB']=round(float(np.mean(rows['side_to_mid_dB'])),2)
res['LR_corr']=float(np.corrcoef(L,R)[0,1])
# dynamics
r=rows['rms']; res['rms_p10_p50_p90']=[round(float(x),3) for x in np.percentile(r[:230],[10,50,90])]
res['crest_dB']=float(20*np.log10(np.abs(m).max()/rms(m)))
# silences / dips: seconds where rms < 40% median within 10-225
med=np.median(r); res['low_rms_seconds']=[int(i) for i in range(n) if r[i]<0.5*med]
# per-second dump
json.dump({k:[round(float(x),5) for x in v] for k,v in rows.items()},open(out+'/per_second_extra.json','w'))
# beat-level energy: bass stem periodicity (808 pattern) via onset envelope of low band
low=librosa.feature.rms(y=librosa.effects.preemphasis(m),frame_length=2048,hop_length=512)[0]
json.dump(res,open(out+'/music_extra.json','w'),indent=1)
print(json.dumps(res,indent=1)[:6000])
# chromagram key per 30s with harmonic only
yh=librosa.istft(H)
ch=librosa.feature.chroma_cqt(y=yh,sr=sr)
names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
for s in range(0,n,30):
    c=ch[:,int(s*sr/512):int((s+30)*sr/512)].mean(1)
    print(s,[names[i] for i in np.argsort(-c)[:4]],np.round(np.sort(c)[::-1][:4],2))
