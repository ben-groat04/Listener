# Errors and mistakes log

Format: time (UTC) · what went wrong · how it was handled · lesson.

- 23:32 · (pre-v1) First Google Drive download returned a sign-in page because the file was private. · Asked the user to share it; re-downloaded. · Check `file`/content type of any download before trusting it.
- 23:47 · `cd X && (jobs) & pip ...` backgrounded the whole `cd && ...` list, so the following `pip` ran in the old cwd and its log path didn't exist. · Re-ran pip from the right directory. · Put `cd` on its own line before backgrounding jobs.
- 23:55 · Printed a full warning-spammed log (DeprecationWarning x87) into context, wasting usage. · Will always pipe logs through `grep -v Warning | tail`. · Filter noisy logs before reading.
- 23:55 · faster-whisper crashed: installed PyAV version rejects `metadata_errors` kwarg. · Fix by pinning a compatible `av` or feeding numpy audio. · Smoke-test new libraries on a 5 s clip before long runs.
- 00:00 · Committed a ~54 MB WAV (regenerable) and GitHub warned about large files. · Added `.gitignore` for `*.wav`, amended my own unmerged commit and force-pushed (with lease) to my session branch so history stays small. · Ignore regenerable binaries before the first commit.
- 00:05 · REPEATED the 23:47 mistake: `cd X && nohup ... &` backgrounds the cd too, so the next commands ran in the old cwd. · Noticed from 'No such file' errors. · Rule: always put `cd` on its own line (or use absolute paths) when a command backgrounds anything.
- 00:08 · Wikimedia Commons returned HTTP 429 for every media download (shared egress IP). · Switched to Internet Archive CC-licensed music videos. · Have a fallback source for test media.
