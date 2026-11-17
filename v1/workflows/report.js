export const meta = {
  name: 'v1-report',
  description: 'Video-agnostic final step: turn the checked music reading + interpretation into a readable, human REPORT.md, then cold-read and revise it',
  phases: [{ title: 'Write' }, { title: 'Cold read' }, { title: 'Revise' }],
}
// args: { root: optional repo root, videos: ['video1'], out: 'analysis', compare: '<name of a compare/ folder under out>' (optional; skipped if its comparison.md is missing), blind: optional true (no context.md, no research) }
// Root: R defaults to args.root, else the literal /home/user/Listener (Workflow scripts have no __dirname/process, so it is NOT derived from the script's location).
// If R/v1/scripts/check_outputs.py is missing (wrong root), the preflight throws before any writer is launched.
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
const rootCheck = `${R}/v1/scripts/check_outputs.py`
const humanPaths = v => [`${OUT}/${v}/LISTENING.md`, `${OUT}/${v}/FACTS.md`]  // human-listening layer (optional: fall back with a stated note when absent)
const pre = await exists([rootCheck, ...(cmpPath ? [...need, cmpPath] : need), ...VIDS.flatMap(humanPaths)], 'preflight')
if (!pre.find(x => x.path === rootCheck).ok) throw new Error(`report.js: ${rootCheck} not found, so root '${R}' is wrong (pass args.root = the repo checkout). Nothing launched.`)
const humanAll = VIDS.flatMap(humanPaths)
const missing = pre.filter(x => !x.ok && x.path !== cmpPath && x.path !== rootCheck && !humanAll.includes(x.path)).map(x => x.path)
if (missing.length) throw new Error(`report.js: missing required inputs, nothing launched:\n${missing.join('\n')}`)
const USE_CMP = !!cmpPath && pre.find(x => x.path === cmpPath).ok
const BLIND = !!args.blind || OUT.includes('analysis_blind')
const HAS_HUMAN = {}
for (const v of VIDS) { HAS_HUMAN[v] = humanPaths(v).every(p => pre.find(x => x.path === p).ok); if (!HAS_HUMAN[v]) log(`${v}: LISTENING.md and/or FACTS.md missing under ${OUT}/${v}/ (run listening.js first): falling back to music_reading.md/interpretation.md/dossier as the only sources, and the report will say its voice comes from the measurement layer only`) }
if (cmpPath && !USE_CMP) log(`comparison ${cmpPath} not found: continuing without it`)
async function one(vid) {
  const F = `${OUT}/${vid}/REPORT.md`
  const HUMAN = HAS_HUMAN[vid]
  const LF = `${OUT}/${vid}/LISTENING.md`, FF = `${OUT}/${vid}/FACTS.md`
  const checking = `${OUT}/music/${vid}/music_reading.md (the music), ${OUT}/${vid}/interpretation.md, ${OUT}/${vid}/dossier.md${USE_CMP ? `, ${cmpPath}` : ''}, v1/data/${vid}/context.md (unless blind), v1/data/${vid}/sync/sync.json`
  const src = HUMAN
    ? `Sources. READ FIRST, as the main human voice: ${LF} (how a listener hears and feels it) and ${FF} (the verified key moments you may state). Read second, as the CHECKING LAYER and sidecar (already fact-checked; they license, refute or add to the human sentences, they do not set the voice): ${checking}. Where LISTENING.md and a checking file disagree, the checking file and raw data win and the sentence is fixed. Repo ${R}.`
    : `Sources (already fact-checked): ${checking}. NOTE: ${LF} and/or ${FF} are absent, so there is no human-listening layer; say in one plain clause in the Evidence appendix that the voice here rests on the measurement layer only. Music first: ${OUT}/music/${vid}/music_reading.md is primary. Repo ${R}.`
  const writer = note => agent(`${src}${note}

Write ${F} with the Write tool. This file is a PROJECT DELIVERABLE that lives in the repository (it is the task's output, not a report back to your caller), so writing it is exactly what is asked. ALSO return the full markdown in the report_markdown field so the workflow can save it if writing fails.
The file is the final, human report on ${vid}, for an intelligent reader who wants to understand how this music and video FEEL and what they MEAN, the way a perceptive critic or a moved listener would put it. It has TWO TIERS.

TIER 1, the main text (felt prose, British English). HARD RULES (a checker, v1/scripts/check_outputs.py --report, will fail the file if they are broken):
- Lead with the music. Then how the picture works with it. Then meaning and context. Then the moments that stay with you.
- Flowing, vivid, precise prose, few numbers. No statistics anywhere in Tier 1: no Hz, dB, %, p= or r= (a digit followed by Hz, dB, %, "p=" or "r="), no correlation or p-values. Say "very quiet", "low and heavy", "most of the cuts". Move every such figure to the Tier 2 appendix. Keep m:ss timestamps so the reader can find moments.
- MANDATORY, and placed immediately after the music-and-picture passages, the heading exactly "## What it is like to listen (interpretation)": the human-listening layer of Tier 1, written as a listener would (the checker needs the section to be labelled interpretation and to use "I" or "my"; keep the "I" to what a listener could honestly say, plain, never "I felt" invented from nowhere), GROUNDED in ${HUMAN ? `${LF} and ${FF} first, then` : ''} the panel's attention, boredom and change-of-mind notes (read ${OUT}/${vid}/panel/ and ${OUT}/${vid}/interpretation.md; quote or paraphrase those notes and give each its m:ss). Plain sentence first, then at most one image; no numbers or units here either (all the Tier 1 number rules apply to this layer). Cover where attention rises or drifts, physical sensation, boredom or restlessness, and where the listener's mind changed. Do not invent events the notes do not contain; if the notes hold none of a kind, say so in one clause.
- REQUIRED Tier 1 paragraph headed "## Where it sits": genre, lineage and cultural setting. Sources for it are ONLY the lineage specialist output (written as ${OUT}/music/${vid}/specialists/round_*/lineage.md, or the lineage output in ${OUT}/${vid}/lineage_and_words.md if that is where lineage lives) and reception notes: the lineage specialist file (the highest-numbered ${OUT}/music/${vid}/specialists/round_*/lineage.md) and research/reception.md (look in v1/data/${vid}/research/ and ${OUT}/${vid}/research/). End it with "Sources: <files>. Confidence: <high|medium|low>." Never invent influences, bands, scenes or dates that those files do not state. Any placement the sources do not themselves state (your own by-ear placement) is labelled INFERRED with a plain-word confidence. If neither file exists or neither supports a claim, OMIT the section's claims entirely and write one line "Where it sits: not established from the sources." ${BLIND ? 'THIS IS A BLIND RUN: write a genre-by-feel label only, say plainly it is by ear/feel, and label it INFERRED with a plain-word confidence; name no influences.' : ''}
- Any claim of what "listeners feel", "most listeners" or "audiences" do must be exactly one of: (1) a cited reception quote (quote it and name the file in research/reception.md), (2) a stated musical mechanism (name the sound feature that produces the effect), or (3) labelled "my reading" (this applies equally to claims lifted from LISTENING.md: a felt effect on others needs one of the three). Unlabelled generalisations about other listeners are not allowed.
- Every context fact in an opening paragraph (names, places, dates, events taken from context.md or research) carries an inline tag [CONTEXT: <file>, <high|medium|low>]. The tag carries the real source file and a confidence taken from that file (do not raise it); the same marker and confidence appear on the fact's appendix row. Facts seen or heard directly need no such tag. ${BLIND ? 'Blind run: there is no context; anything identified from an end card or caption is tagged OBSERVED with the frame file.' : ''}
- Every claim about colour, on-screen text or a gesture cites a frame file (f_NNNN.jpg) or an m:ss timestamp in the same sentence, and only for frames YOU opened. Absence claims are written "in the N frames opened, none shows ..." with the real N (the number of frames you actually opened, the same N recorded on the Checked-against line of the appendix; no frames opened means no absence claim); never "nobody", "never", "no one". Do not use the words fur, hand-painted, hand-lettered or policeman (see v1/DO_NOT_CLAIM.md); describe what is literally visible.
- Emotive sound nouns (heartbeat, bell, breath) are banned unless the same sentence labels them "(metaphor)".
- Include a short lineage / cultural-context passage only through the "Where it sits" rules above; never import context the sources lack.
${USE_CMP ? `- COMPARISON IS MANDATORY (a comparison file exists, so omitting this section is a failure): read ${cmpPath} and add a short section "## Seen after / before the other part" (say "after" or "before" according to where this video sits in the pair) drawing the main continuities and changes from the comparison, and add a reciprocal link to the other video's report (relative path ../<other-video>/REPORT.md) and to the comparison file. Keep tags from the comparison; do not add comparison facts it lacks. The comparison file must also link back to this report (check it; if it does not, say so in the appendix under Where to look next, do not edit it).` : ''}
- Say the limitation ONCE, in ONE sentence at the very END of Tier 1 (the last sentence before the Evidence appendix): the music was "heard" through measurements (stems, spectrograms, chords, levels), not by ears. Not at the start, and not repeated elsewhere.
- Where something is uncertain, say so in plain words ("almost certainly", "probably", "a fair guess", "no way to tell"). Do not put H/M/L/OBS/INT tags in the main prose (the [CONTEXT: ...] tag and INFERRED in the opening are the exceptions).
- No process narrative and no agent counts: nothing about how the analysis was run, which agents or passes were used, or how many.
- Write the opening paragraph, "What this most probably is", LAST, after everything else is drafted, and place it first. It states in plain words what the piece is (kind of music, kind of film, what it is about) and includes any INFERRED identifications (genre, era, maker, place, instrument) each with plain-word confidence (for example "almost certainly", "probably", "possibly"), never stated as bare fact.
- Length: main text 1,200-2,000 words (the appendix is extra and does not count).

TIER 2, a final section headed exactly "## Evidence appendix" (the statistics removed from Tier 1 live here, with units):
- Start with a "Checked against" header line naming the source files and raw data the claims were checked against, AND listing every frame file you opened (f_NNNN.jpg), with the count N used in the "in the N frames opened" absence claims.
- List the key claims behind Tier 1 (a compact table or list), each with its tag (H/M/L/OBS/INT, carried over from the sources), its source file, and the measurement or observation it rests on.
- TAG RULE: a tag may not be lowered between the sources and this report (for example H to M, or OBS to INT) without a stated reason in the appendix row. Raising a tag needs a source that justifies it.
- If shot or cut counts are used anywhere, add a "Detector caveats" line stating that they come from automatic detection, with its known misses and false cuts.
- End with "Where to look next": links to the detailed files.
- Every fact must come from the sources; do not add facts. Where sources disagree, say so in the appendix.
When finished, run: python3 ${R}/v1/scripts/check_outputs.py --report ${F} and fix every FAIL before you finish.`, { label: `write:${vid}`, phase: 'Write', model: 'sonnet', schema: { type: 'object', properties: { summary: { type: 'string' }, report_markdown: { type: 'string' } }, required: ['summary', 'report_markdown'] } })
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
    ['feel', 'a music lover who has seen the video: does this capture how it actually feels? Where is it flat, robotic, over-hedged, or missing the obvious (the big riff, the emotional peak, the human story)? Is the first-person listener layer present, labelled as interpretation, credible and grounded in the panel notes? Is the Where-it-sits paragraph sourced only from the lineage file and reception notes, with sources and confidence?'],
    ['truth', 'a strict fact-checker: check 12 concrete claims against the source files and raw data (v1/data/' + vid + '/). List anything unsupported or wrong. Also check that tagged claims survive: every H/M/L/OBS/INT tag in the appendix matches its source, none is lowered or raised without a stated reason, and INFERRED identifications in the opening paragraph carry plain-word confidence.'],
    ['tiers', 'a structure critic: check tier separation. Tier 1 must be felt prose with few numbers, no stray units, no tags, no process narrative or agent counts, the limitation stated once in one sentence at the END of Tier 1 (not the start), no Hz/dB/%/p=/r= in Tier 1, the opening paragraph consistent with the rest (written last), and a main text of 1,200-2,000 words. Tier 2 (Evidence appendix) must have a Checked against header, tagged claims with source file and measurement, and a detector caveats line if shot counts appear. Also check: unlabelled listeners-feel claims; context facts in the opening without a [CONTEXT: file, confidence] tag; colour/text/gesture claims without a frame or timestamp; absence claims not worded as in the N frames opened; Checked against not listing all frames opened; ' + (USE_CMP ? 'the Seen after / before the other part section and reciprocal link; ' : '') + 'and run python3 ' + R + '/v1/scripts/check_outputs.py --report ' + F + '. Report any evidence leaking into Tier 1 or felt claims lacking an appendix row.'],
  ].map(([k, who]) => () => agent(`${src}\n\nYou are ${who}\nRead ${F}. Return a verdict and a list of concrete problems with suggested fixes.`, { label: `cold:${k}:${vid}`, phase: 'Cold read', model: 'sonnet', schema: CR })))
  await agent(`${src}\n\nRevise ${F} using these cold-read notes (verify each against the sources before acting; ignore notes that are wrong): ${JSON.stringify(crit.filter(Boolean))}\nKeep both tiers intact (felt Tier 1, tagged Evidence appendix) and every hard rule above (listener heading, Where it sits, no statistics in Tier 1, limitation last sentence of Tier 1); finish by running python3 ${R}/v1/scripts/check_outputs.py --report ${F} and fixing FAILs and the main text within 1,200-2,000 words. Keep it readable and true. Append nothing about the revision to the report itself; add one line to v1/PROGRESS.md.`, { label: `revise:${vid}`, phase: 'Revise', model: 'sonnet', schema: SUM })
  return vid
}
return await parallel(VIDS.map(v => () => one(v)))
