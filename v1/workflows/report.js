export const meta = {
  name: 'v1-report',
  description: 'Video-agnostic final step: turn the checked music reading + interpretation into a readable, human REPORT.md, then cold-read and revise it',
  phases: [{ title: 'Write' }, { title: 'Cold read' }, { title: 'Revise' }],
}
// args: { root: optional repo root, videos: ['video1'], out: 'analysis', compare: '<name of a compare/ folder under out>' (optional; skipped if its comparison.md is missing) }
// Root: args.root, else two directories up from this script (v1/workflows), else the working directory.
const R = (args && args.root) || '/home/user/Listener'  // Workflow scripts have no Node APIs (__dirname/process undefined); pass args.root for another checkout
const OUT = `${R}/v1/${args.out || 'analysis'}`
const SUM = { type: 'object', properties: { summary: { type: 'string' } }, required: ['summary'] }
const CR = { type: 'object', properties: { verdict: { type: 'string' }, problems: { type: 'array', items: { type: 'string' } } }, required: ['verdict', 'problems'] }
const VIDS = (args.videos || []).map(v => (typeof v === 'string' ? v : v.vid))
const CHK = { type: 'object', properties: { files: { type: 'array', items: { type: 'object', properties: { path: { type: 'string' }, exists: { type: 'boolean' }, bytes: { type: 'integer' } }, required: ['path', 'exists', 'bytes'] } } }, required: ['files'] }
async function exists(paths, label) {
  const r = await agent(`For each of these paths (repo ${R}), report whether the file exists and its size in bytes (use ls -l or stat; do not read or edit them): ${JSON.stringify(paths)}`, { label, phase: 'Write', model: 'sonnet', effort: 'low', schema: CHK })
  return paths.map(p => { const f = r && r.files.find(x => x.path === p); return { path: p, ok: !!(f && f.exists && f.bytes > 0) } })
}
// Preflight: required inputs must exist; the comparison is optional and dropped if absent.
const need = VIDS.flatMap(v => [`${OUT}/music/${v}/music_reading.md`, `${OUT}/${v}/interpretation.md`])
const cmpPath = args.compare ? `${OUT}/compare/${args.compare}/comparison.md` : null
const pre = await exists(cmpPath ? [...need, cmpPath] : need, 'preflight')
const missing = pre.filter(x => !x.ok && x.path !== cmpPath).map(x => x.path)
if (missing.length) throw new Error(`report.js: missing required inputs, nothing launched:\n${missing.join('\n')}`)
const USE_CMP = !!cmpPath && pre.find(x => x.path === cmpPath).ok
if (cmpPath && !USE_CMP) log(`comparison ${cmpPath} not found: continuing without it`)
async function one(vid) {
  const F = `${OUT}/${vid}/REPORT.md`
  const src = `Sources (already fact-checked): ${OUT}/music/${vid}/music_reading.md (the music, primary), ${OUT}/${vid}/interpretation.md, ${OUT}/${vid}/dossier.md${USE_CMP ? `, ${cmpPath}` : ''}, v1/data/${vid}/context.md (unless blind), v1/data/${vid}/sync/sync.json. Repo ${R}.`
  const writer = note => agent(`${src}${note}

Write ${F} with the Write tool. This file is a PROJECT DELIVERABLE that lives in the repository (it is the task's output, not a report back to your caller), so writing it is exactly what is asked. ALSO return the full markdown in the report_markdown field so the workflow can save it if writing fails.
The file is the final, human report on ${vid}, for an intelligent reader who wants to understand how this music and video FEEL and what they MEAN, the way a perceptive critic or a moved listener would put it. It has TWO TIERS.

TIER 1, the main text (felt prose, British English):
- Lead with the music. Then how the picture works with it. Then meaning and context. Then the moments that stay with you.
- Flowing, vivid, precise prose, few numbers. No unit in the main text unless it changes the feel (say "very quiet", not "-40 dB"). Keep timestamps (m:ss) so the reader can find moments.
- Include a clearly labelled first-person listener layer, "What it is like to listen", written as a listener would: where attention rises or drifts, physical sensation (chest, breath, posture), boredom or restlessness, and where the listener's mind changed. Tag the whole section as interpretation (e.g. "(interpretation)") and ground it in moments the sources actually support; do not invent events.
- Include a short lineage / cultural-context passage if the sources contain one (influences, genre ancestry, historical or cultural setting); omit it if they do not. Never import context the sources lack.
- Say the limitation ONCE, briefly: the music was "heard" through measurements (stems, spectrograms, chords, levels), not by ears. Do not repeat it elsewhere.
- Where something is uncertain, say so in plain words ("almost certainly", "probably", "a fair guess", "no way to tell"). Do not put H/M/L/OBS/INT tags in the main prose.
- No process narrative and no agent counts: nothing about how the analysis was run, which agents or passes were used, or how many.
- Write the opening paragraph, "What this most probably is", LAST, after everything else is drafted, and place it first. It states in plain words what the piece is (kind of music, kind of film, what it is about) and includes any INFERRED identifications (genre, era, maker, place, instrument) each with plain-word confidence (for example "almost certainly", "probably", "possibly"), never stated as bare fact.
- Length: main text 1,200-2,000 words (the appendix is extra and does not count).

TIER 2, a final section headed exactly "Evidence appendix":
- Start with a "Checked against" header line naming the source files and raw data the claims were checked against.
- List the key claims behind Tier 1 (a compact table or list), each with its tag (H/M/L/OBS/INT, carried over from the sources), its source file, and the measurement or observation it rests on.
- TAG RULE: a tag may not be lowered between the sources and this report (for example H to M, or OBS to INT) without a stated reason in the appendix row. Raising a tag needs a source that justifies it.
- If shot or cut counts are used anywhere, add a "Detector caveats" line stating that they come from automatic detection, with its known misses and false cuts.
- End with "Where to look next": links to the detailed files.
- Every fact must come from the sources; do not add facts. Where sources disagree, say so in the appendix.`, { label: `write:${vid}`, phase: 'Write', model: 'sonnet', schema: { type: 'object', properties: { summary: { type: 'string' }, report_markdown: { type: 'string' } }, required: ['summary', 'report_markdown'] } })
  const w1 = await writer('')
  if (!(await exists([F], `exists:${vid}`))[0].ok && w1 && w1.report_markdown && w1.report_markdown.length > 500) {
    log(`${vid}: writer could not save REPORT.md; saving the returned markdown via a saver agent`)
    await agent(`Save this exact markdown to ${F} using Bash (cat with a quoted heredoc) or the Write tool. It is a repository deliverable. Do not change the text.\n\n${w1.report_markdown}`, { label: `save:${vid}`, phase: 'Write', model: 'sonnet', effort: 'low', schema: SUM })
  }
  if (!(await exists([F], `exists:${vid}`))[0].ok) {
    log(`${vid}: REPORT.md missing after writer; retrying once`)
    await writer('\nA previous attempt produced NO file. You MUST create the file with the Write tool at the exact path below, then confirm it exists.')
    if (!(await exists([F], `exists2:${vid}`))[0].ok) { log(`${vid}: REPORT.md still missing after retry; skipping cold read`); return { vid, error: 'REPORT.md not written' } }
  }
  const crit = await parallel([
    ['feel', 'a music lover who has seen the video: does this capture how it actually feels? Where is it flat, robotic, over-hedged, or missing the obvious (the big riff, the emotional peak, the human story)? Is the first-person listener layer present, labelled as interpretation and credible?'],
    ['truth', 'a strict fact-checker: check 12 concrete claims against the source files and raw data (v1/data/' + vid + '/). List anything unsupported or wrong. Also check that tagged claims survive: every H/M/L/OBS/INT tag in the appendix matches its source, none is lowered or raised without a stated reason, and INFERRED identifications in the opening paragraph carry plain-word confidence.'],
    ['tiers', 'a structure critic: check tier separation. Tier 1 must be felt prose with few numbers, no stray units, no tags, no process narrative or agent counts, the limitation stated once, the opening paragraph consistent with the rest (written last), and a main text of 1,200-2,000 words. Tier 2 (Evidence appendix) must have a Checked against header, tagged claims with source file and measurement, and a detector caveats line if shot counts appear. Report any evidence leaking into Tier 1 or felt claims lacking an appendix row.'],
  ].map(([k, who]) => () => agent(`${src}\n\nYou are ${who}\nRead ${F}. Return a verdict and a list of concrete problems with suggested fixes.`, { label: `cold:${k}:${vid}`, phase: 'Cold read', model: 'sonnet', schema: CR })))
  await agent(`${src}\n\nRevise ${F} using these cold-read notes (verify each against the sources before acting; ignore notes that are wrong): ${JSON.stringify(crit.filter(Boolean))}\nKeep both tiers intact (felt Tier 1, tagged Evidence appendix) and the main text within 1,200-2,000 words. Keep it readable and true. Append nothing about the revision to the report itself; add one line to v1/PROGRESS.md.`, { label: `revise:${vid}`, phase: 'Revise', model: 'sonnet', schema: SUM })
  return vid
}
return await parallel(VIDS.map(v => () => one(v)))
