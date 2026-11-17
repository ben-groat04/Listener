# Usage log
| time (UTC) | 5h used | 7d used | note |
|---|---|---|---|
| 23:31 | 78% | 52% | session start |
| 23:38 | 80% | 52% | v1 started |
| 23:43 | 82% | 52% | prep work (local scripts, few tokens) |
| 23:46 | 83% | 52% | ~0.5%/min while idle-ish chatting with Opus context |
| 23:47 | 83% | 52% | user: another session is also consuming usage (will stop soon), so the observed rate overstates this session's burn |
| 23:50 | 85% | 52% | 3 Sonnet researchers = 262k subagent tokens, about 1-2% (shared with another session). Launched video1 perceive (10 viewers + music) with a hard stop at 93% |
| 23:56 | 89% | 53% | +4% in 6 min while 10 viewers ran (plus the other session). **Stop launching until reset**; let the running video1 workflow finish. |
| 23:58 | 90% | 53% | status allowed_warning. Paused all agent work until 01:40 reset |
| 23:59 | 90% | 53% | user: the other session has stopped, so further increases are this session only |
| 00:16 | 92% | 53% | 10 Sonnet viewers cost ~2% (860k tokens). Per user, using remaining headroom: video2 seg 9-16 + words |
| 00:26 | 95% | 54% | 9 viewers = 790k tokens, ~3%. Remaining agent work needs music_views (CPU still running), so next launch is at the reset |
| 00:45 | 97% | 54% | 10 window listeners = 847k tokens, ~2%. Holding at 97% until the 01:40 reset (scheduled restart 01:42) |
| 01:43 | 0% | 54% | **RESET confirmed** (next 06:40). Container had restarted again; jobs restored. Heavy phase starts |
| 01:46 | 4% | 54% | 4 workflows in parallel (2 music panels, blind chain, research-2): ~1%/min |
| 02:22 | 45% | 60% | ~1.1%/min with 4-5 workflows; projected limit ~03:10 |
| 02:33 | 59% | 62% | ~1.4%/min |
| 02:36 | 63% | 62% | launched coldread cr1 |
| 02:47 | 75% | 64% | |
| 02:48 | ~76% | 64% | rules check-in 1 |
| 02:50 | 84% | 65% | blind video1 chain done (71 agents, 7.1M tokens) |
| 03:05 | 97% | 67% | window nearly spent; t_birdwalk blind chain still running and may be cut off (resume from its run id next window: wf_4fc94b33-454) |
| 03:11 | 100% | 67% | 5-hour limit hit (t_birdwalk blind chain cut off mid-panel; resumable) |
| 06:43 | 0% | 67% | **RESET 2** (next 11:40). Weekly 67%: each full window has cost ~13% weekly, so plan to stop this window around **~80% weekly** to leave the user headroom until the Fri 10:00 weekly reset. |
| 06:56 | 12% | 69% | ~2% weekly per 12% of window; cap this window near 55-60% (≈80% weekly) |
| 07:11 | 24% | 70% | weekly rising ~1% per 8% of window: whole window would end near ~80% weekly |
