# Words: t_dl_mirror (blind mode)

Sources used: three existing whisper (medium) transcripts in `lyrics/` (mix transcribe, mix translate, vocals-stem transcribe), the "doubtful" lists, the per-second vocal stem loudness (`stems/stem_rms_per_second.json`), and frames opened at full size. I also re-ran faster-whisper medium (int8, cpu, English) on vocals.wav windows 0:08-0:32, 0:27-0:57, 1:10-1:32, 3:25-3:57 and 3:48-3:59. Results: verse 1 text (0:27-0:57) reproduced the earlier reading exactly; hook windows 1:10-1:32 and 3:25-3:35 gave 'in my period in the morning, just see me, I see you' (3:27 window: 'In the period in the morning'), so 'period' is the most repeated reading of the hook word (4 passes) with 'carry/hair/ear/theory' as minority variants, still unconfirmed by ear; the intro 0:08-0:30 re-run was poor (lp -1.39, 'You know who it is, yeah'; 'In my period in the morning, listening to me') and is not used as primary; 3:56 'Thank you' on a silent stem is hallucination. Everything below is a collation and judgement across all passes. I cannot play audio.

## Language, speakers, era, quality
- OBSERVED: all transcripts auto-detect English (p=0.85 on mix, 0.68 on vocals stem). All lines are English; no translation needed (the "translate" pass is English to English and agrees with the transcribe pass). English column = original.
- OBSERVED: the vocal stem is silent (<0.001 RMS) for 0:00-0:09, becomes active at 0:10 and runs to about 3:34; it is silent from 3:35 to the end (239 s). Short gaps at 0:14, 0:24, 1:25, 2:26, 3:27 match the breaths/pauses between phrases.
- INFERRED (from the transcripts' rhyme and flow): one rapper/singer, first person, in verses; a sung/chanted hook. Whether the hook is the same voice or a second voice is not determinable from text. SPECULATED: hook may be doubled or sung over a sample.
- OBSERVED: no narrator, reporter or interviewee speech is evident in the transcripts. The three "Thanks for watching" / "You" lines after 3:56 are whisper hallucinations over a silent vocal stem (vocal stem is silent there): DISCARD.
- Recording era/quality: INFERRED (weak) from lyrics ("95 Nissan", "favorite CD") and the 4:3-ish, soft, compressed picture with a small logo bottom-right: a mid-2000s-style music video, standard-definition. Print on the title card, legible at full size in f_0003 and f_0230: "DL / Mirror / A Boston State Of Mind / CommonWealth Records / Dir: Matt Workman". OBSERVED. (Treat these as the on-screen credits only; I make no further identification.) Unread: small white logo bottom-right (f_0012, f_0100), tiny text beneath it.
- Mix audio: INFERRED that vocal is forward and clear in the mix (stem RMS 0.1-0.2 while singing); whisper marks many mix segments "no_speech_prob" 0.66-0.90 anyway because the beat is loud, so those flags do NOT mean no speech; the vocal-stem run confirms speech throughout.

## Confidence key
H = all 2-3 transcripts agree, text coherent. M = transcripts differ in a few words; sense clear. L = transcripts disagree materially; best guess. Times are from the whisper segments (good to about 1 s, and the long segments in the hook sections were not resolved per line). Tag: all rows OBSERVED as transcription (heard by whisper), the English column's correction of mishearings is INFERRED.

## Timestamped transcript
### Intro and hook (0:10-0:30)
| Time | Words | Conf | Notes |
|---|---|---|---|
| 0:10-0:14 | You, you I see | M | mix and translate agree; whisper also wrote "Music" at 0:10 (label, not a word) |
| 0:14-0:15 | Yeah | M | ad-lib |
| 0:15-0:17 | In my [carry/period/hair/ear?] in the morning | L | whisper variants: "carry", "period", "hair", "ear", "theory". The vocals-stem pass gives "theory" (3:20) and "period" in the hook elsewhere. Best guess for the repeated word is unresolved; "mirror" fits the title card but is NOT heard, so I do not claim it. |
| 0:17-0:19 | There's a scene/thing in me | L | "thing" vs "scene" |
| 0:19-0:20 | You know what it is / where we live, yeah | L | transcripts disagree |
| 0:20-0:24 | You, you I see | M | |
| 0:24-0:28 | In my [carry/period] in the morning | L | as above |
| 0:28-0:30 | Still seein' me, I see you | M | flagged doubtful by whisper (beat) but vocal stem agrees |

### Verse 1 (0:30-1:11), rapped
| Time | Words | Conf | Notes |
|---|---|---|---|
| 0:30-0:33 | Wake up, stretch my arms, prepare for the daily | H | |
| 0:33-0:35 | Look down on the bed and see a strange lady | H | |
| 0:35-0:38 | Can't recall who she is, 'cause last night's blurry | H | |
| 0:38-0:40 | But it's nine to five (heard "nine on five"), gotta move in a hurry | M | "nine on five" in all passes; "nine to five" is my inference from sense |
| 0:40-0:44 | All I can recall is one shot, two shot, three, four, five | H | |
| 0:44-0:46 | Henny on the rocks, non-stop | M | "Henny" is what whisper heard (possibly a brand name; unverified) |
| 0:46-0:48 | Scratch my head, tryna recall after | H | |
| 0:48-0:51 | The shots dancin' and bein' a drunk bastard | M | |
| 0:51-0:54 | But all I know is this freak is wrapped/racked in nothin' | L | "wrapped"(vocals) vs "racked"(mix) |
| 0:54-0:56 | But my bed, bath and beyond, she [felt/fell] rings | L | last word unclear; a wordplay on "bed bath and beyond" is INFERRED |
| 0:56-1:01 | Fiancée's on her way up the steps, wake the girl, grab her clothes, and in the closet she goes | M | "Fiance's" in transcript |
| 1:01-1:06 | Getting closer, pop tic tacs, and like toaster pick up the latex, hide the mimosa | L | "and like toaster" garbled; "latex" and "mimosa" heard in all passes |
| 1:06-1:11 | Run to the sink, splash water in my face, look in the mirror, but today I seem out of place like | H | the word "mirror" is clearly sung here (matches the title card text) |

### Hook (1:11-1:31)
| 1:11-1:31 | You, you I see, in my [period/carry/theory] in the morning, just seein' me, I see (repeated twice, about 10 s each) | M | whisper merged into two long segments; exact line times unresolved |

### Verse 2 (1:31-2:12)
| Time | Words | Conf | Notes |
|---|---|---|---|
| 1:31-1:36 | Get in my '95 Nissan and put my favourite CD on, which just can't get a break | M | "Nissan" heard in all three passes |
| 1:36-1:41 | So I start my engine so I won't be late, gotta get to my job and scrub the stacked plates | M | |
| 1:41-1:44 | Is it just me or am I catching reds? | H | |
| 1:44-1:46 | Light after light, these blocks, I'm bangin' my head | M | |
| 1:46-1:50 | Urgh, I'm gettin' pissed off, driver in front of me is drivin' slow | M | |
| 1:50-1:54 | [garbled: "it's cell gap and it slips off" / "in a cell, yapping"] Swerve right to left, symbolizing a criss-cross | L / M | first half unresolved (a phone call is SPECULATED); "swerve right to left" is solid |
| 1:54-1:57 | Point my finger out the window to him and flip [dog/him off] | M | |
| 1:57-1:59 | He slams on the brakes, causin' me to [wreck/rip] in them | L | |
| 1:59-2:04 | Head hits the wheel, lose full comprehension; out of anger, jump out the car and dash towards him | M | |
| 2:04-2:09 | [my back received a whoopin'] I put a crease in his cheeks and I knew I was in trouble | L | |
| 2:09-2:12 | As I saw myself inside his [blood/bottle?] | L | the image the verse ends on: "saw myself" in his reflection is INFERRED, not heard |

### Hook (2:12-2:32)
| 2:12-2:32 | You, you I see, I see, in my [period] and in the morning, just seein' me, I see you (twice) | M | pass 2 transcript gives clear line times: 2:12, 2:16 "I see", 2:17 "in my period and in the morning", 2:20 "just seein' me", 2:21 "I see you, you I see", 2:26 "in my period...", 2:30 "just seein' me", 2:31 "I see you" |

### Verse 3 (2:32-3:14)
| Time | Words | Conf | Notes |
|---|---|---|---|
| 2:32-2:35 | Nine to five, they cuttin' my funds, need implants (?) | L | "Now on the fly they cuttin'" / "Nine to five" vary |
| 2:35-2:38 | Slottin' things to cookie for a piece of a food stamp | L | "food stamp" heard in mix and translate; "bootstamp" in the vocals pass |
| 2:38-2:40 | I hustle hard on my [n-word], I stay on the grind | M | slur appears in the transcripts at 2:37 and 2:40 (transcribed as "nigg"); recorded here as a fact of the lyric, not repeated in full |
| 2:40-2:42 | Collect every dime 'cause I'm smarter, my [n-word] | M | |
| 2:42-2:44 | Got the baggies with the custom logo | H | |
| 2:44-2:47 | To separate myself from the garbage and [high-price / hot bright] logos | L | |
| 2:47-2:50 | Watch, I'ma add this neighbourhood in a chokehold | L | "choco" / "chokehold"; vocals pass says "chokehold" |
| 2:50-2:52 | Three for ten all day, that's my promo | H | |
| 2:52-2:55 | Pockets lookin' more obese as the day goes | H | |
| 2:55-2:57 | Lipo mentality, suckin' the streets | M | |
| 2:57-3:00 | Sell to a 12-year-old who ODs on the corner | H | |
| 3:00-3:03 | Making the trades [of/with] the street hotter than California | M | |
| 3:03-3:05 | Can't find/think of no lawyer, phone call or line-up | M | |
| 3:05-3:08 | Life is living colour right now 'cause my time's up | H | |
| 3:08-3:11 | Locked like [thousand/styles in] Acorn, through the shiny aluminium toilet | L | first half unresolved |
| 3:11-3:13 | I can see that my face gone [tan / ...] | L | vocal stem pass ends "my face gone"; "tan" only in the mix pass; last word unreliable |

### Hook out (3:14-3:34)
| Time | Words | Conf | Notes |
|---|---|---|---|
| 3:14-3:17 | You, I see. I see. | M | |
| 3:17-3:20 | In my [theory/ear/hair/period] and my morning | L | |
| 3:21-3:24 | I see you. | M | |
| 3:25-3:27 | You, I see. | M | |
| 3:28-3:31 | In my [theory/hair] and in the morning | L | |
| 3:31-3:34 | You see in me, I see you / "If I hear it in the morning, then I see it in me, I see you" | L | mix-transcribe and mix-translate disagree; last phrase "I see you" is solid |
| 3:34-3:59 | no speech | H | vocal stem silent; the "Thanks for watching" at 3:56 is hallucination |

## Phrases carrying emotional or thematic weight (INFERRED from the text)
- "You, you I see ... just seein' me, I see you": the refrain; its pairing of seeing the other and seeing oneself, together with the title "Mirror" (OBSERVED on the title card) and the line "look in the mirror, but today I seem out of place" (1:06, H) is what makes the reflection theme INFERRED. The repeated unclear word ("carry/period/hair/ear/theory") means I cannot tell what the refrain says it sees "in the morning".
- "Look down on the bed and see a strange lady / Can't recall who she is" (0:33-0:38): morning-after, disorientation (OBSERVED words).
- "Fiancée's on her way up the steps ... hide the mimosa" (0:56-1:06): concealment/panic (OBSERVED words; tone INFERRED).
- "I knew I was in trouble as I saw myself inside his ..." (2:06-2:12, L): confrontation turns to self-recognition (the second half is uncertain).
- "can't ... no lawyer, phone call or line-up ... my time's up" (3:03-3:08): arrest/consequence at the end of the third verse (INFERRED).
- Structure: INFERRED each verse is a day-in-the-life vignette (morning bed, commute road-rage, street dealing), each followed by the same hook. This structure matches the auto sections (A verse / B hook at 0:30, 1:12, 1:33, 2:13, 2:32, 3:14).
- A contemporaneous speech content warning: language includes a racial slur and drug sale (child OD) themes. Recorded in the table as heard.

## Not resolved (to improve later)
- The repeating hook word at 0:15, 0:24, 1:11-1:31, 2:12-2:32, 3:17, 3:28. Needs a short high-effort pass (large-v3 on vocals.wav windows 0:12-0:30 and 2:12-2:34). My medium re-run on the stem supports 'period' but is not decisive.
- Verse 2 lines at 1:50-1:54 and 1:57-1:59; verse 3 lines at 2:32-2:38, 3:08-3:13.
- Exact line times in the 1:11-1:31 hook (whisper returned two 10-second blocks).
