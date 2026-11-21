SHARED PREP round 1 REPORT. Start 2026-11-21T11:21:19Z, end 2026-11-21T13:09:57Z (TIMING.txt in /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf4/prep-r1/). FROZEN created at /home/user/Listener/taste-model/.cache/shared/FROZEN. MANIFEST.txt and FEATURES.md (new sections 4, 5, 6) are in the same folder. No sealed data was touched and I did not use git. I added nothing to .cache/shared/ beyond the w4-* directories, FEATURES.md, MANIFEST.txt and FROZEN.

WHAT WAS BUILT (location and format only)
- .cache/shared/w4-essentia/ : float16 npz shards (shard_NNNN.npz, 50 clips per block in the md5-sorted manifest order), labels.json, and models/ (pb + json files). Shards hold per-patch head activations ([P,605]) with patch centre times, per-patch 1280-d embeddings, clip-level mean/max of heads, and clip-level mean/std of the embedding. Array names, shapes and dtypes are in FEATURES.md section 4. Total 1.1 GB.
- .cache/shared/w4-lyrics/ : lyrics.jsonl (15,177 lines), feats.pkl and emb.pkl (15,177 entries each).
- .cache/shared/w4-descriptors/ : NOT BUILT (see below).
- Code is in /home/user/Listener/taste-model/predictors/w4-shared-prep/: build_essentia.py, fetch_models.sh, fetch_lyrics_w4.py, build_lyrics_feats_w4.py, universe.py, coverage.py, make_manifest.py. The exact regenerate commands are in FEATURES.md. I chose this folder name myself because the prompt gave no predictor folder for shared prep.

P1 ESSENTIA (ran)
- `pip install essentia-tensorflow==2.1b6.dev1389` worked at the first attempt, so the fallback was not needed.
- The embedding model and all 16 heads downloaded: genre_discogs400, mtg_jamendo moodtheme / instrument / genre, danceability, voice_instrumental, the 7 mood heads, tonal_atonal, approachability_regression and engagement_regression. The approachability and engagement files sit under classification-heads/approachability/ and engagement/. I did not compute any artist or label embeddings.
- Coverage: 10,100 of 10,288 ok clips (202 of 206 blocks), 281,861 patches, 0 failed decodes.
  - MISSING: blocks 199, 203, 204 and 205 (188 clips, no rows). I stopped starting new blocks at the 105-minute mark.
  - Share of tracks with a row (ALL slice): train 0.877 (has_url 0.894), tried 0.921 (0.939), decoy 0.974 (0.991).
  - TUNE: tried 0.911, decoy 0.974. LATE: tried 0.936, decoy 0.975.
  - The per-slice tables are in FEATURES.md.
- DROPPED: arousal/valence heads on msd-musicnn-1 (emomusic and deam). The musicnn front end cost 1.3-1.7 s per clip, which would have raised the per-clip cost from about 2.1 s to about 3.5 s, and the full pass would not have fitted the cap. I deleted the musicnn, emomusic and deam model files again.
- Runtimes measured:
  - 50-clip benchmark with musicnn: 197 s.
  - Single-process component timing per clip: decode 0.15 s, effnet 1.8-2.0 s, 16 heads 0.1 s, musicnn 1.3-1.7 s.
  - Production pass: 4 workers with 1 thread each, 11:29 to 13:08 UTC (99 min), about 106-130 s per 50-clip block per worker.
- Go/no-go: the estimate for the full pass without musicnn was about 94-110 min wall clock on 4 workers, which is over the 105-minute mark. I chose go with a stated partial coverage in md5 block order rather than dropping P1.
- P1 shard code was cleaned up after the run (dead-code line removed). I re-ran 4 clips and the output was identical to shard 0 (max abs diff 0.0).

P2 DESCRIPTORS (not built, dropped)
- The P1 pass used all CPU through the cap, and P1 has priority.
- 20-clip benchmark (one process, run while P1 was running): 2.4 s per clip with HPSS, 0.44 s per clip without HPSS. Neither pass was run for the full manifest.
- The descriptor script was deleted because it was unused, and no w4-descriptors directory exists.

P3 LYRICS (ran)
- All 10,880 W3 records were copied unchanged. The old directory was not modified.
- The universe (train, tried and decoy tracks of all 14 folds, main + holdout parts) is 10,651 trackIds; 4,297 had no record. All 4,297 were looked up with the same query and acceptance rules as W3, with 0 failures. The lookups took 792 s and ran with 3 request threads and a 0.3 s pause per request.
- feats.pkl and emb.pkl were built with the W3 code and model. The 10,880 existing embeddings were copied and 4,297 new ones encoded. This took about 10 min on 1 torch thread.
- 4,526 of the copied W3 records are not in the current universe. I kept them.
- Record, found and embedding rates (tried vs decoy), from the new directory:

| slice | group | tracks | lyr_record | lyr_found | lyr_emb |
|---|---|---|---|---|---|
| TUNE | tried | 1490 | 1.000 | 0.938 | 0.919 |
| TUNE | decoy | 7450 | 1.000 | 0.857 | 0.800 |
| LATE | tried | 960 | 1.000 | 0.949 | 0.944 |
| LATE | decoy | 4800 | 1.000 | 0.883 | 0.843 |
| ALL | tried | 2450 | 1.000 | 0.942 | 0.929 |
| ALL | decoy | 12250 | 1.000 | 0.868 | 0.817 |

  - ALL train: record 1.000, found 0.867, emb 0.817.
  - The old decoy record rate was 0.578. The tried/decoy gap in found rate is now 0.942 vs 0.868 in ALL.

CHECKS I RAN (facts)
- The coverage script's track counts for the existing caches match the old FEATURES.md table (e.g. TUNE tried 1490, decoy 7450, ALL train 16234).
- Test lyric and embedding counts above come from the cache files themselves.
- Peak CPU use was 4 workers for P1, plus 3 lookup threads then 1 torch thread for P3.

WHAT I ONLY BELIEVE (not tested)
- I did not check whether other agents ran concurrently. I assumed none did, since I used 4 workers.
- I did not validate the Essentia outputs against the model cards beyond shape and NaN checks (no NaN found in the 4-clip check).

Final shared-folder contents are listed with sha256 of every non-bulk file in /home/user/Listener/taste-model/.cache/shared/MANIFEST.txt. FEATURES.md has a sha256 recorded there. Nothing under .cache/shared/ may change now.