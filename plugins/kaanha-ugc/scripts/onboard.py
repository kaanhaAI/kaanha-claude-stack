#!/usr/bin/env python3
"""SessionStart onboarding for kaanha-ugc.

Tells the user the skill is installed and how to use it - once - and keeps
nudging only while a prerequisite is still missing. Silent on every session
after the first successful setup, so it never becomes noise.

stdlib only. Never fails the session: any error exits 0 quietly.
"""
import os
import shutil
import sys

def main() -> int:
    try:
        home = os.path.expanduser("~")
        stamp_dir = os.path.join(home, ".kaanha")
        stamp = os.path.join(stamp_dir, "ugc-onboarded")

        has_ffmpeg = shutil.which("ffmpeg") is not None

        # ASCII only - this prints to arbitrary consoles (Windows cp1252
        # included); a non-encodable char would raise and be swallowed by
        # the guard below, silently breaking onboarding on Windows.
        if not has_ffmpeg:
            # Prereq missing - nudge every session until it's fixed.
            print(
                "[kaanha-ugc] installed, but ffmpeg is missing. "
                "Install it (Windows: winget install Gyan.FFmpeg | "
                "macOS: brew install ffmpeg), then install a video engine "
                "(watch-skill). Say 'how does kaanha-ugc work' for the guide."
            )
            return 0

        if not os.path.exists(stamp):
            # First run with prereqs present - welcome once, then go quiet.
            print(
                "[kaanha-ugc] ready. Point it at a video and say "
                "'run a UGC analysis on <url or file>' - it reads the "
                "hook, retention, scroll-stops, CTA, and best clips, then "
                "writes an HTML report. Needs a video engine installed "
                "(watch-skill recommended, or claude-video). "
                "Say 'how does kaanha-ugc work' for the full guide."
            )
            os.makedirs(stamp_dir, exist_ok=True)
            with open(stamp, "w", encoding="utf-8") as fh:
                fh.write("onboarded\n")
        return 0
    except Exception:
        # Onboarding must never break a session.
        return 0

if __name__ == "__main__":
    sys.exit(main())
