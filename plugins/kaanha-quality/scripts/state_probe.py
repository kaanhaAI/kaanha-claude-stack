#!/usr/bin/env python3
"""kaanha-quality project state probe (SessionStart).

The mandate tells Claude how to work. This tells it where it IS — the facts
about THIS project that a file listing does not reveal and that change what
should happen next: that there is no test command for the gate to run, that
the stack is Svelte so Threlte beats R3F, that a UI project has no brand
spec. Guessing any of these produces confident, wrong work.

It then injects the lessons this project's shape has already earned
(lessons.py), because a lesson recorded in one repo is worthless if it
cannot reach the next one.

Constraints, same as every hook here: stdlib only, ASCII out, no network,
never raises, and SILENT when there is nothing worth saying — a hook that
speaks every session teaches people to skip it.

Opt out: KAANHA_STATE_PROBE=off
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import lessons  # noqa: E402
except Exception:
    lessons = None

MAX_LESSONS = 3


def disabled():
    return os.environ.get("KAANHA_STATE_PROBE", "").lower() in ("off", "0", "false")


def read_json(path):
    try:
        with open(path, encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception:
        return None


def project_root(start):
    """The repo root, not the cwd.

    A session opened in apps/web is still working on the whole project: its
    brand spec, its workspace deps and its scenes live above. Probing the
    cwd alone reports a project that does not exist - it invented a missing
    BRAND.md that was one level up.
    """
    d = os.path.abspath(start)
    for _ in range(6):  # bounded: never walk to the filesystem root
        if os.path.isdir(os.path.join(d, ".git")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return os.path.abspath(start)


def exists(root, *rel):
    return os.path.exists(os.path.join(root, *rel))


def any_exists(root, rels):
    """True if any of these relative paths exists under root or a workspace."""
    for rel in rels:
        if os.path.exists(os.path.join(root, *rel)):
            return True
        for parent in ("apps", "packages", "services"):
            pdir = os.path.join(root, parent)
            if not os.path.isdir(pdir):
                continue
            try:
                for entry in sorted(os.listdir(pdir))[:12]:
                    if os.path.exists(os.path.join(pdir, entry, *rel)):
                        return True
            except OSError:
                continue
    return False


def package_jsons(root):
    """Root package.json plus workspace packages, bounded.

    Monorepos are the normal shape, not the exception: at a pnpm/npm
    workspace root the deps and the test script live in apps/* or
    packages/*, so a root-only probe misses the entire stack AND fires a
    false "no test script" alarm at a package that legitimately has none.
    A false alarm in the first line the reader sees costs more trust than
    silence would.
    """
    found = []
    root_pkg = read_json(os.path.join(root, "package.json"))
    if root_pkg is not None:
        found.append(root_pkg)
    if root_pkg is None and not exists(root, "pnpm-workspace.yaml"):
        return found
    for parent in ("apps", "packages", "services"):
        pdir = os.path.join(root, parent)
        if not os.path.isdir(pdir):
            continue
        try:
            entries = sorted(os.listdir(pdir))[:12]  # bounded: never walk a tree
        except OSError:
            continue
        for entry in entries:
            pkg = read_json(os.path.join(pdir, entry, "package.json"))
            if pkg is not None:
                found.append(pkg)
    return found


def probe(root):
    """Return (facts, tags). Facts are only things worth acting on."""
    facts, tags = [], set()

    if os.name == "nt":
        tags.add("windows")
    if exists(root, ".git"):
        tags.add("git")
    if exists(root, ".github", "workflows"):
        tags.add("github-actions")

    pkgs = package_jsons(root)
    if pkgs:
        tags.add("node")
        deps, scripts = {}, {}
        for pkg in pkgs:
            for key in ("dependencies", "devDependencies"):
                d = pkg.get(key)
                if isinstance(d, dict):
                    deps.update(d)
            s = pkg.get("scripts")
            if isinstance(s, dict):
                scripts.update(s)
        if len(pkgs) > 1:
            tags.add("monorepo")
        for name, tag in (
            ("svelte", "svelte"), ("@sveltejs/kit", "sveltekit"),
            ("next", "next"), ("react", "react"), ("vue", "vue"),
            ("three", "threejs"), ("@threlte/core", "threlte"),
            ("@react-three/fiber", "r3f"), ("gsap", "gsap"),
            ("@playwright/test", "playwright"), ("vitest", "vitest"),
            ("jest", "jest"), ("typescript", "typescript"),
        ):
            if name in deps:
                tags.add(tag)

        has_test = any(k.startswith("test") for k in scripts)
        has_build = "build" in scripts
        if not has_test:
            facts.append(
                "No test script anywhere in this project - kaanha-tester will "
                "have nothing real to run, so the gate cannot prove this "
                "project works. Worth fixing before the first ship."
            )
        if has_build and not has_test:
            tags.add("build-only")

    if exists(root, "pyproject.toml") or exists(root, "requirements.txt"):
        tags.add("python")
    if exists(root, "go.mod"):
        tags.add("go")
    if exists(root, "Cargo.toml"):
        tags.add("rust")

    ui = bool(tags & {"svelte", "sveltekit", "next", "react", "vue"})
    if ui and not (exists(root, "BRAND.md") or exists(root, "docs", "BRAND.md")):
        facts.append(
            "UI project with no BRAND.md - design work here has no spec to "
            "obey, so it will drift. Generate one before the first visual task."
        )
    # Dependency-sniffing alone misses the best case: a hand-written
    # raymarched WebGL scene has no three.js in package.json at all.
    if tags & {"threejs", "threlte", "r3f"} or any_exists(root, [
        ("src", "lib", "scenes"), ("src", "scenes"), ("src", "shaders"),
        ("src", "lib", "shaders"),
    ]):
        tags.add("3d")
        facts.append(
            "3D/WebGL project - kaanha-3d-web applies: build the floors in "
            "from commit one (reduced-motion poster, tab-hidden pause, DPR "
            "cap, dynamic shader loop bounds). They are unaddable later."
        )
    if "sveltekit" in tags and "3d" in tags:
        facts.append(
            "SvelteKit + 3D: if this scene reaches for a framework binding, "
            "Threlte is the Svelte one (R3F is React) - but the ladder starts "
            "below both: raymarched SDF, then vanilla Three."
        )

    if "git" in tags and not exists(root, ".github", "workflows"):
        facts.append(
            "Git repo with no GitHub workflows - no cloud watcher, no "
            "dependency audit. enroll_cloud stamps them in one command."
        )

    return facts, sorted(tags)


def main():
    if disabled():
        return
    root = project_root(os.getcwd())
    facts, tags = probe(root)

    lines = []
    if facts:
        lines.append("[kaanha-quality] This project's state (probed, not assumed):")
        lines += ["- " + f for f in facts]

    if lessons is not None:
        try:
            hits = lessons.relevant(tags=tags, project=root, limit=MAX_LESSONS)
            if hits:
                lines.append(
                    "Lessons this project's shape has already earned - do not "
                    "relearn them:"
                )
                for r in hits:
                    where = r.get("project") or "?"
                    lines.append(f"- ({where}) {r.get('rule')}")
            for e in lessons.promotable():
                lines.append(
                    f"- This has bitten {e['n']}x: \"{e['rule'][:80]}\". "
                    f"Stop remembering it - build the check that enforces it."
                )
        except Exception:
            pass

    if lines:
        print("\n".join(lines))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # never break a session over context enrichment
    sys.exit(0)
