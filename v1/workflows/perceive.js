export const meta = {
  name: 'v1-perceive',
  description: 'Video-agnostic: watch each video segment by segment, read music + words; write human-style observations to v1/analysis/perceive/<video>/',
  phases: [
    { title: 'Watch', detail: 'one Sonnet viewer per 20 s segment' },
    { title: 'Listen', detail: 'music + words agents per video' },
  ],
}
// args: { root: optional repo root, videos: ['video1', ...] or [{ vid: 'video1', dur: 188.7 }, ...] (dur read from audio_features/summary.json when omitted), skip_done: [ 'video1:seg_01', ... ], blind: false, out: 'analysis', video_dir: 'videos' }
// Root: no fallback. R is args.root, else the literal /home/user/Listener (not derived from the script location). Pass args.root for another checkout.
const R = (args && args.root) || '/home/user/Listener'  // Workflow scripts have no Node APIs (__dirname/process undefined); pass args.root for another checkout
// Preflight: fail loudly before any agent is launched if the root is wrong (no fallback; default is the literal /home/user/Listener, pass args.root).
const ROOT_PROBE = `${R}/v1/scripts/check_outputs.py`
const ROOT_SCHEMA = { type: 'object', properties: { exists: { type: 'boolean' } }, required: ['exists'] }
const rootProbe = await agent(`Report whether this file exists (use ls or stat; do not read or edit it): ${ROOT_PROBE}`, { label: 'preflight:root', phase: 'Watch', model: 'sonnet', effort: 'low', schema: ROOT_SCHEMA })
if (!(rootProbe && rootProbe.exists)) throw new Error(`perceive.js: ${ROOT_PROBE} not found, so root "${R}" is wrong (pass args.root = the repo path)`)
const A = `${R}/v1/${args.out || 'analysis'}`
const BLIND = !!args.blind
// Accept bare names or {vid, dur}; when dur is omitted an agent reads duration_s from v1/data/<vid>/audio_features/summary.json.
async function resolveVideos(list) {
  const vs = (list || []).map(v => (typeof v === 'string' ? { vid: v } : { ...v }))
  const need = vs.filter(v => !(v.dur > 0))
  if (need.length) {
    const got = await agent(`Read "duration_s" from ${R}/v1/data/<vid>/audio_features/summary.json for each of these videos: ${need.map(v => v.vid).join(', ')}. Return the numbers exactly as stored (do not invent any; omit a video whose file is missing).`, { label: 'durations', model: 'sonnet', effort: 'low', schema: { type: 'object', properties: { durations: { type: 'array', items: { type: 'object', properties: { vid: { type: 'string' }, dur: { type: 'number' } }, required: ['vid', 'dur'] } } }, required: ['durations'] } })
    for (const v of need) { const g = got && got.durations.find(d => d.vid === v.vid); if (g && g.dur > 0) v.dur = g.dur }
    const bad = need.filter(v => !(v.dur > 0)).map(v => v.vid)
    if (bad.length) throw new Error(`No duration for: ${bad.join(', ')} (pass {vid,dur} or run 04_audio_features.py first)`)
  }
  return vs
}
const VIDEOS = await resolveVideos(args.videos)
const SUM = { type: 'object', properties: { summary: { type: 'string' }, open_questions: { type: 'array', items: { type: 'string' } } }, required: ['summary', 'open_questions'] }
const common = vid => `
You are part of a team analysing music videos the way a thoughtful HUMAN viewer would: what you see, hear, feel, and what it means.
Repo: ${R}. This task is about ${(args.video_dir || 'videos')}/${vid}.mp4. ${BLIND ? 'BLIND MODE: do NOT read context.md, anything under v1/analysis/ (other than your own output folder ' + A + '), or use the web. Work only from what can be seen and heard in the extracted data, as a viewer with no background information would.' : 'FIRST read v1/data/' + vid + '/context.md (known facts about this video: subject, artist, sources). Treat it as a lead to verify, not gospel.'}
Extracted material lives in v1/data/${vid}/:
- contact_sheets/sheet_NN.jpg: 5x4 grids, one frame per second, timestamp burned in; sheet NN covers seconds (NN-1)*20 .. NN*20-1.
- frames_1fps/f_NNNN.jpg: frame at second NNNN-1 (f_0001 = 0 s). Open individual frames to look closely.
- scenes/shots.json + scenes/keyframes/: detected cuts with a mid-shot keyframe each.
- lyrics/*.txt: whisper transcripts (may be wrong, especially names and non-English speech; correct with judgement and say so).
- audio_features/summary.json (tempo, key estimate, auto sections, per-second loudness/brightness/onset), overview.png, spectrogram.png.
- visual_features/per_second.json (brightness, saturation, warmth, motion, faces, dominant colours), overview.png, colour_barcode.png, cut_beat_alignment.json.
- sync/sync.json + sync.png (if present): measured music-picture relationship (cut/beat phase locking, cut rate vs loudness, motion vs onsets).
- stems/ (if present): per-second loudness of vocals/drums/bass/other from source separation, stems.png.
${BLIND ? '' : '- v1/analysis/research/ may hold background research; use it.'}
You cannot play audio; infer the music from spectrogram/features/stems/transcripts and say how confident you are.
Write in clear English with British spelling. Be concrete and timestamped (m:ss). Separate OBSERVATION from INTERPRETATION and label speculation. Accuracy matters more than eloquence: never invent details you did not see.
PICTURE-READING RULES (apply to every claim about frames; standing list in ${R}/v1/DO_NOT_CLAIM.md, read it first and do not make those claims):
a) Open the frame at FULL SIZE (Read the individual f_NNNN.jpg, not only the contact sheet) before interpreting it. For each pivotal frame (a gesture, a look, a sign, a banner, a face, a turning point) write a two-field note: "literal: what is visible at full size" (colours, shapes, positions, legible print, no meaning) then "reading: your interpretation". Never merge the two fields.
b) Quote only print that is legible at full size. Everything else goes in a list headed 'unread' (say where it is and what can be seen of it, e.g. 'unread: white capitals on a dark board, first word blurred'). Never complete or correct a name, number or word from research, context or transcripts.
c) Tag every claim OBSERVED (seen or heard in the frames/data this session), INFERRED (follows from observations; say from which) or SPECULATED (a guess). Keep the tag on each claim, including in the summary.
${BLIND ? 'd) Blind mode: you have no background; do not name an event, person or place unless print or speech you can read or hear says so, and tag any identification INFERRED with the clues.' : 'd) ANTI-PRIMING: context.md can bias your eyes. Check every visual claim against the frames BEFORE you consult context.md for it: first write what the pixels show, then, only if useful, compare with context.md. Tag any claim that comes from context rather than pixels as FROM-CONTEXT (with the context.md line), and never let it support an OBSERVED claim. If frames and context disagree, report the frames and flag the disagreement.'}
Use the Read tool to view images. Write your output file with the Write tool, then return a short summary.`

const pad = n => String(n).padStart(2, '0')
const mmss = s => `${Math.floor(s / 60)}:${pad(Math.floor(s % 60))}`
const skip = new Set(args.skip_done || [])
const SEGS = []
for (const { vid, dur } of VIDEOS) for (let n = 1; (n - 1) * 20 < dur; n++) if (!skip.has(`${vid}:seg_${pad(n)}`)) SEGS.push({ vid, n, from: (n - 1) * 20, to: Math.min(n * 20, Math.ceil(dur)) })

const watch = s => agent(`${common(s.vid)}

YOUR JOB: be the eyes for ${s.vid}, seconds ${s.from}-${s.to} (${mmss(s.from)}-${mmss(s.to)}).
1. Read v1/data/${s.vid}/contact_sheets/sheet_${pad(s.n)}.jpg.
2. Read the keyframes for shots overlapping this range (see shots.json), and open 1 fps frames wherever something deserves a close look (faces, expressions, text, signs, crowds, objects, transitions). Look at at least 8 individual images, each at full size, following the PICTURE-READING RULES (literal then reading; legible print only, the rest 'unread'; OBSERVED/INFERRED/SPECULATED per claim; DO_NOT_CLAIM.md).
3. Read the transcript lines and the per-second audio/visual features for this range.
4. Write ${A}/perceive/${s.vid}/seg_${pad(s.n)}.md with sections:
   - Shot-by-shot description (time, what we see, framing/camera movement, archival vs newly shot, colour/b&w, texture, any editing effects)
   - Pivotal frames: for each, 'f_NNNN literal: ...' then 'reading: ...' (tagged OBSERVED/INFERRED/SPECULATED)
   - People (clothing, posture, action; no age, sex or role unless clearly shown, see DO_NOT_CLAIM.md), places, objects, on-screen text (transcribe and translate only the legible print; list the rest under 'unread')
   - Sound in this stretch: words (original + translation), music energy, how picture and sound line up (cuts on beats? images echoing words? contrast?)
   - What a viewer feels here and why
   - Symbols, motifs, visual rhymes worth tracking across the film
   - Open questions for the team (include every 'unread' item and anything needing a frame at an exact time)`, { label: `watch:${s.vid}:${pad(s.n)}`, phase: 'Watch', model: 'sonnet', schema: SUM })

const aux = VIDEOS.flatMap(({ vid }) => [
  ...(skip.has(`${vid}:music`) ? [] : [() => agent(`${common(vid)}

YOUR JOB: be the ears (music) for ${vid}. Study audio_features/, stems/ if present, the beat/cut alignment and the transcripts.
Run Python (librosa, numpy installed) on v1/data/${vid}/audio/song.wav to measure more: e.g. librosa.effects.hpss percussive vs harmonic energy per section, band energies (sub-bass, guitars/mids, cymbals), drops, silences, build-ups, resolve tempo octave ambiguity, key changes, stereo width (song.wav is stereo), dynamics. Save helper scripts under v1/scripts/agents/ and outputs under v1/data/${vid}/audio_features/extra/.
Tag each claim OBSERVED/INFERRED/SPECULATED; do not make the claims in ${R}/v1/DO_NOT_CLAIM.md; if you open frames, record 'literal' before 'reading' and list illegible print as 'unread'.
Write ${A}/perceive/${vid}/music.md: genre, instrumentation (with evidence), structure map with timestamps, emotional arc, how the music frames the words, moments a listener would remember. State confidence for each claim.`, { label: `listen:${vid}`, phase: 'Listen', model: 'sonnet', schema: SUM })]),
  ...(skip.has(`${vid}:words`) ? [] : [() => agent(`${common(vid)}

YOUR JOB: the words for ${vid}. Build the best possible transcript of every spoken or sung word, with timestamps, original language and English.
Compare all transcripts in v1/data/${vid}/lyrics/. Re-run faster-whisper yourself on specific short windows where needed (model "medium" or "large-v3", device cpu, compute_type int8; load audio with librosa.load(path, sr=16000, offset=..., duration=...) and pass the numpy array, because the PyAV path is broken). ${BLIND ? 'Detect the language yourself.' : 'Use language hints and initial_prompt with likely names from context.md.'} If v1/data/${vid}/stems_raw/htdemucs/song/vocals.wav exists, transcribe that too: it removes the music. The CPU is slow, so keep windows short.
Any on-screen print you cite must be legible at full size in a frame you opened; otherwise list it as 'unread' and never complete names from context or research (see ${R}/v1/DO_NOT_CLAIM.md). Tag claims OBSERVED/INFERRED/SPECULATED.
Write ${A}/perceive/${vid}/words.md: a clean timestamped table (time, original, English, confidence, notes), who seems to be speaking (narrator, reporter, interviewee, singer?), recording era and quality, and which phrases carry emotional or thematic weight.`, { label: `words:${vid}`, phase: 'Listen', model: 'sonnet', schema: SUM })]),
])

phase('Watch')
const all = await parallel([...SEGS.map(s => () => watch(s)), ...aux])
log(`${all.filter(Boolean).length}/${all.length} agents returned`)
return all.map((r, i) => ({ id: i < SEGS.length ? `${SEGS[i].vid}:seg_${pad(SEGS[i].n)}` : `aux_${i - SEGS.length}`, ...(r || { summary: 'FAILED', open_questions: [] }) }))
