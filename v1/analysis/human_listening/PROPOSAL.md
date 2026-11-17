# Proposal: writing about music the way a person hears it

*British English. Based on the three-round debate in `round_1/` to `round_3/` (psychologist, fan, critic, musician, viewer, devil's advocate) and on our own reports (`v1/analysis/video2/REPORT.md`, `video1/REPORT.md`) and workflows (`v1/workflows/listen.js`, `interpret.js`, `report.js`, `perceive.js`).*

The user said: "This is absolutely not how a human thinks and listens about music." The panel agreed with the user, and agreed on why. None of this is a call to throw the measurements away. They stay, as the checking layer. They stop being the voice.

One caution first. The panel is itself a set of agents predicting what people would say. It has no listener data (the fan and the psychologist both say so, and the critic ends by asking the user for one real sentence). So this proposal is a better-made prediction, not a finding. Step 6 of the pipeline below is how we get real data.

---

## 1. Diagnosis: why our outputs read like an audit

The panel found four causes (psychologist, round 3): order, time, unit, who. I add the pipeline root of each.

**1. Order: we measure first and attach a feeling afterwards.** A person gets a gist first ("cold, steady, sad-ish") and goes looking for reasons only if asked. Our pipeline runs the other way, and `listen.js` bakes this in. `MUSIC_RULES` demands a boundary evidence table, a 10 ms envelope of the last 3 s and re-measured stems before any "feeling" is allowed. The specialists (harmony, rhythm, sound, voice, form, lineage, feeling) are measurement lenses, and "feeling" is one of seven. The report then reads like this:

> "It feels like a held breath, or a cold morning heard through glass (INT)." followed by the thuds "at 0:00, 0:08, 0:12, 0:20 and 0:24".

The critic and the psychologist both call this the best sentence in the report. We apologised for it with a tag and then buried it under timestamps.

**2. Time: the reports are written from the end of the file.** Every agent has seen the whole track before writing. At 0:30 our writer already knows what happens at 1:28. A listener does not, so a report written this way cannot hold anticipation, which the psychologist calls half of what music is. It produces this:

> "Its force comes from the gap before it and the lack of any warning (INT); it is the biggest single event in the piece."

The musician checked the stems. There was warning: the drums thin out and nearly vanish at 1:01 to 1:03 and 1:10 to 1:15, and the pad-plus-voice gap tells anyone who knows builds that something is coming. Five panellists independently caught this one error. The deeper fault is that we wrote "no warning" without asking what the listener had been taught by then.

**3. Unit: we treat each event as an equal data point.** The structure is an inventory of timestamped stretches ("The trance and the plateau, 2:48.8 to 4:36.8"), each given roughly the same weight. People remember the first minute, the one moment that changes, the ending, and a mood for the rest. `interpret.js` and `report.js` ask for coverage (a dossier timeline, then a panel over it, then 1,200 to 2,000 words that must "Lead with the music. Then the picture. Then meaning. Then the moments that stay with you"). Coverage is the audit's unit. Memory's unit is the shape.

**4. Who: there is no listener.** Our "I" in `report.js` is "GROUNDED in the panel's attention, boredom and change-of-mind notes", which means it is a summary of notes written by personas who were themselves reading the dossier. Nobody ever sits in a seat, on a phone, without Dutch, not knowing the race. The ending then becomes a shrug:

> "Whether you feel grief, pride or a quiet leaving depends on what you bring."

A real listener does not say that, and it is the place where the report should be most specific.

**Further root causes in the prompts:**

- **Hard rules reward the audit voice.** `report.js` bans decibels in Tier 1, which is good, but the Tier 1 text is still produced from `music_reading.md`, a document written in measurements. A writer who is told to paraphrase an audit produces a paraphrased audit. The video2 report I read still has "about 50 dB louder", "roughly 22 dB", "161 BPM" and "36% of the 86 cuts... p about 0.09" in its body. It is nearer to a tagged audit than to the felt-prose layer the prompt asks for.
- **Epistemic tags in the main text.** OBS / INT / "best-supported word is withdrawal; 'mourning' is weaker". This ranks adjectives by evidence as if a mood were a hypothesis (critic).
- **The AI-limits disclaimer is both placed wrongly and repeated.** `report.js` says to state it once at the end of Tier 1, which is right, but the video2 report also opens with a "How this music was heard" section and re-states it per paragraph through tags. The result is the apology stamp (psychologist, critic).
- **Many adversarial checkers and no human-fit checker.** Every cold read in `report.js` is "feel", "truth" or "tiers". Only one asks "is it flat?", and it is checking the draft against the same sources. Nothing tests the draft against how a person would have heard it. The `truth` pass in particular can only move prose toward the numbers.
- **Measurements never get translated.** The musician found "the bass plays a figure grouped in threes against the kick" in our own data. It was a real finding, and the report wrapped it in a beat-tracker aside ("fools an automatic beat tracker, which reports 161 BPM") so the musician had to unwrap it into "it rolls rather than marches". Our pipeline has no step whose job is to turn a measurement into the thing a player would say.
- **Missing dimensions the reports never touch:** groove (does it push or drag?), what the picture makes the music mean, equipment (a phone has no floor), and what is left in memory afterwards.

---

## 2. How humans actually listen and watch (the panel's consensus)

In plain words:

1. **Gist first.** In a few seconds you know what kind of thing it is: slow or fast, warm or cold, a band or a machine, a voice or not. Detail comes later, if at all.
2. **Body before head.** The pulse reaches you first (foot-tap, lean in, drag). Then you recognise a character ("cold", "solemn"). Then what you bring: history, the voice, a memory.
3. **You live forward.** You do not know what comes next. Music works by teaching you something (a beat, a pattern), then keeping it, breaking it, or paying it off. Surprise and relief only exist for someone who does not know the end. The thinned-out drums before 1:28 are the teaching. The kick coming back on the one is the payoff.
4. **Attention comes and goes.** You notice a new sound, a shift, a voice. A repeated loop stops being listened to and becomes something you walk on. Often you only notice afterwards that it got fiercer.
5. **Memory is selective and schematic.** After one listen people keep the first minute, the one moment that changes, and the ending. Everything else is replaced by a schema: "it kept going, steady, got harder". Some keep the voice because it is the only part that sounds like a person.
6. **A voice is a person, even without the words.** For a listener who does not speak Dutch, the narrator is a person, a date, a sense of a great many numbers. For someone who knows the race, the words are 1963.
7. **Listeners differ, mostly at the ending and in the middle.** The same stop is "a wake" to someone who knows that 127 finished out of nearly ten thousand, and "a cold march that stops before you are ready" to someone who does not. One of the best answers the panel found is to say what two or three named listeners would bring, in a sentence each, rather than "depends on what you bring".
8. **Picture and music fuse.** A drone over a title card is a held breath. The same drone over a skater's back is effort. We have treated music and picture as two files that either line up or do not (the 80 ms sync test). People ask what the footage makes the music mean.
9. **We talk in plain words and comparisons.** "Rolls rather than marches." "It just stops, like someone leaving the room." A person compares to a gait, a room, a weather, or another record they know. They do not quote decibels.
10. **Equipment matters.** On a phone speaker the deep thumps in Part 1 do not exist. This is the commonest reason a real listener and our report would disagree.

---

## 3. The new output: what a "human listening" piece contains and how it is written

### 3.1 Shape

Replace the 1,200 to 2,000 word inventory with a short page that follows the way memory works. Roughly 600 to 900 words of main text, then the sidecar.

1. **The line (one sentence).** What it is like, said as you would say it in a pub. For Part 2 the critic's version is "A cold walk that stops before the end." It must be earned by everything below and not qualified by anything.
2. **Front page (about 300 words).** The verdict and a lean (who it is for, who it is not for), the one moment you will remember, the ending, what it is like.
3. **First listen, forward in time.** Written by a listener who does not know what is coming. What you have been taught by each point, what happens, what it does. It covers the opening wait, the first voice, the turn, the ending. The long middle gets two honest sentences (see 3.4).
4. **Who hears what.** Two or three named listeners (cold first-timer on a phone; a fan of this kind of record; someone who knows the race or speaks Dutch) with one or two sentences each, especially on the middle and the ending. This replaces "depends on what you bring".
5. **Second listen / afterwards.** What a repeat listener hears that a first one missed, and what survives in memory after the track has ended (see Section 4, stages B and C).
6. **What the picture does to the music** (one short paragraph, when there is a picture). Not whether cuts hit beats, but what the footage makes the music mean.
7. **Where it sits.** Short comparison to other music or films, only where a feature can license it (see 3.5).
8. **What nobody here could hear.** One paragraph (see 3.6).
9. **Sidecar (separate file or an appendix, not the page).** The evidence layer (see 3.7).

### 3.2 Voice

- Plain, committed, British. Say "you" and mean a named listener. No "I felt" (we did not), no "most people" with invented figures, no stolen band names.
- Plain confidence words ("probably", "surely", "a guess") rather than OBS/INT/SPEC/H/M/L.
- **Plain sentence first, then at most one image, then stop.** A beautiful sentence is the best hiding place for an error (the fan, on the "coat coming off in a warm room" that cannot be wrong).
- **Own one bet.** The critic's review deliberately leaves in "the moment you will remember", a clause that is pure bet, because a review without one bet is a catalogue. Be wrong in the one place where it is cheap and visible.
- **Commit on what the music does; be modest about what it does to a person** (musician). The current reports do it back to front: "how it was made cannot be recovered" sits beside a confident "feels like a held breath". Say "a synth-sounding layer slowly opens up" with confidence, and "for some listeners, a held breath".

### 3.3 Lines that ring false, and what a listener would say

These are taken from the reports and the panel's tables.

| Our report says | The problem | A person would say |
|---|---|---|
| "Its force comes from the gap before it and the lack of any warning (INT); it is the biggest single event in the piece." | Wrong on the stems (drums thin first). "Biggest" is a loudness ranking. | "It thins out, goes quiet, and then the kick comes back. That is the moment." |
| "The drums about 50 dB louder." | An artefact of measuring from near-silence. Nobody hears 50 dB. | "The kick comes back on the one, with nothing to announce it." |
| "A steady foot-tap with a slight limp (INT). It also fools an automatic beat tracker, which reports 161 BPM instead of 120." | The limp is the best phrase; the tracker sentence kills it. A tracker is not the listener. | "It rolls rather than marches." |
| "One layer brightens by roughly 22 dB in its top frequencies (about 3 dB in the full mix), fastest between about 3:26 and 3:50." | A measurement followed by a measurement of itself. | "Something up top keeps opening, a bit at a time, until you realise you are leaning forward." |
| "It feels like a held breath, or a cold morning heard through glass (INT)." | The best line, apologised for. | The same line without the tag. |
| "Whether you feel grief, pride or a quiet leaving depends on what you bring." | A shrug dressed as a conclusion. | "If you know that 127 people finished out of nearly ten thousand, it is a wake. If you do not, it is a cold march that stops before you are ready." |
| "The best-supported word is withdrawal; 'mourning' is weaker (INT)." | Ranks adjectives by evidence. | "It stops rather than ends." |
| "36% of the 86 cuts fall within 80 ms of a beat... p about 0.09." | The honest result is a plain sentence. | "The pictures do their own thing." |
| "The same seven notes (B C# D E F# G A) are used throughout." | No listener is moved by a pitch-class set. Appendix material. | "It stays in one sad-ish place and never leaves." |
| "The composer is in effect the mixer." | Interesting to us, meaningless to a listener. | Leave it out, or put it in the sidecar. |
| "The picture ignores the drop." | A detector's story about an edit whose intent nobody knows. | "The edit does not punch the drop." |

The pattern in the right-hand column is the finding. Every correct human sentence is shorter than ours, and the report already contained the seed of most of them.

### 3.4 What to leave out, and what gets the words

**Leave out of the body:** decibels, BPM, window sizes, p-values, pitch-class sets, tracker results, process narrative, agent counts, OBS/INT/H/M/L tags, "depends on what you bring", the full-length even-handed walk-through.

**Spend the words** on the opening wait, the first human sound, the one moment that changes, the ending and the silence after it. Give the long middle two sentences about what people do there: "This is the long stretch where the beat stops being something you listen to and becomes something you walk on. Some people will love it, some will check the time, and most will only notice afterwards that it had got fiercer." (psychologist). Counts a person can make ("two bars", "two hits") are fine. A tempo is allowed once if it says what the record is.

**Taught, then denied, then paid** (viewer, musician) is the narrative form to use for the drop and the ending.

### 3.5 Comparison to other music

Compare only when you can name the stem feature that licenses it ("a drum machine walking while an archive voice leads" is licensed; "sounds like Kraftwerk" is not unless a measured feature supports it). Otherwise use a gait, a room, or weather. One image per section. "Sounds like" is licensed; "is" is not, without stems. The existing `lineage` specialist already holds the sourced version; the new piece uses it sparingly.

### 3.6 Handling AI limits honestly without hedging every line

Say it once, in one plain paragraph near the end, not as a stamp on each claim:

> "None of us heard this. We worked from separated stems, levels and pitch tracks, and from frames. We could not hear the weight of the kick, the grain of the voice, the room, or whether any of it moved us. Where we write 'you', it is a prediction about a named kind of listener, and we would like your ear to overrule it."

Then stop apologising. This is the one change that the whole panel, including the devil's advocate, accepted. The devil's point was that the audit voice protects against overclaiming, so the replacement protects differently:

- Every feeling sentence is a **labelled prediction a real person could confirm or deny** (the viewer's rule). "Would", not "felt".
- Every feeling has a **mechanism test**: a thing in the signal plus a named mechanism, or it is cut (fan, devil).
- **Taught-before-denied is checked** against the stems before it is written (devil: "an expectation is a claim about the past, so check the past").
- The user's own ear has the final vote.

### 3.7 Where evidence lives instead

A **sidecar** (e.g. `REPORT.evidence.md` or the existing Evidence appendix, now keyed by sentence). Each human sentence has an id; each id has: the timestamp, the measurement, the mechanism, the confidence (H/M/L tags live here, not in the prose), and the check that was done. A reader who wants the alibi can open it, and fact-checkers read register one against it. The test for the body is that a reader who never sees the sidecar still finds the sentence true. "Measurement licenses the sentence and never appears in it" (critic).

---

## 4. Pipeline changes (video-agnostic)

Principle: **voice first, audit second.** The checking layer stays; it moves after the human drafts and checks them, instead of feeding them. Nothing here mentions any specific video. Video-specific facts still go in `v1/data/<video>/context.md`, and a persona that "knows the race" is created from whatever `context.md` says, not hard-coded.

### 4.1 New stage A: first-listen personas (before analysis, a new workflow `firstlisten.js`)

Three to five distinct **listener personas**, each a separate Sonnet agent in its own context, each given only a **forward-in-time, cumulative feed** of the audio evidence, not the final `music_reading.md`:

- The feed is a sequence of short slices (say 20 to 30 s, reusing the window structure from `listen.js`) revealed one at a time, each with plain-language derived cues only (loudness trend as a shape, which stems are present, whether a voice is speaking, the groove, a transcript or translation if the persona would have one). Each agent writes a short reaction after each slice, committing to what it expects next, and is **not allowed to read ahead**. This is the psychologist's "forward pass", made compulsory by the critic.
- Persona set (generic, parametrised by listener facts, not by video): (1) cold first-timer on a phone, no language or background; (2) a fan of the genre; (3) someone who knows the subject (built from `context.md`, so it only exists when there is context); (4) a working musician or producer; (5) someone who watches with the picture (the viewer).
- Each writes a **first-listen reaction (about 150 words)** and, in a separate agent run with a fresh context, a **repeat-listen reaction** after being given the whole-piece summary: what they now hear that they missed, and what they expect to remember. Personas do not see each other's work at this stage, so the panel's convergence (the devil's warning: "one prior counted six times") is not baked in.
- Output: `analysis/<video>/human/first_<persona>.md` and `repeat_<persona>.md`. Every claim in them is labelled prediction, not testimony; no "I felt".

### 4.2 New stage B: the "afterwards" memory test

A fresh agent for each persona is given **only that persona's own first-listen note** (not the data), a few minutes of "distraction" modelled as a different small task, and then asked: what do you remember, what is the one moment, what was the ending like, what did you not notice? This tests the report's selection against the psychologist's claim that memory is selective and schematic, and shows which moments carry weight. The result sets the **word budget** for stage D (peak, first voice, ending get the words; the middle gets two sentences). Cheap: five short Sonnet agents.

### 4.3 New stage C: translation step and comparison to other music

- **Translator.** An agent reads the measured facts in `music_reading.md` and writes, per fact, "the nearest thing a player says", with its licensing feature (musician, critic). Examples: "grouped in threes against the kick" becomes "it rolls"; "drums vanish 1:24.3, return 1:28.6" becomes "two bars with nothing under the voice, then back on the one". Output: a table `translation.md` of (measurement, plain sentence, licence, equipment caveat).
- **Comparison.** A separate agent finds two or three comparisons to other music or films, each justified by a named stem feature and sourced via the existing `lineage` specialist and research notes; anything unlicensed is dropped. This stays out of the first-listen personas so they remain naive.

### 4.4 `perceive.js`

- Keep it as the data-gathering stage, but add per-segment **"what does the footage make the music mean?"** notes (viewer, round 3) and a plain **"what would a phone viewer see and hear here"** line (equipment).
- Change the viewer prompt from "watch the segment and write observations" to forward-only: segment N's agent gets the notes for segments 1 to N-1 and **not** later ones, so the viewer's reading is cumulative. (It already works in 20 s segments, so this is a small change.)
- Add a "what is the one thing a person would keep from this segment, and could they miss it?" line, which feeds the memory test.

### 4.5 `listen.js`

- Keep the measurement panel and fact-check; it is the checking layer. But make three changes:
  1. **Add specialists for groove and for the listener's body** (does it push or drag, the weight of what a drummer plays, what a loop does to attention). The panel found groove entirely missing from our reports. Say plainly in the prompt that the "feeling" specialist works from the first-listen notes (stage A), not from measurements alone.
  2. **Add a "taught before" check** to the boundary rule in `MUSIC_RULES` rule 3: for every moment described as a surprise, drop, return or ending, list what the listener had been taught in the preceding 30 s (what has been present and for how long), from the stems. This is the mechanism that would have caught the 1:24 "no warning" error.
  3. **Write `music_reading.md` as a sidecar**, not as the source for prose. It keeps its tables. It is no longer the document the writer paraphrases.
- Do not edit `MUSIC_RULES` rules 1, 2 and 4 (production era, blind honesty, end-of-track measurement): they stay as the checks.

### 4.6 `interpret.js`

- The panel and moderator should read the first-listen and repeat-listen notes (stage A) **before** the dossier, and be told to disagree with them where the evidence does; the dossier is the checking layer here.
- Panel personas should match the listener set above and should be told to answer "what would you say to a mate, and what would you remember?" before citing data. Add the devil's-advocate role used in this debate (what is lost, how to keep it without the audit voice), because it caught real problems.
- Ask the moderator for a **"where listeners split"** section (cold, fan, knows-the-subject) instead of a single synthesis.
- Fact-checkers keep their lenses but get one more: **"is this sentence true for the listener it names?"**

### 4.7 `report.js`

This is the stage with most changes.

1. **Inputs.** The writer gets, in this order: the first-listen and repeat-listen notes, the memory test, the translation table and the comparison. It gets `music_reading.md`, `interpretation.md` and the dossier **only as the sidecar source**. This reverses the current "Sources (already fact-checked)" line.
2. **Replace the two tiers** with the structure in 3.1. Main page 600 to 900 words (down from 1,200 to 2,000); the line, front page, forward-in-time first listen, who hears what, afterwards, picture, where it sits, what nobody could hear. Sidecar second, keyed by sentence id.
3. **Rewrite the hard rules.** Keep: no statistics in the body; frames cited for visual claims; absence claims with a real N; `DO_NOT_CLAIM` words; "Where it sits" only from the lineage file and reception notes; context facts tagged. Drop: the "I" first-person section grounded in panel notes (replaced by the named-listener sections); the "write the opening paragraph last" rule (the line must be earned, but it comes first and the writer chooses it from the first-listen notes); the requirement that the limitation be a single sentence (now a paragraph, once). Add: plain-sentence-then-one-image; one bet; no "I felt"; no tags in the body; a verdict with a lean and a for/not-for; "taught, then denied, then paid" for the drop and the ending; the middle gets at most two sentences; the opening line says what it is like.
4. **Change the cold reads.** Keep `truth` and `tiers` (adapted to the sidecar). Replace `feel` with **three human-fit reads**: (a) a persona who has only the report and checks whether each sentence matches the first-listen notes it was meant to come from; (b) a player-test: a musician agent given the stems' plain summary and the draft, asked "which sentences would you not have said?" (musician's cheap test, adopted by the whole panel); (c) a "mate" read: "where does this sound like a committee, a database or a review nobody would print? Quote the lines."
5. **Add a check script** (extend `v1/scripts/check_outputs.py`): fail the body if it contains OBS/INT/H/M/L tags, units, "depends on", "best-supported", more than one image per section, or "I felt", or exceeds the word budget. Keep the existing digit and unit checks.
6. **Ask the user.** The report publishes a two-line prompt at the end of the page: "What stayed with you? Which sentence rang falsest?" The answers go into `v1/analysis/human_listening/real_listener/<video>.md` and are used to score and retune the prompts. This is the only real listener data we will have.

### 4.8 Keep measurement as the checking layer

Nothing is deleted from the measurement stack. It now plays three roles: (a) it **licenses** each human sentence in the sidecar; (b) it **refutes** a human sentence that is wrong (as it did with "no warning"); (c) it **suggests** new things for a human to say (as the musician's "groove in threes" did). The sidecar fact-check is unchanged: if any sentence's licence fails, it is fixed, not defended.

### 4.9 Video-agnostic by construction

No stage names a video, band or event. Personas are templates filled from facts that exist for any video (language heard, whether `context.md` exists, whether there is picture). Where there is no context (blind runs), the "knows the subject" persona is simply not created. Equipment is a parameter ("phone", "headphones", "speakers"), defaulting to phone plus headphones as two separate reads when the music has deep bass.

### 4.10 Order of work

1. Write `firstlisten.js` (stage A and B) and run on `video2`.
2. Write the translation and comparison agents.
3. Rewrite the `report.js` writer prompt, cold reads and check script.
4. Add the groove specialist and "taught before" check to `listen.js`.
5. Forward-only change to `perceive.js` and `interpret.js` reading order.
6. Blind A/B judging of old vs new report on both videos (this is what `human.js` already sets up) and then ask the user for a real data point.

---

## 5. Writing brief for the writer agent (one paragraph)

Write a short piece (600 to 900 words of main text) for an intelligent stranger who has not heard the music, in British English and in the voice of someone who has just listened to it with them. Open with one plain sentence that says what it is like, then give a verdict and a lean (who it is for, who it is not for), the one moment they will remember and the ending, all in a front page of about 300 words; then walk through it forward in time as a first-time listener who does not yet know what is coming, saying what the music has taught you to expect, what happens, and what it does, giving the opening, the first voice, the turning point and the ending most of the words and the long middle two honest sentences about what people do there and where they split. Use "you" for named kinds of listener (a cold first-timer on a phone, a fan, someone who knows the subject) and say what each would hear, as a prediction a real person could confirm or deny, with plain confidence words ("probably", "surely") and never "I felt", never a number you cannot count by ear, never a decibel, tempo figure, p-value, tag or "depends on what you bring"; put the plain sentence first and at most one image after it, and compare to other music only when a feature you can name licenses it, otherwise reach for a gait, a room or the weather. Own one bet and let it be wrong. Where the picture matters, say what the footage makes the music mean. Say once, in one honest paragraph near the end, what nobody here could hear (the weight of the kick, the grain of the voice, whether any of it moved us) and that the reader's own ear has the final vote, and then stop apologising. Every sentence must have an id and a row in the sidecar giving its timestamp, measurement, mechanism and confidence, and any sentence the sidecar cannot license must be cut or softened.

---

## 6. Open questions for the user

1. Is the problem that the reports are **wrong**, or that they are written in the wrong **voice** even when they are right? The panel assumed the second. If it is the first, parts of this are cosmetic.
2. One real sentence about what stayed with you after Part 2, and one about which sentence in our report rang falsest. The panel's mood converged fast (the devil's warning that this may be one prior counted six times); one human sentence outweighs another round of us agreeing with each other.
