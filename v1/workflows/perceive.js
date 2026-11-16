export const meta = {
  name: 'v1-perceive',
  description: 'Video-agnostic: watch each video segment by segment, read music + words; write human-style observations to v1/analysis/perceive/<video>/',
  phases: [
    { title: 'Watch', detail: 'one Sonnet viewer per 20 s segment' },
    { title: 'Listen', detail: 'music + words agents per video' },
  ],
}
// args: { videos: [{ vid: 'video1', dur: 188.7 }, ...], skip_done: [ 'video1:seg_01', ... ] }
const R = '/home/user/Listener'
const A = `${R}/v1/analysis`
const SUM = { type: 'object', properties: { summary: { type: 'string' }, open_questions: { type: 'array', items: { type: 'string' } } }, required: ['summary', 'open_questions'] }
const common = vid => `
You are part of a team analysing music videos the way a thoughtful HUMAN viewer would: what you see, hear, feel, and what it means.
Repo: ${R}. This task is about videos/${vid}.mp4. FIRST read v1/data/${vid}/context.md (known facts about this video: subject, artist, sources). Treat it as a lead to verify, not gospel.
Extracted material lives in v1/data/${vid}/:
- contact_sheets/sheet_NN.jpg: 5x4 grids, one frame per second, timestamp burned in; sheet NN covers seconds (NN-1)*20 .. NN*20-1.
- frames_1fps/f_NNNN.jpg: frame at second NNNN-1 (f_0001 = 0 s). Open individual frames to look closely.
- scenes/shots.json + scenes/keyframes/: detected cuts with a mid-shot keyframe each.
- lyrics/*.txt: whisper transcripts (may be wrong, especially names and non-English speech; correct with judgement and say so).
- audio_features/summary.json (tempo, key estimate, auto sections, per-second loudness/brightness/onset), overview.png, spectrogram.png.
- visual_features/per_second.json (brightness, saturation, warmth, motion, faces, dominant colours), overview.png, colour_barcode.png, cut_beat_alignment.json.
- stems/ (if present): per-second loudness of vocals/drums/bass/other from source separation, stems.png.
- v1/analysis/research/ may hold background research; use it.
You cannot play audio; infer the music from spectrogram/features/stems/transcripts and say how confident you are.
Write in clear English with British spelling. Be concrete and timestamped (m:ss). Separate OBSERVATION from INTERPRETATION and label speculation. Accuracy matters more than eloquence: never invent details you did not see.
Use the Read tool to view images. Write your output file with the Write tool, then return a short summary.`

const pad = n => String(n).padStart(2, '0')
const mmss = s => `${Math.floor(s / 60)}:${pad(Math.floor(s % 60))}`
const skip = new Set(args.skip_done || [])
const SEGS = []
for (const { vid, dur } of args.videos) for (let n = 1; (n - 1) * 20 < dur; n++) if (!skip.has(`${vid}:seg_${pad(n)}`)) SEGS.push({ vid, n, from: (n - 1) * 20, to: Math.min(n * 20, Math.ceil(dur)) })

const watch = s => agent(`${common(s.vid)}

YOUR JOB: be the eyes for ${s.vid}, seconds ${s.from}-${s.to} (${mmss(s.from)}-${mmss(s.to)}).
1. Read v1/data/${s.vid}/contact_sheets/sheet_${pad(s.n)}.jpg.
2. Read the keyframes for shots overlapping this range (see shots.json), and open 1 fps frames wherever something deserves a close look (faces, expressions, text, signs, crowds, objects, transitions). Look at at least 8 individual images.
3. Read the transcript lines and the per-second audio/visual features for this range.
4. Write ${A}/perceive/${s.vid}/seg_${pad(s.n)}.md with sections:
   - Shot-by-shot description (time, what we see, framing/camera movement, archival vs newly shot, colour/b&w, texture, any editing effects)
   - People (age, clothing, expression, action), places, objects, on-screen text (transcribe and translate it)
   - Sound in this stretch: words (original + translation), music energy, how picture and sound line up (cuts on beats? images echoing words? contrast?)
   - What a viewer feels here and why
   - Symbols, motifs, visual rhymes worth tracking across the film
   - Open questions for the team`, { label: `watch:${s.vid}:${pad(s.n)}`, phase: 'Watch', model: 'sonnet', schema: SUM })

const aux = args.videos.flatMap(({ vid }) => [
  ...(skip.has(`${vid}:music`) ? [] : [() => agent(`${common(vid)}

YOUR JOB: be the ears (music) for ${vid}. Study audio_features/, stems/ if present, the beat/cut alignment and the transcripts.
Run Python (librosa, numpy installed) on v1/data/${vid}/audio/song.wav to measure more: e.g. librosa.effects.hpss percussive vs harmonic energy per section, band energies (sub-bass, guitars/mids, cymbals), drops, silences, build-ups, resolve tempo octave ambiguity, key changes, stereo width (song.wav is stereo), dynamics. Save helper scripts under v1/scripts/agents/ and outputs under v1/data/${vid}/audio_features/extra/.
Write ${A}/perceive/${vid}/music.md: genre, instrumentation (with evidence), structure map with timestamps, emotional arc, how the music frames the words, moments a listener would remember. State confidence for each claim.`, { label: `listen:${vid}`, phase: 'Listen', model: 'sonnet', schema: SUM })]),
  ...(skip.has(`${vid}:words`) ? [] : [() => agent(`${common(vid)}

YOUR JOB: the words for ${vid}. Build the best possible transcript of every spoken or sung word, with timestamps, original language and English.
Compare all transcripts in v1/data/${vid}/lyrics/. Re-run faster-whisper yourself on specific short windows where needed (model "medium" or "large-v3", device cpu, compute_type int8; load audio with librosa.load(path, sr=16000, offset=..., duration=...) and pass the numpy array, because the PyAV path is broken). Use language hints and initial_prompt with likely names from context.md. If v1/data/${vid}/stems_raw/htdemucs/song/vocals.wav exists, transcribe that too: it removes the music. The CPU is slow, so keep windows short.
Write ${A}/perceive/${vid}/words.md: a clean timestamped table (time, original, English, confidence, notes), who seems to be speaking (narrator, reporter, interviewee, singer?), recording era and quality, and which phrases carry emotional or thematic weight.`, { label: `words:${vid}`, phase: 'Listen', model: 'sonnet', schema: SUM })]),
])

phase('Watch')
const all = await parallel([...SEGS.map(s => () => watch(s)), ...aux])
log(`${all.filter(Boolean).length}/${all.length} agents returned`)
return all.map((r, i) => ({ id: i < SEGS.length ? `${SEGS[i].vid}:seg_${pad(SEGS[i].n)}` : `aux_${i - SEGS.length}`, ...(r || { summary: 'FAILED', open_questions: [] }) }))
