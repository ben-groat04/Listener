import sys; sys.path.insert(0,'.'); from lib import *
Z=np.load("results/a1_raw.npz"); B=Z["S1_sauc__boot"]; P=Z["S1_sauc__point"]; I={m:i for i,m in enumerate(MODELS)}
r=[I[m] for m in REFS]; am=B[:,r].argmax(1); print("bootstrap share where each ref is best, order", REFS, [round(float(np.mean(am==k)),2) for k in range(3)])
mx=B[:,r].max(1); d_fixed=B[:,I['pair_z']]-B[:,I['ref_w4r1_listening']]; d_best=B[:,I['pair_z']]-mx
print("pair_z minus fixed listening mean", d_fixed.mean().round(4), np.percentile(d_fixed,[10,90]).round(4)); print("pair_z minus best-of-3 mean", d_best.mean().round(4), np.percentile(d_best,[10,90]).round(4))
