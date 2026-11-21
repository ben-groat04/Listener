#!/bin/sh
# Downloads the Essentia model files used by build_essentia.py into .cache/shared/w4-essentia/models/ (needs essentia.upf.edu on the network allowlist).
D=/home/user/Listener/taste-model/.cache/shared/w4-essentia/models; mkdir -p $D; cd $D
B=https://essentia.upf.edu/models
for e in pb json; do curl -fsS -o discogs-effnet-bs64-1.$e $B/feature-extractors/discogs-effnet/discogs-effnet-bs64-1.$e; done
for h in genre_discogs400 mtg_jamendo_moodtheme mtg_jamendo_instrument mtg_jamendo_genre danceability voice_instrumental mood_aggressive mood_happy mood_party mood_relaxed mood_sad mood_acoustic mood_electronic tonal_atonal; do
  for e in pb json; do curl -fsS -o $h-discogs-effnet-1.$e $B/classification-heads/$h/$h-discogs-effnet-1.$e; done; done
for h in approachability engagement; do for e in pb json; do curl -fsS -o ${h}_regression-discogs-effnet-1.$e $B/classification-heads/$h/${h}_regression-discogs-effnet-1.$e; done; done
