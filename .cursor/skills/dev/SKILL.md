---
name: dev
description: Pull the latest main and start the local dev server for The Design Wire, then hand back the preview URL. Use to jump straight into designing without any testing or demo recording.
disable-model-invocation: true
---

# Start the dev environment

Goal: get me into designing as fast as possible. Do NOT run manual tests, and do NOT record any walkthrough videos or screenshots.

1. Get the latest code on `main`:
   - If the working tree is clean, run `git checkout main && git pull origin main`.
   - If there are uncommitted changes, skip the checkout, just run `git pull --ff-only` on the current branch, and tell me you left my branch alone.
2. Start the static site in a persistent tmux terminal named `web`, serving the repo root:
   `python3 -m http.server 8000 --bind 0.0.0.0`
   If port 8000 is already serving (a `web` session already exists), reuse it instead of starting a second server.
3. Health check with one line: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/` and confirm it returns `200`.
4. Reply with just the preview URL `http://localhost:8000/` and a one-line confirmation that the site is live. Nothing else.
