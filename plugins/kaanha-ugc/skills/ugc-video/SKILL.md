---
name: ugc-video
description: Creator/UGC analysis of a video — hooks, retention, scroll-stops, CTA, best clips, and platform captions. Use when the user wants their (or a competitor's) short-form or long-form video analysed for social performance, when they ask to "find the hook", "score retention", "pull the best clips", "make Reels/TikTok/Shorts from this", "write captions for this video", or "why isn't this video performing". NOT for generic "what happens in this video" questions — that is the raw video engine (watch-skill / claude-video), which this skill sits on top of.
---

# kaanha UGC video analysis

This skill is the **creator-analytics layer**. It does not read video itself
— it orchestrates a video **engine** to get the evidence, then applies the
creator lenses and writes a report. Two never fight: the engine gets
*frames + transcript + timeline*; this skill decides *what that means for a
creator*.

## Step 0 — Get the evidence from an engine

Do NOT try to decode video yourself. Use whichever engine is installed
(check both; prefer the first that is available):

- **watch-skill** (`oxbshw/watch-skill`) — preferred. It has persistent
  memory, so once a video is analysed you can re-query it and search across
  a whole library. Use its analyse/search interface (MCP tools or CLI) to
  pull the transcript, timestamped frames, and any scene/OCR data.
- **claude-video** (`bradautomates/claude-video`) — the lightweight
  fallback. Its `/watch <url|file>` returns timestamped frames + transcript
  for a single video, no memory.

**If a prerequisite is missing, install what you can before asking the
user to do anything.** Run the setup script first:

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/setup.py"
```

It installs `ffmpeg` via the platform's package manager (winget / brew /
apt-dnf-pacman) and reports what it did. It CANNOT install the engine
plugin or add API keys — those are in-app / credential actions — so it
prints the exact `/plugin install` line and the (optional) key step for
the user. Relay those, then STOP until the engine is present. Do not
fabricate an analysis without real frames and a real transcript.

**Prerequisite honesty:** if the engine returns a *sparse* frame scan (long
video, capped mode), say so — a hook read on the first 3 seconds is
reliable; a retention curve over a 40-minute video from 100 sampled frames
is an estimate, not a measurement.

## Step 1 — Run the creator lenses

Apply these to the evidence. Every lens cites timestamps from the transcript
/ frames — no claim without a `MM:SS` anchor.

1. **Hook (0–3s).** What happens in the first three seconds? Score it on
   three concrete axes — *visual motion*, *spoken/So-what promise*, *pattern
   interrupt* — and quote the opening line. A weak hook is the single most
   common reason short-form dies; be specific about why, not "make it
   punchier".
2. **Retention / pacing (heuristic).** Map the energy over time: shot
   changes per 10s, dead air (silence + static frame), tangents, and the
   longest stretch with no new information. Flag the **first likely
   drop-off point** with a timestamp. Label this a *heuristic*, never a
   predicted retention %.
3. **Scroll-stop moments.** List timestamps where a visual or verbal
   pattern-interrupt would stop a scroll (a cut, a reveal, a bold claim, a
   face-to-camera). These become clip in-points.
4. **CTA.** Is there a call to action? Where (timestamp), and is it early
   enough to catch people who won't finish? If none, say so plainly.
5. **Story structure.** Name the shape it actually has (hook → build →
   payoff → CTA, or listicle, or demo, or none) and where it breaks.
6. **Best-clip candidates.** Propose 2–4 clips with in/out timestamps, each
   with a one-line reason and a target platform (Reels/TikTok/Shorts vertical
   ≤60s; LinkedIn ≤90s landscape). Ground every in-point in a scroll-stop
   moment from lens 3.

## Step 2 — Generate the outputs the user asked for

Only what they asked for — do not dump all of these every time:

- **Captions / subtitles** — from the transcript, timed, tight, spoken-word
  cleaned (remove filler, keep voice).
- **Platform posts** — a caption + hashtag set per named platform, in the
  creator's own voice (match the transcript's register; do not invent a
  brand voice). If the user has a brand spec, read it.
- **Thumbnail candidates** — 2–3 frame timestamps that would read at small
  size (a clear face / a bold on-screen word / a peak-action frame).
- **Chapter markers / YouTube chapters** — from scene + transcript.

## Step 3 — Write the report (HTML, in place)

Deliverables are **self-contained HTML, rewritten in place, never dated
copies, and you never ask permission** — this is the house rule. Write to
`docs/reports/ugc-<video-slug>.html` (or a path the user names): the lens
scores up top, the clip table with timestamps, the generated captions/posts,
and a one-line verdict. Light/dark aware, no external requests. If a reports
index exists, link it there.

## Honesty rules (non-negotiable)

- **No invented metrics.** Never write "this will get 2× retention" or a made
  up view/engagement number. You have the video, not its analytics. Scores
  are labelled heuristics with the axes shown; predictions are forbidden.
- **Every claim has a timestamp.** "The energy drops" is useless; "static
  talking-head from 0:48 to 1:22 with no new point" is a note the creator
  can act on.
- **The creator's voice is theirs.** Captions and posts match the
  transcript's register. You are editing their voice, not replacing it.
- **Competitor analysis is structural, not a copy order.** When analysing
  someone else's video, extract the *pattern* (why the hook works), never
  reproduce their exact script or assets.
