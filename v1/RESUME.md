# After a container reset

1. Read the rules (steps 0-1 of [../TOOLKIT.md](../TOOLKIT.md)), then run `bash v1/scripts/00_setup.sh`: it reinstalls libraries and regenerates the git-ignored WAV files.
2. Read the Current state table at the top of [PROGRESS.md](PROGRESS.md) and [logs/ERRORS.md](logs/ERRORS.md). Restart `bash v1/scripts/autocommit.sh &` (commits and pushes every 2 minutes).
3. Continue from the gaps in that table, following the stages and usage policy in [../TOOLKIT.md](../TOOLKIT.md). Existing output files mean a unit is done; workflows skip finished work.
