#!/usr/bin/env python3
"""kaanha-quality lessons store — the machine-readable half of mandate rule 6.

Rule 6 says: record what bites you. Memory files do that in prose, for
humans, for ONE project folder. This store does it in structure: countable,
cross-project, queryable by the shape of the project you are in. That is the
difference between "we wrote it down" and "the stack knows".

Its real job is the promotion question. A lesson you recorded once is a
note; the same lesson recorded three times is an unbuilt guard, and only a
counter can tell you which you have.

LOCAL ONLY. Nothing here is ever transmitted. There is no telemetry in this
stack and adding some would break the promise the update check makes in the
public README ("nothing about you or your repo is sent"). The user's own
machine is the only place their state lives.

CLI:
  python lessons.py --add --rule "..." --believed "..." --was-true "..."
                    [--tags svelte,ci] [--source verifier] [--project PATH]
  python lessons.py --list [--tags a,b] [--limit N]
  python lessons.py --stats          # what keeps biting = what to automate

Store: ~/.claude/plugins/data/kaanha-quality/lessons.jsonl
Append-only, one JSON object per line: a corrupt line costs one lesson,
never the store. Opt out entirely with KAANHA_LESSONS=off.
"""
import argparse
import difflib
import json
import os
import re
import sys
import time

PROMOTE_AT = 3   # a rule seen this many times should be a check, not a memory
SAME_RULE = 0.72  # fingerprint similarity above which two rules are "the same"

# Dropped before fingerprinting: they carry no identity, and one of them
# appearing in a rephrasing must not fork a lesson into two half-counts.
STOPWORDS = {
    "the", "and", "or", "but", "it", "its", "this", "that", "these", "those",
    "them", "they", "is", "are", "was", "were", "be", "been", "being", "to",
    "of", "in", "on", "at", "for", "with", "from", "by", "as", "not", "never",
    "always", "must", "should", "can", "will", "would", "when", "then", "than",
    "so", "if", "you", "your", "we", "our", "into", "onto", "before", "after",
    "does", "did", "has", "have", "had", "just", "only", "also", "very",
}


def disabled():
    return os.environ.get("KAANHA_LESSONS", "").lower() in ("off", "0", "false")


def store_path():
    return os.path.join(
        os.path.expanduser("~"), ".claude", "plugins", "data",
        "kaanha-quality", "lessons.jsonl",
    )


def _stem(w):
    """Crudest useful stemming: 'sources' -> 'source', 'checks' -> 'check'.

    Not linguistics - just enough that a plural cannot split one lesson
    into two half-counts and hide a promotion.
    """
    if len(w) > 4 and w.endswith("s") and not w.endswith(("ss", "us", "is")):
        w = w[:-1]
    return w


def fingerprint(rule):
    """Normalize a rule so re-phrasings of one lesson collide.

    Two phrasings of the same lesson MUST group or the counter is
    decorative — spotting the same thing biting again is the whole job.
    Content words only, stemmed, deduped, order-independent.
    """
    words = re.findall(r"[a-z0-9]+", (rule or "").lower())
    keep = [_stem(w) for w in words if len(w) > 3 and w not in STOPWORDS]
    return " ".join(sorted(set(keep)))[:200]


def _same(fp_a, fp_b):
    """Near-miss grouping: normalization alone cannot survive real drift."""
    if not fp_a or not fp_b:
        return fp_a == fp_b
    if fp_a == fp_b:
        return True
    return difflib.SequenceMatcher(None, fp_a, fp_b).ratio() >= SAME_RULE


def add(rule, believed, was_true, tags=None, source=None, project=None):
    if disabled():
        return None
    rec = {
        "ts": int(time.time()),
        "project": os.path.basename(os.path.abspath(project or os.getcwd())),
        "tags": sorted(set(t.strip().lower() for t in (tags or []) if t.strip())),
        "believed": (believed or "").strip(),
        "was_true": (was_true or "").strip(),
        "rule": (rule or "").strip(),
        "fp": fingerprint(rule),
        "source": (source or "unknown").strip(),
    }
    path = store_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=True) + "\n")
    return rec


def read_all():
    """Every readable lesson. A bad line is skipped, never fatal."""
    path = store_path()
    out = []
    if not os.path.isfile(path):
        return out
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:
                    continue  # one corrupt line must not blind the store
    except OSError:
        pass
    return out


def relevant(tags=None, project=None, limit=3):
    """Lessons that match THIS project: same folder, or a shared tag.

    Untagged lessons only surface in their own project — a lesson with no
    shape cannot be known to apply anywhere else, and guessing would fill
    every session with noise from unrelated work.
    """
    tags = set(t.lower() for t in (tags or []))
    proj = os.path.basename(os.path.abspath(project or os.getcwd()))
    hits = []
    for r in read_all():
        same_project = r.get("project") == proj
        shared = tags & set(r.get("tags") or [])
        if same_project or shared:
            hits.append(r)
    hits.sort(key=lambda r: r.get("ts", 0), reverse=True)

    # One lesson, once. Three recordings of the same bite are ONE thing to
    # tell the reader - the count belongs in the promotion line, not here.
    unique = []
    for r in hits:
        fp = r.get("fp") or fingerprint(r.get("rule"))
        if not any(_same(fp, u.get("fp") or fingerprint(u.get("rule"))) for u in unique):
            unique.append(r)
        if len(unique) >= limit:
            break
    return unique


def stats():
    """Recurrence, most-repeated first — near-miss phrasings grouped.

    Fingerprints are matched by similarity, not equality: real lessons get
    re-typed from memory, and an exact-match counter would report three
    separate 1x notes instead of one 3x alarm.
    """
    groups = []
    for r in read_all():
        fp = r.get("fp") or fingerprint(r.get("rule"))
        for g in groups:
            if _same(fp, g["fp"]):
                g["n"] += 1
                g["tags"] |= set(r.get("tags") or [])
                if r.get("ts", 0) >= g["ts"]:  # newest phrasing represents it
                    g["rule"], g["ts"] = r.get("rule", g["rule"]), r.get("ts", 0)
                break
        else:
            groups.append({
                "fp": fp, "n": 1, "rule": r.get("rule", ""),
                "tags": set(r.get("tags") or []), "ts": r.get("ts", 0),
            })
    groups.sort(key=lambda g: g["n"], reverse=True)
    for g in groups:
        g["tags"] = sorted(g["tags"])
    return groups


def promotable():
    """Lessons that have bitten enough times to deserve a machine check."""
    return [e for e in stats() if e["n"] >= PROMOTE_AT]


def main():
    ap = argparse.ArgumentParser(description="kaanha-quality lessons store")
    ap.add_argument("--add", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--rule")
    ap.add_argument("--believed")
    ap.add_argument("--was-true", dest="was_true")
    ap.add_argument("--tags", default="")
    ap.add_argument("--source")
    ap.add_argument("--project")
    ap.add_argument("--limit", type=int, default=5)
    a = ap.parse_args()

    if disabled():
        print("lessons store is off (KAANHA_LESSONS)")
        return 0

    if a.add:
        if not (a.rule and a.believed and a.was_true):
            print("--add needs --rule, --believed and --was-true", file=sys.stderr)
            return 2
        rec = add(a.rule, a.believed, a.was_true,
                  [t for t in a.tags.split(",") if t.strip()], a.source, a.project)
        # Count the way stats() counts, or --add says 1x while --stats says 3x
        # and the promotion warning never fires where it is most useful.
        n = sum(1 for r in read_all()
                if _same(r.get("fp") or fingerprint(r.get("rule")), rec["fp"]))
        print(f"lesson recorded ({n}x): {rec['rule']}")
        if n >= PROMOTE_AT:
            print(f"  ^ seen {n} times - this should be a CHECK, not a memory.")
        return 0

    if a.stats:
        rows = stats()
        if not rows:
            print("no lessons recorded yet")
            return 0
        for e in rows:
            flag = "  <- promote to a check" if e["n"] >= PROMOTE_AT else ""
            tags = (" [" + ",".join(e["tags"]) + "]") if e["tags"] else ""
            print(f"{e['n']}x  {e['rule'][:90]}{tags}{flag}")
        return 0

    for r in (relevant(tags=[t for t in a.tags.split(",") if t.strip()],
                       limit=a.limit) if a.list else []):
        print(f"[{r.get('project')}] {r.get('rule')}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)  # a lessons failure must never break a session or a task
