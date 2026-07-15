#!/usr/bin/env python3
"""kaanha-ugc setup - detect and install prerequisites.

Run by the skill (Step 0) when a prerequisite is missing, or by hand:
    python setup.py            # detect + install what's missing
    python setup.py --check    # detect only, install nothing

Installs ffmpeg via the platform package manager. It CANNOT install the
video-engine plugin (watch-skill / claude-video) or add API keys - those
are in-app / credential actions - so it detects and instructs for those.

stdlib only. ASCII output (Windows consoles choke on non-ASCII).
"""
import argparse
import platform
import shutil
import subprocess
import sys


def have(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def run(cmd: list) -> tuple:
    """Run a command, return (ok, combined_output)."""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        return p.returncode == 0, (p.stdout or "") + (p.stderr or "")
    except FileNotFoundError:
        return False, f"{cmd[0]}: not found"
    except subprocess.TimeoutExpired:
        return False, f"{cmd[0]}: timed out"
    except Exception as e:  # pragma: no cover
        return False, str(e)


def install_ffmpeg() -> bool:
    """Install ffmpeg using whichever package manager exists. Returns success."""
    system = platform.system()
    if system == "Windows":
        if have("winget"):
            print("Installing ffmpeg via winget...")
            ok, out = run([
                "winget", "install", "--id", "Gyan.FFmpeg", "-e",
                "--accept-source-agreements", "--accept-package-agreements",
            ])
            print(out.strip()[-500:])
            if ok:
                print("ffmpeg installed. Restart the app/shell so PATH updates.")
            return ok
        print("winget not found. Install ffmpeg manually: https://www.gyan.dev/ffmpeg/builds/")
        return False
    if system == "Darwin":
        if have("brew"):
            print("Installing ffmpeg via Homebrew...")
            ok, out = run(["brew", "install", "ffmpeg"])
            print(out.strip()[-500:])
            return ok
        print("Homebrew not found. Install it (https://brew.sh) then: brew install ffmpeg")
        return False
    # Linux
    for mgr, cmd in (
        ("apt-get", ["sudo", "apt-get", "install", "-y", "ffmpeg"]),
        ("dnf", ["sudo", "dnf", "install", "-y", "ffmpeg"]),
        ("pacman", ["sudo", "pacman", "-S", "--noconfirm", "ffmpeg"]),
    ):
        if have(mgr):
            print(f"Installing ffmpeg via {mgr}...")
            ok, out = run(cmd)
            print(out.strip()[-500:])
            return ok
    print("No known package manager. Install ffmpeg via your distro's package manager.")
    return False


def engine_present() -> bool:
    """Best-effort detection of an installed video engine.

    The engines register as plugins / CLIs. We check for their CLI entry
    points on PATH; absence is not proof (a plugin-only install may not add
    a CLI), so this is advisory only.
    """
    return have("watch-skill") or have("watch") or have("claude-video")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="detect only, install nothing")
    args = ap.parse_args()

    print("kaanha-ugc setup")
    print("-" * 40)

    # 1) Python (we're running, so it's fine) + ffmpeg.
    print(f"python: OK ({platform.python_version()})")

    ff = have("ffmpeg")
    print(f"ffmpeg: {'OK' if ff else 'MISSING'}")
    if not ff and not args.check:
        ff = install_ffmpeg()
        # Re-check on PATH may need a restart; report honestly.
        if not ff:
            ff = have("ffmpeg")

    # 2) Engine (advisory - cannot auto-install a plugin).
    eng = engine_present()
    print(f"video engine (watch-skill/claude-video): {'detected' if eng else 'not detected on PATH'}")

    # 3) Verdict + the steps only the user can take.
    print("-" * 40)
    if ff and eng:
        print("READY. Say: run a UGC analysis on <url or file>")
        return 0

    print("Remaining steps (these need YOU, in-app / credential actions):")
    if not ff:
        print("  - ffmpeg still missing: install it, then restart the app/shell.")
    if not eng:
        print("  - Install a video engine plugin (in the app):")
        print("      /plugin install watch-skill@kaanha    (recommended, has memory)")
        print("      /plugin install claude-video@kaanha    (lightweight)")
        print("    Optional: a Groq/Gemini key for cloud-quality transcription/vision")
        print("    (or run watch-skill offline with local Whisper + Ollama, free).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
