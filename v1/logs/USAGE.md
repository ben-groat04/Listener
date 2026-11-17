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
