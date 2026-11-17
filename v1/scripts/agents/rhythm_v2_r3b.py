import numpy as np, librosa
from scipy.signal import butter, sosfiltfilt
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050; hop=32
dr=librosa.load(D+'drums.wav',sr=sr)[0]
band=lambda y,lo,hi: sosfiltfilt(butter(4,[lo,hi],'band',fs=sr,output='sos'),y)
for nm,(lo,hi) in {'kick':(30,150),'snare':(150,2000)}.items():
    o=librosa.onset.onset_strength(y=band(dr,lo,hi),sr=sr,hop_length=hop); fps=sr/hop
    on=librosa.onset.onset_detect(onset_envelope=o,sr=sr,hop_length=hop,units='time',delta=0.5)
    for a,b in [(30,44),(60,70),(76,84),(88,96),(150,156),(296,306)]:
        print(nm,a,b,[(round(x,2),round(x%0.5,2)) for x in on if a<=x<b])
