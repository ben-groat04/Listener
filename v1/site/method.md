# How this was made

**The videos.** `videos/video1.mp4` is Public Service Broadcasting's *Elfstedentocht Part 1* (3:09) and `videos/video2.mp4` is *Part 2* (5:04). Both were made in 2013 for the Explore the North festival in Leeuwarden, for the 50th anniversary of the 1963 race, using footage and voice-over from the Fries Film Archief. The part order is confirmed by the official track lengths on MusicBrainz.

**How the agents "listened".** No agent can hear. Each track was split into stems (vocals, drums, bass, everything else) with demucs, then measured: per-second loudness and stereo width, spectrograms in 20-second windows, chords, the melody line, tempo and beats, zero-shot audio tags (CLAP), and transcripts of the Dutch narration (faster-whisper, including a pass on the isolated voice). The picture was read from frames sampled once a second plus a keyframe per shot, and the link between music and picture was measured (cuts against beats, cut rate against loudness).

**How the reading was built.**
1. Listeners took the music 20 seconds at a time, then seven specialists (harmony, rhythm, sound, voice, form, lineage, feeling) argued over the whole track for three rounds.
2. Viewers took the picture 20 seconds at a time.
3. A six-person panel (first-time viewer, film critic, music critic, cultural insider, symbolist, sceptic) debated the whole piece over three rounds, reading the music analysis first.
4. Fact-checkers then tried to disprove every claim, and refuted claims were fixed: about 15 to 30 per document.
5. Fresh "cold readers" audited the finished work and their findings were fixed and verified.

**What a blind test showed.** The whole pipeline was also run with no background facts and no web. It still worked out the subject (the 1963 Elfstedentocht) from the spoken date and the newspaper headlines in shot. Comparing the two runs showed that **context biases as well as helps**: the informed run "saw" a celebratory raised fist (in fact a raised hand) and a headline it could not actually read, both primed by the research. The blind run read more like a person responding. Those lessons are now rules in the toolkit's prompts.

**Limits.** The feelings described are reasoned from measurements, not heard. Instrument identity (guitar or synth) often cannot be settled from stems. Frames are sampled about once a second, so brief moments can be missed. Uncertain points are marked in the text.

**Why the first version was rewritten.** The first published reports read like an audit of a spectrogram: decibels, timestamps, confidence tags. You said, rightly, that this is not how a person listens. A six-person panel (music psychologist, fan, music journalist, musician, phone viewer and a devil's advocate) debated why, and the pipeline gained a final stage. A verified sheet of key moments is built, a single listener's account is written only from those facts, it is checked for jargon and clock times, fact-checked, and scored by judges who did not see how it was made. The **Part 1** and **Part 2** tabs are those listening accounts. The **in detail** tabs keep the evidence-heavy reports underneath them.
