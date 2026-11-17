export const meta = {
  name: 'v1-human',
  description: 'Panel debates why our reports are not how humans listen to music, designs a human-listening approach, prototypes it on a video, and blind judges compare old vs new',
  phases: [{ title: 'Debate' }, { title: 'Design' }, { title: 'Prototype' }, { title: 'Judge' }],
}
// args: { videos: ['video2','video1'], rounds: 3, root: optional }
const R = (args && args.root) || '/home/user/Listener'  // Workflow scripts have no Node APIs
// Preflight: fail loudly before any agent is launched if the root is wrong (no fallback; default is the literal /home/user/Listener, pass args.root).
const ROOT_PROBE = `${R}/v1/scripts/check_outputs.py`
const ROOT_SCHEMA = { type: 'object', properties: { exists: { type: 'boolean' } }, required: ['exists'] }
const rootProbe = await agent(`Report whether this file exists (use ls or stat; do not read or edit it): ${ROOT_PROBE}`, { label: 'preflight:root', phase: 'Debate', model: 'sonnet', effort: 'low', schema: ROOT_SCHEMA })
if (!(rootProbe && rootProbe.exists)) throw new Error(`human.js: ${ROOT_PROBE} not found, so root "${R}" is wrong (pass args.root = the repo path)`)
const D = `${R}/v1/analysis/human_listening`
const SUM = { type: 'object', properties: { summary: { type: 'string' } }, required: ['summary'] }
const J = { type: 'object', properties: { more_human: { type: 'string', enum: ['A', 'B', 'tie'] }, more_accurate: { type: 'string', enum: ['A', 'B', 'tie'] }, would_rather_read: { type: 'string', enum: ['A', 'B'] }, why: { type: 'string' }, still_not_human: { type: 'array', items: { type: 'string' } } }, required: ['more_human', 'more_accurate', 'would_rather_read', 'why', 'still_not_human'] }
const VIDS = args.videos || ['video2', 'video1']
const ctx = `Repo ${R}. We built a toolkit so Claude can understand a music video "the way a human would feel and interpret it". The user has read our published reports (${VIDS.map(v => `v1/analysis/${v}/REPORT.md`).join(', ')}, plus v1/analysis/compare/elfstedentocht_diptych/comparison.md) and said: "This is absolutely not how a human thinks and listens about music."
How the reports were produced: agents cannot hear, so they "listen" through measurements (demucs stems, dB levels, spectrograms, chords, pitch tracks, CLAP tags, transcripts) and 1 fps frames; workflows forced every feeling to cite a measurement; panels and fact-checkers then hardened it (see v1/workflows/listen.js, interpret.js, report.js and v1/analysis/music/<video>/music_reading.md). The music: Public Service Broadcasting, "Elfstedentocht Part 1" (video1) and "Part 2" (video2), 2013, built on Dutch archive narration about the brutal 1963 Frisian skating race.
Read the reports yourself before speaking. British English. Talk like a person, not a committee. Be concrete: quote lines from our reports that ring false and say what a real listener would say instead.`

const PANEL = [
  ['psychologist', 'a music psychologist: what research says about how people actually listen (expectation and surprise, the ITPRA idea, groove and the urge to move, chills, absorption, memory for music being schematic and selective, attention drifting, associations, emotions people feel versus recognise, how little technical vocabulary ordinary listeners use)'],
  ['fan', 'an ordinary music fan who loves this kind of thing: how you actually talk about a song to a mate, what you remember after one listen, what made the hairs stand up, what you would skip, the songs it reminds you of'],
  ['critic', 'a music journalist who writes for a living: how good music writing captures a track (image, metaphor, comparison, context, a point of view, economy) and why a timestamped inventory is not criticism'],
  ['musician', 'a working musician: how players hear a track (the riff, the groove, the build, the drop, what the drummer is doing, the production trick), using musicians\' words rather than measurements, and what the measurement-led reports got right but expressed wrongly'],
  ['viewer', 'someone who watched the video on their phone: how image and music fuse into one feeling, what you notice and what passes you by, what the archive footage does to you, how you would describe it afterwards'],
  ['devil', 'a devil\'s advocate for the current approach: what would be LOST by going "human" (accuracy, honesty about what an AI can perceive, checkability), and how to keep those without the audit voice'],
]
phase('Debate')
for (let r = 1; r <= (args.rounds || 3); r++) {
  await parallel(PANEL.map(([k, who]) => () => agent(`${ctx}

You are ${who}.
${r === 1
  ? 'ROUND 1. Read the reports. Say plainly why they are not how a human listens, with quoted examples. Then describe, from your angle, how a human actually takes in this music and video, from first seconds to afterwards. End with 3 questions for named panellists (psychologist, fan, critic, musician, viewer, devil).'
  : `ROUND ${r}. Read every panellist's round ${r - 1} file in ${D}/round_${r - 1}/. Answer what was asked of you, argue where you disagree, build on the best ideas. ${r === (args.rounds || 3) ? 'FINAL ROUND: end with your 7 most important principles for writing about music the way a human experiences it, and the 3 worst habits of our current reports to kill.' : 'End with 2 new questions for named panellists.'}`}
Write ${D}/round_${r}/${k}.md, then return a short summary.`, { label: `${k}:r${r}`, phase: 'Debate', model: 'sonnet', schema: SUM })))
  log(`debate round ${r} done`)
}

phase('Design')
await agent(`${ctx}

Read the whole debate in ${D}/round_*/. Write ${D}/PROPOSAL.md:
1. Diagnosis: why our outputs read like an audit (root causes in the pipeline and prompts, not just style).
2. How humans actually listen and watch (the panel's consensus), in plain words.
3. The new output: what a "human listening" piece contains and how it is written (voice, structure, what to leave out, how to handle AI limits honestly without hedging every line, where evidence lives instead).
4. Pipeline changes: concrete edits to v1/workflows (listen.js, interpret.js, report.js, perceive.js) and any new stage (e.g. several distinct listener personas writing short first-listen and repeat-listen reactions before any analysis, an "afterwards" memory test, comparison to other music). Keep measurement as the checking layer, not the voice. Keep the toolkit video-agnostic.
5. A one-paragraph writing brief that a writer agent can follow.
Do not edit the workflows yourself. Return a summary.`, { label: 'design', phase: 'Design', model: 'sonnet', schema: SUM })

phase('Prototype')
await parallel(VIDS.map(vid => () => agent(`${ctx}

Follow the writing brief and output spec in ${D}/PROPOSAL.md exactly. Using the existing analysis for ${vid} (v1/analysis/music/${vid}/music_reading.md, v1/analysis/${vid}/interpretation.md, dossier.md, v1/data/${vid}/context.md) as your private notes, never as your voice, write ${D}/${vid}_human.md: the piece a perceptive human would write after watching and listening to this video. Every fact must still be true to those notes (do not invent events, instruments or lyrics), but the measurements stay out of sight unless a human would genuinely mention them. This file is a repository deliverable: write it with the Write tool. Return a summary.`, { label: `prototype:${vid}`, phase: 'Prototype', model: 'sonnet', schema: SUM })))

phase('Judge')
const JUDGES = [
  ['casual', 'a casual listener who has seen the video once'],
  ['writer', 'an experienced music editor at a magazine'],
  ['stickler', 'a stickler for accuracy who will check claims against v1/analysis/music/<video>/music_reading.md and v1/data/<video>/'],
]
const verdicts = await parallel(VIDS.flatMap(vid => JUDGES.map(([k, who]) => () => agent(`${ctx}

You are ${who}. You have NOT seen the debate. Read two pieces about ${vid}: A = v1/analysis/${vid}/REPORT.md, B = ${D}/${vid}_human.md. Judge which is more like how a human experiences and talks about this music and video, which is more accurate, which you would rather read, and list what in the better one still does not sound human.`, { label: `judge:${k}:${vid}`, phase: 'Judge', model: 'sonnet', schema: J }).then(v => v && ({ vid, judge: k, ...v })))))
await agent(`${ctx}

Judges' verdicts (A = old REPORT.md, B = new human piece): ${JSON.stringify(verdicts.filter(Boolean))}
Write ${D}/VERDICT.md: the scores, what worked, what still is not human, and the next changes to make. Append a short dated entry to v1/PROGRESS.md. Return a summary.`, { label: 'verdict', phase: 'Judge', model: 'sonnet', schema: SUM })
return verdicts.filter(Boolean).map(v => `${v.vid}/${v.judge}: human=${v.more_human} accurate=${v.more_accurate} read=${v.would_rather_read}`)
