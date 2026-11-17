# After a container reset

1. Do steps 1-2 of [../TOOLKIT.md](../TOOLKIT.md) (read the rules; `bash v1/scripts/00_setup.sh`, which reinstalls libraries and regenerates the git-ignored WAV files).
2. Read [PROGRESS.md](PROGRESS.md) (the Current state table at the top says what is done) and [logs/ERRORS.md](logs/ERRORS.md).
3. Continue from the gaps in the table. Existing output files mean that unit is done; workflow prompts skip finished work.

Notes: `scripts/autocommit.sh` commits and pushes every 2 minutes while the session lives (restart it if the container was reset); still commit and push after every workflow. Check usage before large workflows (`v1/logs/USAGE.md`).
