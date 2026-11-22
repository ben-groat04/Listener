# prep-r1 report
Start 2026-11-21T18:18:14Z, end 2026-11-21T18:36:35Z (about 18 min). Output: /home/user/Listener/taste-model/.cache/shared-w5r1/ (README.md, MANIFEST.txt with sha256, DONE; files made read-only). Code: /home/user/Listener/taste-model/predictors/w5r1-shared-prep/.
- A: mert_md5.npy, mert_full.npy, mert_layer_mean.npy, N=10288 = ok-manifest count, full coverage. Build A+B took 16 s. 200-row bit-equality asserted.
- B: essentia_compact.npz N=10100; 188 ok-manifest clips absent (listed in essentia_meta.json and README); labels in essentia_meta.json; 200-row equality asserted. seg_act has 574 empty (NaN) segment entries.
- C: runtime estimate from 5 clips: 4.6 s/clip, 200 clips about 15.5 min; go (cap 45 min). Actual 991 s, full 200 sample, offline (model cached locally). Table in README:
clips used 200 of 200
| layer | median cos fp32 vs cached (per window) | median cos cached 4-win mean vs 12-win mean | Spearman PC1-10 (median / min) cached vs 12-win |
|---|---|---|---|
| 1 | 0.9822 | 0.9899 | 0.985 / 0.978 |
| 2 | 0.9807 | 0.9909 | 0.986 / 0.976 |
| 3 | 0.9800 | 0.9881 | 0.987 / 0.984 |
| 4 | 0.9761 | 0.9867 | 0.988 / 0.983 |
| 5 | 0.9815 | 0.9805 | 0.983 / 0.974 |
| 6 | 0.9862 | 0.9748 | 0.980 / 0.964 |
| 7 | 0.9880 | 0.9704 | 0.952 / 0.904 |
| 8 | 0.9888 | 0.9766 | 0.953 / 0.925 |
| 9 | 0.9910 | 0.9770 | 0.972 / 0.914 |
| 10 | 0.9921 | 0.9838 | 0.960 / 0.929 |
| 11 | 0.9822 | 0.9822 | 0.968 / 0.947 |
| 12 | 0.9563 | 0.9871 | 0.980 / 0.955 |
PC1-10 Spearman, layer 12: [0.99, 0.986, 0.982, 0.98, 0.978, 0.98, 0.977, 0.972, 0.98, 0.955]
Note: shards held 2528 rows not in the ok manifest (excluded). No extraction beyond C. Nothing could not be done.
