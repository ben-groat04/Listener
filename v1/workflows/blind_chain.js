export const meta = {
  name: 'v1-blind-chain',
  description: 'Blind end-to-end run (no context, no research, no web): perceive -> listen -> interpret, output to v1/analysis_blind/',
  phases: [{ title: 'Blind perceive' }, { title: 'Blind listen' }, { title: 'Blind interpret' }],
}
const W = '/home/user/Listener/v1/workflows'
const common = { blind: true, out: 'analysis_blind', video_dir: args.video_dir || 'videos' }
phase('Blind perceive')
await workflow({ scriptPath: `${W}/perceive.js` }, { ...common, videos: args.videos })
phase('Blind listen')
await workflow({ scriptPath: `${W}/listen.js` }, { ...common, videos: args.videos, rounds: 2 })
phase('Blind interpret')
const r = await workflow({ scriptPath: `${W}/interpret.js` }, { ...common, videos: args.videos.map(v => v.vid), rounds: 3 })
return r