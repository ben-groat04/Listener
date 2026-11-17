export const meta = {
  name: 'v1-blind-chain',
  description: 'Blind end-to-end run (no context, no research, no web): perceive -> listen -> identify -> freeze blind claims -> interpret, output to v1/analysis_blind/, then a leak check; optional blind-first informed extension and blindcmp final stage',
  phases: [{ title: 'Blind perceive' }, { title: 'Blind listen' }, { title: 'Identification' }, { title: 'Blind interpret' }, { title: 'Leak check' }, { title: 'Informed extension' }, { title: 'Compare' }],
}
// args: { root: optional repo root, videos: ['video1'] or [{vid, dur}] (dur auto-read when omitted), video_dir: 'videos',
//         blind_first: false, compare_after: false, informed_rounds: 3 }
// Root: args.root, else two directories up from this script (v1/workflows), else the working directory.
//
// Default (blind_first falsy): perceive -> listen -> identification -> freeze -> interpret -> leak check, all blind.
//
// IDENTIFICATION (L1/L3/L16): after perceive/listen, one blind agent per video names its top THREE candidate identifications
//   (event, era, kind of production), each with converging clues, a confidence word and the tag INFERRED. Proper nouns (places,
//   names, titles) need ASR convergence: two independent passes (e.g. Whisper transcribe and translate, or a transcript plus
//   on-screen text) must agree on the sound/spelling; otherwise they are written as 'heard as ...' not as fact. Failing to name an
//   event the evidence makes near-certain is a DEFECT: blind runs must not refuse to say what they clearly heard or saw.
// FREEZE: before any research, v1/data/<vid>/blind_frozen.md is written (subject, date, place, structure times, top moments, each
//   with a confidence tag) and made read-only (chmod a-w). Later stages may read it but must never edit it.
//   v1/data/<vid>/unknowns.md lists what the blind lane could not settle: it is the informed lane's research agenda.
// blind_first: true -> after the blind stages and leak check, an informed lane researches the unknowns (web allowed, context.md
//   allowed) and writes v1/data/<vid>/informed_extension.md, then runs interpret.js unblinded into v1/analysis/. The informed lane
//   EXTENDS the frozen claims (adds, confirms, or lists a disagreement beside them); it never rewrites them.
//   PREREQUISITE: interpret.js reads informed perceive/listen outputs (v1/analysis/perceive, v1/analysis/music/<vid>); for a video that
//   has none yet, run perceive.js and listen.js with {out:'analysis', blind:false} first (this chain does not do it, to avoid overwriting).
// compare_after: true -> blindcmp.js is the final stage (the documented default final stage for any blind-first run; set it true
//   there). It diffs frozen claims against informed outputs on time/count claims and decides disagreements from raw data in
//   v1/data/<vid>/, not from either side's say-so.
// The leak check always runs: blind outputs (including blind_frozen.md) must not contain context-only facts unless the term is
//   supported by a quoted ASR/on-screen source, which the check records.
const R = (args && args.root) || '/home/user/Listener'  // Workflow scripts have no Node APIs (__dirname/process undefined); pass args.root for another checkout
const W = `${R}/v1/workflows`
const common = { blind: true, out: 'analysis_blind', video_dir: args.video_dir || 'videos', root: R }
const VID_NAMES = (args.videos || []).map(v => (typeof v === 'string' ? v : v.vid))
const BLIND_RULES = `BLIND RULES: do not read v1/data/<vid>/context.md, v1/analysis/ (informed work), v1/analysis/research/, or use the web. Use only the raw data in v1/data/<vid>/ and v1/analysis_blind/.`
phase('Blind perceive')
await workflow({ scriptPath: `${W}/perceive.js` }, { ...common, videos: args.videos })
phase('Blind listen')
await workflow({ scriptPath: `${W}/listen.js` }, { ...common, videos: args.videos, rounds: 2 })

// Identification (L1, L3, L16) then freeze (L13 partial). Blind: no context, no web.
phase('Identification')
const IDENT = { type: 'object', properties: { candidates: { type: 'array', items: { type: 'object', properties: { event: { type: 'string' }, era: { type: 'string' }, production_kind: { type: 'string' }, clues: { type: 'array', items: { type: 'string' } }, confidence: { type: 'string' } }, required: ['event', 'era', 'production_kind', 'clues', 'confidence'] } }, frozen_written: { type: 'boolean' }, unknowns_written: { type: 'boolean' }, summary: { type: 'string' } }, required: ['candidates', 'frozen_written', 'unknowns_written', 'summary'] }
const ident = await parallel(VID_NAMES.map(vid => () => agent(`Identification and freeze for ${vid} (repo ${R}). ${BLIND_RULES}
Read the blind perceive and listen outputs for ${vid} in ${R}/v1/analysis_blind/ and check key points against raw data in ${R}/v1/data/${vid}/ (lyrics/ASR files, scenes/shots.json, frames, music_views, sync).
1. IDENTIFICATION. Give your top THREE candidate identifications of: the event or subject shown, the era, and the kind of production (e.g. archival film with a later soundtrack, original promo, amateur footage). For each: converging clues (quote the file/time or frame/ASR line behind each), a confidence word (near-certain / probable / possible), tagged INFERRED.
2. ASR CONVERGENCE RULE for proper nouns (places, names, titles, languages): state a proper noun as fact only if two independent sources agree on it (e.g. transcribe and translate passes, or ASR plus on-screen lettering you can see in a frame). A single noisy pass gives 'heard as "..."', never a bare name.
3. NO REFUSAL. If the evidence makes the event near-certain, name it plainly. Failing to name a near-certain event, or saying 'cannot determine' about what you clearly heard or saw, is a defect. Equally, do not name what the data does not support.
4. FREEZE. Write ${R}/v1/data/${vid}/blind_frozen.md containing: subject; date or era; place; structure with start/end times in seconds (m:ss too); the top moments with times; and next to EVERY claim a confidence tag (OBSERVED / INFERRED / SPECULATIVE plus near-certain/probable/possible). Time and count claims must be re-derived from the raw JSON/CSV, not copied from prose. Then run: chmod a-w ${R}/v1/data/${vid}/blind_frozen.md. If the file already exists and is read-only, do NOT overwrite it: report frozen_written=false.
5. UNKNOWNS. Write ${R}/v1/data/${vid}/unknowns.md: one bullet per thing the blind lane could not settle (names, dates, places, who/why, what a word was, which count is right), each phrased as a question the informed lane could research, with what the blind run thought and why it is unsure. This is the informed lane's research agenda.
Never write to any other file. British English. Return the candidates and flags.`, { label: `identify:${vid}`, phase: 'Identification', model: 'sonnet', schema: IDENT })))

phase('Blind interpret')
const r = await workflow({ scriptPath: `${W}/interpret.js` }, { ...common, videos: VID_NAMES, rounds: 3 })

// Leak check: blind outputs must not contain facts that only context.md knows (artist, commission, MusicBrainz, part number).
phase('Leak check')
const LEAK = { type: 'object', properties: { terms: { type: 'array', items: { type: 'string' } }, hits: { type: 'array', items: { type: 'object', properties: { file: { type: 'string' }, line: { type: 'integer' }, term: { type: 'string' }, text: { type: 'string' } }, required: ['file', 'term', 'text'] } } }, required: ['terms', 'hits'] }
const leaks = await parallel(VID_NAMES.map(vid => () => agent(`Leak check for ${vid} (repo ${R}). You are the only agent allowed to read v1/data/${vid}/context.md in this blind run, and only to extract terms.
1. Read v1/data/${vid}/context.md and list the context-only terms: the artist/band name and member names, the track title, the commissioning body/festival/event, the archive source, plus always 'MusicBrainz' and 'Part 1' / 'Part One' / 'Part 2' / 'Part Two' (case-insensitive).
2. grep -rniF for each term in ${R}/v1/analysis_blind/ (all files for ${vid}: perceive/${vid}, music/${vid}, ${vid}/, and compare/ if present; skip leak_check files) and in ${R}/v1/data/${vid}/blind_frozen.md and ${R}/v1/data/${vid}/unknowns.md.
3. For each hit, note whether the blind text quotes an on-screen or ASR source for the term (a legitimate identification) or not (a leak).
4. Write ${R}/v1/analysis_blind/leak_check_${vid}.md listing terms searched and every hit (file:line, term, the line, supported/unsupported), or "no hits".
Return the terms and hits. Do NOT edit any blind output (blind_frozen.md is read-only).`, { label: `leak:${vid}`, phase: 'Leak check', model: 'sonnet', effort: 'low', schema: LEAK })))
const hits = leaks.filter(Boolean).flatMap(l => l.hits)
log(`leak check: ${hits.length} hit(s) in blind outputs${hits.length ? ' - see v1/analysis_blind/leak_check_<video>.md' : ''}`)

// Blind-first informed lane: research the unknowns, extend (never rewrite) the frozen claims.
let informed = null
if (args.blind_first) {
  phase('Informed extension')
  await parallel(VID_NAMES.map(vid => () => agent(`Informed extension for ${vid} (repo ${R}). The blind lane is finished and its claims are frozen in ${R}/v1/data/${vid}/blind_frozen.md (read-only: never edit, rename or delete it).
1. Read blind_frozen.md, unknowns.md and context.md; research the unknowns (web allowed). Verify against raw data in ${R}/v1/data/${vid}/ before writing any time or count.
2. Write ${R}/v1/data/${vid}/informed_extension.md: for each frozen claim say CONFIRMED / EXTENDED (new detail added beside it) / DISAGREES (give both versions and your evidence); answer each unknown with source and confidence, or leave it open. Extend, never rewrite: a frozen claim stays as the blind lane wrote it.
Mark what came from research versus from the data. British English. Never invent. Return a short summary.`, { label: `informed-ext:${vid}`, phase: 'Informed extension', model: 'sonnet', schema: { type: 'object', properties: { summary: { type: 'string' } }, required: ['summary'] } })))
  informed = await workflow({ scriptPath: `${W}/interpret.js` }, { blind: false, out: 'analysis', video_dir: common.video_dir, root: R, videos: VID_NAMES, rounds: args.informed_rounds || 3 })
}

// blindcmp.js as the final stage (default for blind-first runs; opt in with compare_after).
let cmp = null
if (args.compare_after) {
  phase('Compare')
  cmp = await workflow({ scriptPath: `${W}/blindcmp.js` }, { videos: VID_NAMES, root: R })
}
return { identification: ident.filter(Boolean).map(i => i.candidates.map(c => c.event)), interpret: r, leak_hits: hits, leak_checked: leaks.filter(Boolean).length + '/' + VID_NAMES.length, informed, compare: cmp }
