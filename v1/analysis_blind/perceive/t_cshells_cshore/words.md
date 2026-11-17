# Words: t_cshells_cshore (blind mode)

## Bottom line
**No intelligible spoken or sung words were found in this video. It reads as instrumental.** (INFERRED from: vocals stem near silent for 6 minutes; every whisper hit is a known hallucination pattern; see below.) Confidence: fairly high for "no sustained lead vocal"; moderate for "no brief spoken fragment anywhere" (I cannot play audio, and the stem has a few short bursts I could not resolve into words).

## Table of whisper output (all rejected unless noted)
| Time | Original | English | Confidence | Notes |
|---|---|---|---|---|
| 0:28.6-0:30.0 | "You" | You | very low (p=0.03, no_speech 0.74) | Mix transcript. Single word on a quiet, synth-only-looking stretch (other-stem only, vocals stem ~0.0001). Rejected. |
| 1:16.6-1:21.3 | Welsh-looking strings ("Cymysgwch ar gyfer cyngor ymlaen...") | no coherent meaning | none (no_speech 0.94) | Vocals-stem run, language guessed "cy" at p=0.49. Zero-length repeated segments at 1:19.7-1:19.9. Hallucination. |
| 2:21.7-2:24.3 | "Ychwanegwch yn fawr." | (roughly "add greatly") | none | Hallucination, same pattern. |
| 3:37.4-3:45.2 | Welsh-looking fragments | n/a | none | no_speech 0.87. |
| 4:28.9-4:29.6 | "This is the only way to get to the top of the mountain. We're going to have to go all the way up to the top." | as written | none | Mix transcript; all words compressed into 0.7 s (4:28.94-4:29.64), timestamps collapsed. Impossible as speech; a stock hallucination. My re-run of 4:24-4:34 gave "Thanks for watching!" (English forced) or "Ychwanegwch ychwanegwch..." (auto): the output changes with settings, so it is not real. |
| 5:15.8-5:44.0 | broken Welsh/English mix | n/a | none | avg_logprob -1.92, one 20 s "segment". Hallucination over the loudest synth passage. |
| 5:59.6-5:59.9 | "Thank you." | Thank you. | none | Over black screen at end; typical whisper end-of-file hallucination. |
| my re-runs (medium, int8) | "Thanks for watching!" at 0:24-0:34 and 4:24-4:34; "Thank you for your viewing." at vocals 5:08-5:18; "Thank you very much." at 5:55-5:57 | n/a | none | Different phrases each time; all are well-known whisper outputs on music/silence. Vocals-stem windows 2:18-2:30 and 5:28-5:36 returned nothing. |

Language detection: unstable (en p=0.39 on mix; cy p=0.49 on vocals stem; nn/cy on re-runs). A language flipping between English, Welsh and Norwegian on the same audio is itself evidence there is no speech to detect. (INFERRED)

## Vocals stem check (OBSERVED)
Per-second vocals loudness is ~0.0001 almost throughout, against 0.1-0.2 for "other". Small bursts only at: 2:22-2:24 (peak 0.052 at 2:23), 3:27, 3:45, 4:27, 4:57, 5:12-5:13 (0.025), 5:17, and a low plateau 5:33-5:38 (~0.003). The biggest, 2:23, is about 25% of the drum stem level at that moment and is a single-second spike, the shape of a transient (drum/synth hit leaking into the separator) rather than a phrase. Whisper on that window gave nothing. (INFERRED; SPECULATED: a vocal chop or sample could exist at 2:23 and 5:13 but is not resolvable.)

## Who speaks
No narrator, reporter, interviewee or singer is identifiable. (INFERRED.)

## Recording era and quality
Cannot be judged from words. Picture only: the footage has a warm, faded, film-like look and the frames shown (e.g. a white open-top car by a beach at about 0:16-0:19, a pale blue-green box-like object labelled in small print I cannot read at 0:11-0:15) suggest older archive material; audio is a full, modern-sounding electronic mix by loudness curve (bass/drums stems start about 1:10 and build), though I cannot hear it. (OBSERVED for frames; INFERRED/SPECULATED for era.)

## Printed words on screen (the only "words" in the video)
Opened at full size: f_0002 and f_0008.
- 0:00-0:03 (literal: white sans-serif capitals, centred on black) "THE NOISE WEEKEND ORCHESTRA". Reading: an artist/credit card. INFERRED.
- 0:05-0:09 (literal: white sans-serif capitals, centred on black) "C-SHELLS C-SHORE". Reading: the title card; the pun-like spelling sounds like "she sells sea shells... sea shore" when spoken, but that is SPECULATED. 
- 0:11-0:15: tiny print on the pale blue-green object, unread (dark letters, one short word, blurred).
- 5:40-5:59: contact sheet 18 shows mostly black, with a faint dark image at 5:40; no print visible. Not opened at full size beyond the contact sheet, so "none seen" only.
- Unread: any print later in the video; I did not open all frames.

## Phrases carrying emotional or thematic weight
None sung or spoken. The only wording available is the title "C-SHELLS C-SHORE" (a seaside/shore theme, which matches the beach frame at 0:16 - INFERRED, weakly). The hallucinated "the only way to get to the top of the mountain" at 4:29 must not be treated as content.

## Recommendation for downstream analysis
Treat this as an instrumental piece; weight analysis on the music features (other/bass/drums stems; the loud "other"-stem peaks from about 3:30 to 5:30) and the picture, not on lyrics.
