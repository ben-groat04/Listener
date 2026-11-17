export const meta = {
  name: 'v1-listening',
  description: 'Video-agnostic final voice: write ONE person\'s felt listening piece from the checked analysis, lint jargon/clock-times, mechanically fact-check, blind-judge for humanness; iterate until judges pass',
  phases: [{ title: 'Write' }, { title: 'Lint' }, { title: 'Fact-check' }, { title: 'Judge' }],
}
// args: { videos: ['video2'], out: 'analysis', max_iters: 3, blind: false, root: optional }
const R = (args && args.root) || '/home/user/Listener'  // Workflow scripts have no Node APIs
const OUT = `${R}/v1/${args.out || 'analysis'}`
const H = `${R}/v1/analysis/human_listening`
const SUM = { type: 'object', properties: { summary: { type: 'string' }, markdown: { type: 'string' } }, required: ['summary', 'markdown'] }
const LINT = { type: 'object', properties: { clock_times: { type: 'integer' }, banned_hits: { type: 'array', items: { type: 'string' } }, scaffolding: { type: 'array', items: { type: 'string' } } }, required: ['clock_times', 'banned_hits', 'scaffolding'] }
const FC = { type: 'object', properties: { errors: { type: 'array', items: { type: 'object', properties: { quote: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' } }, required: ['quote', 'problem', 'fix'] } } }, required: ['errors'] }
const J = { type: 'object', properties: { one_person_who_listened: { type: 'integer', minimum: 1, maximum: 10 }, human: { type: 'integer', minimum: 1, maximum: 10 }, would_share: { type: 'boolean' }, false_notes: { type: 'array', items: { type: 'string' } } }, required: ['one_person_who_listened', 'human', 'would_share', 'false_notes'] }
const BRIEF = `HOW TO WRITE IT (from the human-listening debate, ${H}/PROPOSAL.md and ${H}/VERDICT.md; read both):
- ONE voice, first person, past tense, as someone who has just watched and listened. Say once, in the first line, plainly: "I can't hear; this is how it would land, built from a close analysis of the sound and picture." Then stop apologising and stop hedging every sentence.
- Lead with the felt reaction: what it did to you, in the body (restless, braced, a lump in the throat, bored for a bit, nodding along, cold), and the one or two moments that stay. Not a timeline.
- Talk like a person: images, metaphors, comparisons to other music, films or experiences, clearly offered as comparisons ("it put me in mind of..."). A point of view is allowed, including mild criticism.
- Landmarks, not clocks: "when the voice stops", "the last minute", "after the long wait". At most two clock times in the whole piece, only where a reader would need to find a moment.
- No craft or measurement jargon unless an ordinary listener would use it: no dB, Hz, BPM numbers, stems, chroma, "on the one", "no fill", "held sound", "subtraction", "the wall", "pedal", "taught". No tables, no confidence grades, no persona lists, no "who hears what", no survey questions, no review-blurb opener.
- Describe voices as sounds (old, dry, flat, reading out figures) and let facts land as feeling, not as decoding keys.
- 700-1,200 words. Prose. A short title that sounds like a person wrote it.
- TRUTH: every event, instrument, word and image must be supported by the analysis notes (music_reading.md, harmony.md, voice_as_music.md, interpretation.md, dossier.md, context.md unless blind). Comparisons and feelings are yours; facts are not. Do not include anything listed as refuted or withdrawn in those notes.`
async function one(vid) {
  const F = `${OUT}/${vid}/LISTENING.md`
  const notes = `Private notes (never your voice): ${OUT}/music/${vid}/music_reading.md, ${OUT}/music/${vid}/harmony.md, ${OUT}/music/${vid}/voice_as_music.md, ${OUT}/${vid}/interpretation.md, ${OUT}/${vid}/dossier.md, ${OUT}/${vid}/REPORT.md${args.blind ? '' : `, v1/data/${vid}/context.md, ${OUT}/${vid}/lineage_and_words.md`} (skip any that do not exist). Frames: v1/data/${vid}/frames_1fps/ and contact_sheets/ (look at a few so your images are real). Repo ${R}.`
  let prev = null, feedback = '', iters = []
  for (let it = 1; it <= (args.max_iters || 3); it++) {
    const w = await agent(`${BRIEF}\n\n${notes}\n\n${prev ? `REVISE the previous draft (${F}) using this feedback; keep what judges liked:\n${feedback}` : 'Write the piece.'}\nWrite it to ${F} with the Write tool (a repository deliverable) AND return the full markdown in the markdown field.`, { label: `write:${vid}:i${it}`, phase: 'Write', model: 'sonnet', schema: SUM })
    const lint = await agent(`Lint ${F} (repo ${R}) mechanically with grep/python, do not edit it. Count clock-style times (m:ss). List every occurrence of: dB, Hz, BPM, stem, chroma, LUFS, "on the one", "no fill", "held sound", "subtraction", "the wall", "pedal", "taught", "OBS", "INT", confidence grades (H/M/L), and any table, persona list, survey question or review-blurb opener (scaffolding). If the file is missing, report clock_times -1.`, { label: `lint:${vid}:i${it}`, phase: 'Lint', model: 'sonnet', effort: 'low', schema: LINT })
    const fc = await agent(`Fact-check ${F} (repo ${R}) against the checked analysis: ${notes}\nList every factual statement (events, timings, instruments, words, images, counts, history) that is wrong, unsupported, stronger than the evidence, or listed as refuted/withdrawn in the notes. Feelings and comparisons are not facts; ignore them. Open frames to check images. Be strict.`, { label: `factcheck:${vid}:i${it}`, phase: 'Fact-check', model: 'sonnet', schema: FC })
    const judges = await parallel([['casual', 'someone who has watched the video once on their phone'], ['editor', 'a music magazine editor'], ['friend', 'a friend who loves this kind of music and has heard it many times']].map(([k, who]) => () => agent(`You are ${who}. You have not seen how this was made. Read ${F} (repo ${R}). Score 1-10: does it sound like ONE person who actually listened and watched? How human does it feel overall? Would you share it? Quote every line that rings false (robotic, jargon, hedging, committee voice, fake feeling).`, { label: `judge:${k}:${vid}:i${it}`, phase: 'Judge', model: 'sonnet', schema: J })))
    const js = judges.filter(Boolean)
    const avg = js.length ? js.reduce((a, j) => a + j.one_person_who_listened + j.human, 0) / (2 * js.length) : 0
    const errs = fc ? fc.errors : []
    iters.push({ it, avg: Math.round(avg * 10) / 10, errors: errs.length, clock_times: lint ? lint.clock_times : null, banned: lint ? lint.banned_hits.length + lint.scaffolding.length : null })
    log(`${vid} iter ${it}: judges ${avg.toFixed(1)}/10, ${errs.length} fact errors, lint ${JSON.stringify(lint)}`)
    prev = w
    if (avg >= 8 && errs.length === 0 && lint && lint.clock_times <= 2 && lint.banned_hits.length === 0 && lint.scaffolding.length === 0) break
    feedback = JSON.stringify({ fact_errors: errs, lint, judges: js.map(j => ({ scores: [j.one_person_who_listened, j.human], false_notes: j.false_notes })) })
    if (it === (args.max_iters || 3) && errs.length) {
      await agent(`Final accuracy repair of ${F} (repo ${R}): fix ONLY these factual errors with the smallest wording change that keeps the voice; do not add hedges or jargon. ${JSON.stringify(errs)}`, { label: `repair:${vid}`, phase: 'Fact-check', model: 'sonnet', schema: { type: 'object', properties: { summary: { type: 'string' } }, required: ['summary'] } })
    }
  }
  return { vid, iters }
}
const res = await parallel((args.videos || []).map(v => () => one(v)))
await agent(`Append a short dated entry to ${R}/v1/PROGRESS.md summarising the listening-piece iterations: ${JSON.stringify(res)}. Also write ${H}/ITERATIONS.md with the same data and one line per iteration.`, { label: 'log', phase: 'Judge', model: 'sonnet', effort: 'low', schema: { type: 'object', properties: { summary: { type: 'string' } }, required: ['summary'] } })
return res
