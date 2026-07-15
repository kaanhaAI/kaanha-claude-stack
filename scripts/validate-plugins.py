#!/usr/bin/env python3
"""Validate every plugin manifest in this repo.

Exists because of a hard lesson (2026-07-15): plugin.json's `agents` field
pointed at a directory ("./agents/") instead of individual .md files, and
Claude Code's response to an invalid manifest is to skip the ENTIRE plugin
silently - no skills, no agents, no hooks, no error. The push gate itself
was dead for days and nothing said so.

Checks (stdlib only, exit 1 on any error):
- .claude-plugin/marketplace.json parses; every local plugin source exists.
- every plugins/*/.claude-plugin/plugin.json parses; `name` present;
  `version` present (update detection is version-keyed - the release rule).
- `skills`: string or list of strings; each must be an existing DIRECTORY.
- `agents`: string or list of strings; each must be an existing FILE
  (.md) - a directory value here is THE killer bug this script exists for.
- `hooks`: string/list -> each an existing file containing valid JSON;
  inline object is accepted as-is.
- default-location hooks/hooks.json (even if undeclared) must parse.
- every skill directory (declared or default skills/) has subdirs with a
  SKILL.md that starts with `---` frontmatter.

Run:  python dev/validate_plugins.py        (from anywhere; repo-rooted)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo_root(start):
    d = start
    while True:
        if os.path.isdir(os.path.join(d, "plugins")) or os.path.isdir(
            os.path.join(d, ".claude-plugin")
        ):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            raise SystemExit("could not locate repo root (no plugins/ or .claude-plugin/)")
        d = parent


ROOT = find_repo_root(HERE)
errors = []


def err(msg):
    errors.append(msg)


def load_json(path, what):
    try:
        with open(path, encoding="utf-8-sig") as f:
            return json.load(f)
    except FileNotFoundError:
        err(f"{what}: file not found: {path}")
    except json.JSONDecodeError as e:
        err(f"{what}: INVALID JSON ({e}) in {path}")
    return None


def as_list(v):
    return v if isinstance(v, list) else [v]


def check_plugin(pdir):
    name = os.path.basename(pdir)
    manifest_path = os.path.join(pdir, ".claude-plugin", "plugin.json")
    if not os.path.isfile(manifest_path):
        return  # manifest is optional; defaults auto-discover
    m = load_json(manifest_path, f"{name}/plugin.json")
    if m is None:
        return

    if not m.get("name"):
        err(f"{name}: plugin.json has no 'name' (required)")
    if not m.get("version"):
        err(f"{name}: plugin.json has no 'version' (update detection is version-keyed)")

    # skills: directories
    for s in as_list(m.get("skills") or []):
        if not isinstance(s, str) or not os.path.isdir(os.path.join(pdir, s)):
            err(f"{name}: skills entry {s!r} is not an existing directory")

    # agents: individual FILES - a directory here silently kills the plugin
    for a in as_list(m.get("agents") or []):
        target = os.path.join(pdir, a) if isinstance(a, str) else None
        if target and os.path.isdir(target):
            err(
                f"{name}: agents entry {a!r} is a DIRECTORY - the spec wants "
                f"individual .md file paths (or omit the field for auto-discovery). "
                f"THIS SILENTLY DISABLES THE WHOLE PLUGIN."
            )
        elif not target or not os.path.isfile(target):
            err(f"{name}: agents entry {a!r} is not an existing file")

    # hooks: files containing valid JSON (inline object also allowed)
    hooks = m.get("hooks")
    if hooks is not None and not isinstance(hooks, dict):
        for h in as_list(hooks):
            hp = os.path.join(pdir, h) if isinstance(h, str) else None
            if not hp or not os.path.isfile(hp):
                err(f"{name}: hooks entry {h!r} is not an existing file")
            else:
                load_json(hp, f"{name}: hooks file {h}")

    # default hooks location must parse even when undeclared
    default_hooks = os.path.join(pdir, "hooks", "hooks.json")
    if os.path.isfile(default_hooks):
        load_json(default_hooks, f"{name}: hooks/hooks.json")

    # every skill needs a SKILL.md with frontmatter
    skill_dirs = [os.path.join(pdir, s) for s in as_list(m.get("skills") or [])
                  if isinstance(s, str) and os.path.isdir(os.path.join(pdir, s))]
    default_skills = os.path.join(pdir, "skills")
    if not skill_dirs and os.path.isdir(default_skills):
        skill_dirs = [default_skills]
    for sd in skill_dirs:
        for entry in sorted(os.listdir(sd)):
            sub = os.path.join(sd, entry)
            if not os.path.isdir(sub):
                continue
            sm = os.path.join(sub, "SKILL.md")
            if not os.path.isfile(sm):
                err(f"{name}: skill '{entry}' has no SKILL.md")
                continue
            with open(sm, encoding="utf-8-sig") as f:
                head = f.read(200)
            if not head.lstrip().startswith("---"):
                err(f"{name}: skill '{entry}' SKILL.md missing '---' frontmatter")


def main():
    mp = os.path.join(ROOT, ".claude-plugin", "marketplace.json")
    if os.path.isfile(mp):
        m = load_json(mp, "marketplace.json")
        if m:
            for p in m.get("plugins", []):
                src = p.get("source")
                if isinstance(src, str):  # local path source
                    if not os.path.isdir(os.path.join(ROOT, src)):
                        err(f"marketplace.json: local source {src!r} does not exist")

    plugins_dir = os.path.join(ROOT, "plugins")
    if os.path.isdir(plugins_dir):
        for entry in sorted(os.listdir(plugins_dir)):
            pdir = os.path.join(plugins_dir, entry)
            if os.path.isdir(pdir):
                check_plugin(pdir)

    if errors:
        print(f"PLUGIN VALIDATION FAILED - {len(errors)} error(s):")
        for e in errors:
            print(f"  [X] {e}")
        sys.exit(1)
    print("plugin validation OK - all manifests loadable, no silent-death fields")


if __name__ == "__main__":
    main()
