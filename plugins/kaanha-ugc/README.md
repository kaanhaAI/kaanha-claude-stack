# kaanha-ugc

Creator/UGC analysis for video — the layer that turns a video into a
*performance* report: hook, retention, scroll-stops, CTA, best clips, and
platform captions.

## What it is (and isn't)

kaanha-ugc **does not read video itself.** It sits on top of a video
**engine** that extracts frames + transcript, and it adds the creator
reasoning. Two layers:

| Layer | Job | Ships as |
|---|---|---|
| **Engine** | Decode the video → timestamped frames + transcript | `watch-skill` (recommended, has memory) or `claude-video` (lightweight) — separate plugins |
| **kaanha-ugc** (this) | Analyse that for a creator → hooks, retention, clips, captions | this skill |

So on its own kaanha-ugc is half the package — it needs an engine under it.

## Prerequisites (install once)

1. **ffmpeg** on PATH — every engine needs it.
   Windows `winget install Gyan.FFmpeg` · macOS `brew install ffmpeg` · Linux `apt install ffmpeg`.
2. **A video engine plugin** — install `watch-skill` (recommended) or
   `claude-video`. watch-skill runs local-first and free (local Whisper +
   Ollama); add a Gemini/Claude/OpenAI vision key only for cloud quality.
3. Python 3.8+ (for this skill's onboarding hook) — usually already present.

On the first session after everything's in place, kaanha-ugc prints a one
line "ready" message; if ffmpeg is missing it prints the fix. It never
nags after setup is complete.

## How it works, end to end

```
you: "run a UGC analysis on my-reel.mp4"
        │
        ▼
kaanha-ugc asks the engine for frames + transcript + timeline
        │
        ▼
applies the creator lenses (each claim anchored to a MM:SS timestamp):
  hook (0–3s) · retention/pacing heuristic · scroll-stop moments ·
  CTA placement · story structure · best-clip candidates per platform
        │
        ▼
writes a self-contained HTML report + any captions/posts you asked for
```

## Use it

- `run a UGC analysis on <url or file>`
- `find the hook in this video`
- `pull the 3 best clips for Reels from this`
- `write TikTok captions for this`
- `why isn't this video performing?`

It works in **every project** once installed — skills are global, not
per-project.

## The honesty rules it follows

- **No invented metrics.** It has the video, not its analytics. Scores are
  labelled heuristics with their axes shown; predicted view/retention
  numbers are forbidden.
- **Every claim has a timestamp.** "The energy drops" is useless;
  "static talking-head 0:48–1:22, no new point" is actionable.
- **Your voice stays yours.** Captions/posts match the transcript's
  register — it edits your voice, it doesn't replace it.
- **Competitor analysis is structural** — it extracts *why* a hook works,
  never copies the script or assets.

MIT. Part of the kaanha stack.
