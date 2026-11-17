# Core instructions (logged verbatim intent, 2026-11-16 23:38 UTC)

Source: the user's message that kicked off v1. These are the rules for this attempt.

1. **Think hard. Be creative.**
2. **Use workflows so agents can converse** with each other (debate, respond, build on each other).
3. **The subject is a music video** (music videos in `videos/`, currently `video1`, `video2`). Do all you can, and mean *all*, to analyse
   everything about the video and the music **as a human would interpret it**: meaning, emotion,
   story, symbolism, not just technical data.
4. **Usage pacing:**
   - First check when usage resets.
   - Do NOT hit the usage limit before the reset (at full tilt it would be hit).
   - After it resets, **go crazy. Keep going. Do not stop until the limit is hit after the reset.** This is key.
5. **There is always more to analyse.** Treat it as a human would see it.
6. If it seems everything has been extracted, **run a workflow of cold-read agents on the project** to see what can be improved.
7. **Keep it organised.** Cold-read agents and especially workflows will be useful.
8. **Keep track of errors and mistakes** made along the way (see `logs/ERRORS.md`).
9. **Use Sonnet as often as possible** for agents.
10. The user is hands-off and has given approval for everything, **but cannot sign up for or pay for anything**: work around that.

## Usage facts found at start
- 5-hour window: 80% used at 23:38 UTC, resets **2026-11-17 01:40 UTC**.
- 7-day window: 52% used, resets 2026-11-20 10:00 UTC.
- Plan: cheap local extraction before the reset; heavy multi-agent workflows after it.

## Additional instructions (received ~23:50 UTC)
11. **Track usage periodically** and log the rate of increase (`logs/USAGE.md`). It's a Max plan, so there is room, but **don't edge it**: stop starting new work with a safety margin before 100%.
12. **Don't be too simplistic.** Use workflows, especially with cold reads. Do things very well with the usage available after the reset.
13. The user has a **companion video that precedes this one** (the predecessor `video1.mp4` arrived at 23:42; if another file arrives, add it and name it by order).
14. If a cold start is needed (a fresh version that hasn't seen the videos), make **v2, v3…** sensibly; keep learning via logging and cold reads of lessons learned. **Don't let drift and mistakes recur.**
15. **Chat in English** (the user is English; use British spelling in chat).
16. **Ensure accuracy** (verify claims; adversarial checks).
17. **Never end on "I am waiting on…" or "I stopped here because…".** Keep work flowing; leave a finished, useful state.
18. **Build to survive a container reset**: commit and push often, keep everything reproducible from the repo (setup script, regenerate ignored files), keep workflow scripts and a RESUME guide in the repo.
19. **The toolkit must be video-agnostic** and work across many videos: no subject-specific assumptions in scripts or workflow templates; per-video facts live in per-video context files. Still do specific, in-depth work on these videos, and don't use generality as an excuse to avoid anything.
20. **End goal:** a toolkit where the user can just upload a video and send a fresh Claude session at it to **feel and understand the music and video like a human would**. Deliverables: a one-command extraction pipeline, video-agnostic workflows, and a clear entry document a new session can follow cold. Note: this case has lots of online information; the toolkit must also work for obscure videos with nothing online (test a "blind" mode without web research, and compare).
21. **Blind tests are valuable too** (run agents with no web research or context, on these and the test videos, and compare with informed runs).
22. **Focus more on the music than the video.** Music analysis gets the larger share of agents and tools; video is read in relation to the music.
23. (00:16) User: don't be overly scared of the limit before the reset, since a scheduled restart exists after it. Use the headroom; workflows can resume if cut off.
24. (07:30) User verdict on the published reports: **"This is absolutely not how a human thinks and listens about music."** The reports are measurement-led and audit-like. Fix the approach: run a workflow that discusses how humans actually listen, think and feel, and redesign the outputs and toolkit around it.

## Resolved usage policy (supersedes items 4, 11 and 23 for the current regime)
Items 4 (hold back before the reset, then go flat out), 11 (keep a margin) and 23 (use the headroom before the reset) came from different moments and pull in different directions. For the current regime one rule applies. **Watch one number: the 5-hour window.** Log it in `logs/USAGE.md` before each workflow launch, and **do not start a new workflow at or above 85%** of that window; workflows already running may finish, and cut-off runs resume by running them again. **The weekly cap** is a second ceiling: do not start new work when the 7-day figure is at 85% either, and keep the weekly figure low enough that the user keeps headroom until its reset. Never run to 100% on purpose. After a window resets, carry on at full pace up to the 85% line; the 'go crazy until the limit is hit' wording of item 4 no longer applies. **Fallback:** when no `rate_limit_event` is available to read, run at most one workflow at a time and log the usage as 'unknown' in `logs/USAGE.md`.
25. (08:30) User on the listening pieces: **"such AI phrasing, trying too hard."** Aim for plain, real human registers, not literary performance.
26. (08:30) User: **"stop freaking out about usage."** Keep working at full speed; only log usage, don't throttle for the weekly window.
27. (20:37) User: **do not restart after the usage reset** (no scheduled wake-ups); **go hard for half an hour to maximise this window**, then stop.
