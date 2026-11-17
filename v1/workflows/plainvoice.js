export const meta = {
  name: 'v1-plainvoice',
  description: 'Make listening writing indistinguishable from real people: collect real human music writing, study its style and AI tells, write plain registers, run a Turing-style test against real excerpts, iterate',
  phases: [{ title: 'Corpus' }, { title: 'Style' }, { title: 'Write' }, { title: 'Turing test' }],
}
// args: { videos: ['video2','video1'], rounds: 3, seed: false (true = start from existing v1/analysis/<video>/VOICES.md), root: optional }
const R = (args && args.root) || '/home/user/Listener'  // Workflow scripts have no Node APIs
const H = `${R}/v1/analysis/human_listening`
const C = `${H}/corpus`
const SUM = { type: 'object', properties: { summary: { type: 'string' } }, required: ['summary'] }
const EX = { type: 'object', properties: { excerpts: { type: 'array', items: { type: 'object', properties: { register: { type: 'string', enum: ['text', 'forum', 'review'] }, text: { type: 'string' }, url: { type: 'string' }, about: { type: 'string' } }, required: ['register', 'text', 'url', 'about'] } } }, required: ['excerpts'] }
const DRAFT = { type: 'object', properties: { text_to_mate: { type: 'string' }, forum_post: { type: 'string' }, short_review: { type: 'string' } }, required: ['text_to_mate', 'forum_post', 'short_review'] }
const TV = { type: 'object', properties: { verdicts: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, label: { type: 'string', enum: ['human', 'ai'] }, confidence: { type: 'integer', minimum: 1, maximum: 5 }, tells: { type: 'string' } }, required: ['id', 'label', 'confidence', 'tells'] } } }, required: ['verdicts'] }
const VIDS = args.videos || ['video2', 'video1']

phase('Corpus')
const hunts = [
  ['forum', 'forum and Reddit posts or comments by ordinary listeners describing what a song or album did to them (r/postrock, r/LetsTalkMusic, r/Music, band subreddits, Discogs/RYM user reviews, music forums). Include some about Public Service Broadcasting, post-rock, krautrock, instrumental and electronic tracks.'],
  ['review', 'short, plainly written human reviews and blog posts about tracks or albums (small blogs, Bandcamp fan notes, newsletter write-ups), including any about Public Service Broadcasting\'s Elfstedentocht or similar instrumental, sample-based or archive-footage music. Avoid polished broadsheet criticism.'],
  ['text', 'very casual human reactions: short comments, tweets/threads quoted in articles, YouTube comment snippets quoted on pages you can fetch, people recommending a song to a friend. The register of a text message about a song.'],
]
const corpus = await parallel(hunts.map(([k, what]) => () => agent(`Collect REAL human writing about music from the web for a style study (not about our videos specifically). Load WebSearch and WebFetch with ToolSearch. Find ${what}
Return 8-12 excerpts (each 30-200 words, verbatim, with the URL and what it is about). Only text you actually fetched or saw in a search result; never invent or paraphrase. Skip anything that reads machine-written. Also save them to ${C}/${k}.md with URLs.`, { label: `corpus:${k}`, phase: 'Corpus', model: 'sonnet', schema: EX })))
const REAL = corpus.filter(Boolean).flatMap(c => c.excerpts).filter(e => e.text && e.text.split(' ').length >= 25)
log(`corpus: ${REAL.length} real excerpts`)

phase('Style')
await agent(`Repo ${R}. Study the real human excerpts in ${C}/*.md and our machine-written pieces (v1/analysis/video1/LISTENING.md, v1/analysis/video2/LISTENING.md, v1/analysis/human_listening/*_human.md). Write ${H}/STYLE.md:
1. How real people actually write about music in each register (text, forum post, short review): sentence length, vocabulary, specificity, humour, digressions, imprecision, personal context, how they mention the music (riff, drop, "that bit where"), how they end (usually abruptly, no moral).
2. The AI tells in our pieces, with quoted examples: metaphor stacking, manufactured bodily sensations, tricolons, "not X, but Y", aphoristic closing lines, "I will admit", over-balanced paragraphs, literary similes in every paragraph, performed sincerity, too-neat structure.
3. A short checklist a writer must pass. Return a summary.`, { label: 'style', phase: 'Style', model: 'sonnet', schema: SUM })

const facts = vid => `Facts you may use (and nothing beyond them): ${R}/v1/analysis/${vid}/FACTS.md (verified key moments), plus ${R}/v1/data/${vid}/context.md for who made it. The piece will be shown under a page note saying it was written by Claude from an analysis; do not mention analysis, frames, transcripts or AI in the text.`
let drafts = {}
phase('Write')
if (args.seed) await parallel(VIDS.map(vid => () => agent(`Read ${R}/v1/analysis/${vid}/VOICES.md and return its three pieces verbatim (sections 'A text to a mate', 'A forum post', 'A short review').`, { label: `seed:${vid}`, phase: 'Write', model: 'sonnet', effort: 'low', schema: DRAFT }).then(d => { if (d) drafts[vid] = d })))
else await parallel(VIDS.map(vid => () => agent(`Read ${H}/STYLE.md and a few real excerpts in ${C}/*.md first, so you write like those people, not like a novelist. ${facts(vid)}
Write three pieces about watching and listening to ${vid} (Public Service Broadcasting's Elfstedentocht ${vid === 'video1' ? 'Part 1' : 'Part 2'}), each as a different real person might:
- text_to_mate: 40-110 words, a message recommending (or not) the video to a friend.
- forum_post: 150-320 words, a post in a music forum thread.
- short_review: 300-550 words, a plain blog review.
Plain words. People mention very few facts: at most TWO checkable facts per piece (no counts, dates or temperatures unless it is the one thing that struck you). No staged persona props (kettles, earbuds, car parks) and no sprinkled hedges ('I think', 'no idea') used as decoration. Do not walk through the video in order; people mention one or two bits and skip the rest. No tidy summing-up last line. Vary sentence length unevenly. At most one comparison per piece. No manufactured body sensations unless ordinary ("gave me chills" is fine if earned by a real moment, at most once). No closing aphorism. Imperfect is fine. Every fact true to FACTS.md. Return all three.`, { label: `write:${vid}:r1`, phase: 'Write', model: 'sonnet', schema: DRAFT }).then(d => { drafts[vid] = d })))

const ROUNDS = args.rounds || 3
const history = []
for (let round = 1; round <= ROUNDS; round++) {
  phase('Turing test')
  // pool: our 6 pieces + 6-9 real excerpts, deterministic interleave
  const ours = VIDS.flatMap(v => drafts[v] ? [['text', drafts[v].text_to_mate], ['forum', drafts[v].forum_post], ['review', drafts[v].short_review]].map(([reg, t], i) => ({ id: `${v}-${reg}`, src: 'ours', reg, text: t })) : [])
  const reals = REAL.slice((round - 1) * 3, (round - 1) * 3 + 9).map((e, i) => ({ id: `r${round}-${i}`, src: 'real', reg: e.register, text: e.text }))
  const pool = []
  for (let i = 0; i < Math.max(ours.length, reals.length); i++) { if (reals[i]) pool.push(reals[i]); if (ours[i]) pool.push(ours[i]) }
  // fair design: each of our pieces is judged in its OWN pool with 5 real excerpts (no topic clustering)
  const oursK = pool.filter(p => p.src === 'ours'), realsK = pool.filter(p => p.src === 'real')
  const perPiece = await parallel(oursK.map((o, oi) => () => {
    const others = REAL.slice((oi * 5 + round * 3) % Math.max(1, REAL.length - 5), (oi * 5 + round * 3) % Math.max(1, REAL.length - 5) + 5)
    const items = []; others.forEach((e, i) => { if (i === (oi % 5)) items.push({ src: 'ours', text: o.text }); items.push({ src: 'real', text: e.text }) })
    const blind = items.map((it, i) => ({ id: `Q${round}${oi}${i}`, text: it.text, src: it.src }))
    return parallel([['reader', 'an avid reader of music forums and blogs'], ['editor', 'an editor who spots AI-written copy for a living'], ['musician', 'a musician who reads what fans write about bands']].map(([k, who]) => () => agent(`You are ${who}. Below are ${blind.length} short pieces of writing about music, on different songs. Some were written by real people on forums, blogs and social media; possibly some by an AI. For EACH id, label it human or ai, give confidence 1-5, and name the tells.\n\n${blind.map(b => `### ${b.id}\n${b.text}`).join('\n\n')}`, { label: `judge:${k}:${o.id}:r${round}`, phase: 'Turing test', model: 'sonnet', schema: TV }))).then(js => {
      js = js.filter(Boolean); const ourId = blind.find(b => b.src === 'ours').id
      const vs = js.map(j => j.verdicts.find(v => v.id === ourId)).filter(Boolean)
      const rf = blind.filter(b => b.src === 'real').flatMap(b => js.map(j => j.verdicts.find(v => v.id === b.id))).filter(Boolean)
      return { id: o.id, caught: vs.filter(v => v.label === 'ai').length, of: vs.length, tells: vs.filter(v => v.label === 'ai').map(v => v.tells), realFlagged: rf.filter(v => v.label === 'ai').length, realOf: rf.length }
    })
  }))
  const res = perPiece.filter(Boolean)
  const caughtRate = res.reduce((a, r) => a + r.caught, 0) / Math.max(1, res.reduce((a, r) => a + r.of, 0))
  const falseRate = res.reduce((a, r) => a + r.realFlagged, 0) / Math.max(1, res.reduce((a, r) => a + r.realOf, 0))
  history.push({ round, our_pieces_flagged_ai: Math.round(caughtRate * 100) + '%', real_pieces_flagged_ai: Math.round(falseRate * 100) + '%', per_piece: res.map(r => `${r.id}:${r.caught}/${r.of}`) })
  log(`round ${round}: ours flagged AI ${Math.round(caughtRate * 100)}%, real flagged AI ${Math.round(falseRate * 100)}%`)
  if (caughtRate <= falseRate + 0.1 || round === ROUNDS) break
  phase('Write')
  await parallel(VIDS.map(vid => () => agent(`Read ${H}/STYLE.md. ${facts(vid)}
These are your three pieces about ${vid}; blind judges mixing them with real human writing caught some as AI. Rewrite ONLY the pieces the judges caught (caught > 0), fixing exactly the tells named; return pieces that were not caught EXACTLY unchanged. Keep every fact true.
CURRENT: ${JSON.stringify(drafts[vid])}
JUDGES' TELLS: ${JSON.stringify(res.filter(r => r.id.startsWith(vid)))}`, { label: `write:${vid}:r${round + 1}`, phase: 'Write', model: 'sonnet', schema: DRAFT }).then(d => { if (d) drafts[vid] = d })))
}
await agent(`Repo ${R}. Save these final pieces as repository deliverables (Write tool), one file per video at v1/analysis/<video>/VOICES.md with three headed sections "A text to a mate", "A forum post", "A short review" (text exactly as given, no edits): ${JSON.stringify(drafts)}
Then write ${H}/TURING.md with this test history and what changed between rounds: ${JSON.stringify(history)}. Append a dated line to v1/PROGRESS.md.`, { label: 'save', phase: 'Turing test', model: 'sonnet', effort: 'low', schema: SUM })
return history
