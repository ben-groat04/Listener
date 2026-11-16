export const meta = {
  name: 'v1-perceive',
  description: 'Watch both music videos segment by segment, read the music and narration, research context; write raw human-style observations',
  phases: [
    { title: 'Watch', detail: 'one Sonnet viewer per 20 s segment of each video' },
    { title: 'Listen', detail: 'music + narration agents per video' },
    { title: 'Research', detail: 'history, artist/song identification, cultural meaning' },
  ],
}

const R = '/home/user/Listener'
const A = `${R}/v1/analysis`
const SUM = { type: 'object', properties: { summary: { type: 'string' }, open_questions: { type: 'array', items: { type: 'string' } } }, required: ['summary', 'open_questions'] }
const COMMON = `
You are part of a team analysing two music videos the way a thoughtful HUMAN viewer would: what you see, hear, feel, and what it means.
Repo: ${R}. Videos: videos/video1.mp4 (the predecessor, 188.7 s) and videos/video2.mp4 (the main one, 305.9 s).
Extracted material for each video lives in v1/data/<video>/:
- contact_sheets/sheet_NN.jpg: 5x4 grids, one frame per second, timestamp burned in; sheet NN covers seconds (NN-1)*20 .. NN*20-1.
- frames_1fps/f_NNNN.jpg: frame at second NNNN-1 (f_0001 = 0 s). Open individual frames to look closely.
- scenes/shots.json + scenes/keyframes/: detected cuts with a mid-shot keyframe each.
- lyrics/*.txt: whisper transcripts (Dutch "nl_transcribe" and English "nl_translate"; earlier "small_mix" pass is rough). Whisper makes mistakes with Dutch names; correct them with judgement.
- audio_features/summary.json (tempo, key estimate, auto sections, per-second loudness/brightness/onset), overview.png, spectrogram.png.
- visual_features/per_second.json (brightness, saturation, warmth, motion, faces, dominant colours), overview.png, colour_barcode.png, cut_beat_alignment.json.
Early hint (verify, don't assume): the spoken audio seems to be Dutch archival narration about the Elfstedentocht skating race of 18 January 1963.
You cannot play audio; infer the music from spectrogram/features/transcripts and say how confident you are.
Write in clear English. Be concrete and timestamped (m:ss). Separate OBSERVATION (what is there) from INTERPRETATION (what it might mean) and label speculation.
Use the Read tool to view images. Write your output file with the Write tool, then return a short summary.`

function segments(vid, dur) {
  const out = []
  for (let n = 1; (n - 1) * 20 < dur; n++) out.push({ vid, n, from: (n - 1) * 20, to: Math.min(n * 20, Math.ceil(dur)) })
  return out
}
const SEGS = [...segments('video1', 188.7), ...segments('video2', 305.9)]
const pad = n => String(n).padStart(2, '0')
const mmss = s => `${Math.floor(s / 60)}:${pad(Math.floor(s % 60))}`

const watch = s => agent(`${COMMON}

YOUR JOB: be the eyes for ${s.vid}, seconds ${s.from}-${s.to} (${mmss(s.from)}-${mmss(s.to)}).
1. Read v1/data/${s.vid}/contact_sheets/sheet_${pad(s.n)}.jpg.
2. Read the keyframes in v1/data/${s.vid}/scenes/ for shots overlapping this range (check shots.json), and open 1 fps frames wherever something deserves a close look (faces, text, signs, crowds, objects, transitions). Look at at least 8 individual images.
3. Read the transcript lines and the per-second audio/visual features for this range.
4. Write ${A}/perceive/${s.vid}/seg_${pad(s.n)}.md with sections:
   - Shot-by-shot description (time, what we see, framing/camera, archival vs newly shot, colour/black-and-white, texture/grain)
   - People, places, objects, any on-screen text (transcribe it)
   - Sound in this stretch: narration (Dutch + translation), music energy, how picture and sound line up (cuts on beats? image echoing words?)
   - What a viewer feels here and why
   - Symbols, motifs, visual rhymes worth tracking across the film
   - Open questions for the team`, { label: `watch:${s.vid}:${pad(s.n)}`, phase: 'Watch', model: 'sonnet', schema: SUM })

const listeners = ['video1', 'video2'].flatMap(vid => [
  () => agent(`${COMMON}

YOUR JOB: be the ears (music) for ${vid}. Study v1/data/${vid}/audio_features/ (summary.json, overview.png, spectrogram.png), the beat/cut alignment, and the transcripts.
You may run Python (librosa, numpy are installed) on v1/data/${vid}/audio/song.wav to measure more: e.g. per-section instrumentation clues (spectral bands, percussive vs harmonic via librosa.effects.hpss), drops, silences, build-ups, tempo (resolve the 80 vs 160 BPM ambiguity), key changes, stereo width, dynamics. Save any helper script under v1/scripts/agents/ and outputs under v1/data/${vid}/audio_features/extra/.
Write ${A}/perceive/${vid}/music.md: genre guess, instrumentation guess, structure map with timestamps (intro/build/drop/etc.), emotional arc, how the music frames the narration, notable moments a listener would remember. State confidence.`, { label: `listen:${vid}`, phase: 'Listen', model: 'sonnet', schema: SUM }),
  () => agent(`${COMMON}

YOUR JOB: the words for ${vid}. Build the best possible transcript of every spoken or sung word, with timestamps, in the original language and in English.
Compare all transcripts in v1/data/${vid}/lyrics/. If useful, re-run faster-whisper yourself (model "medium" or "large-v3", device cpu, compute_type int8, feed numpy audio via librosa.load(...,sr=16000) because the PyAV path is broken) on specific time windows, e.g. with language="nl", initial_prompt containing likely names (Elfstedentocht, Leeuwarden, Dokkum, Bartlehiem, Reinier Paping, Friesland, etc.). Only run whisper on short windows; the CPU is slow.
Write ${A}/perceive/${vid}/words.md: a clean timestamped table (time, original, English, confidence, notes), who seems to be speaking (newsreel narrator? radio reporter? interviewee? sung vocal?), what era the recordings sound like, and which phrases carry emotional or thematic weight.`, { label: `words:${vid}`, phase: 'Listen', model: 'sonnet', schema: SUM }),
])

const research = [
  ['history', `Research the Elfstedentocht of 18 January 1963 (the "Hel van '63"): conditions, route, winner (Reinier Paping?), how few finished, famous images and stories, newsreel/radio coverage (Polygoon?), and the Elfstedentocht's place in Dutch identity, including that it has not been held since 1997 and the climate-change angle. Use WebSearch/WebFetch (load them with ToolSearch). Cite URLs. Write ${A}/research/elfstedentocht_1963.md.`],
  ['artist', `Try to identify the artist and the two tracks. Clues: music videos built on Dutch archival narration about the 1963 Elfstedentocht; video1 is the "predecessor" (188.7 s), video2 the follow-up (305.9 s); a sung/chanted section in video2 ~3:32-3:58 includes words like "stuck", "end of the road", "climbing up". Read v1/data/*/lyrics/*.txt for more clues. Search the web (WebSearch/WebFetch via ToolSearch) for bands that make songs from archival samples about the Elfstedentocht (e.g. check Public Service Broadcasting and others, but do not assume). Look at the first and last contact sheets of each video for titles/credits. Report candidates with evidence and confidence; if found, gather official info (album, release year, track titles, what the artist said about the songs). Write ${A}/research/artist_and_tracks.md.`],
  ['culture', `Write the cultural-reading brief a Dutch viewer would bring: what the Elfstedentocht means (Frisian identity, "it giet oan", the "kruisje" stamp cards, the 200 km route, the 11 cities, heroism of ordinary people, frozen toes, nostalgia, winters that no longer come), how archival footage + modern electronic music works as a genre (hauntology, nostalgia, sample-based storytelling), and what themes a music video on this subject would likely be reaching for. Use web sources where helpful (WebSearch via ToolSearch) and cite them. Write ${A}/research/cultural_context.md.`],
].map(([k, p]) => () => agent(`${COMMON}\n\nYOUR JOB (${k}): ${p}`, { label: `research:${k}`, phase: 'Research', model: 'sonnet', schema: SUM }))

phase('Watch')
const all = await parallel([...SEGS.map(s => () => watch(s)), ...listeners, ...research])
const results = all.map((r, i) => ({ id: i < SEGS.length ? `${SEGS[i].vid}:seg_${pad(SEGS[i].n)}` : `aux_${i - SEGS.length}`, ...(r || { summary: 'FAILED', open_questions: [] }) }))
log(`${results.filter(r => r.summary !== 'FAILED').length}/${results.length} agents succeeded`)
return results
