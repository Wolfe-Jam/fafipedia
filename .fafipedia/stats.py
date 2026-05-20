#!/usr/bin/env python3
"""FAFipedia stats — measurement dashboard.

Branches on file shape (same pattern as linter.py):
  - typed-entries (fafipedia.fafi) → composition + drift health
  - substrate-bundle (substrate.fafi) → docs, sections, intro coverage

Run: python3 .fafipedia/stats.py                  # both .fafi files at root
     python3 .fafipedia/stats.py fafipedia.fafi   # one file
"""
import sys
import yaml
from collections import Counter
from pathlib import Path


def file_size_block(paths):
    print("=== FILE SIZE ===")
    total_lines = 0
    total_bytes = 0
    for p in paths:
        size = p.stat().st_size
        lines = sum(1 for _ in open(p, "rb"))
        total_lines += lines
        total_bytes += size
        print(f"  {p.name:20s} {lines:>5d} lines · {size/1024:>6.1f} KB")
    if len(paths) > 1:
        print(f"  {'total':20s} {total_lines:>5d} lines · {total_bytes/1024:>6.1f} KB")


def stats_entries(data, path):
    entries = data.get("entries", [])
    n = len(entries)
    print(f"\n=== {path.name} (curated) ===")
    print(f"  Total entries     {n}")
    if n == 0:
        return

    types = Counter(e.get("type", "?") for e in entries)
    print(f"  By type:          " + " · ".join(f"{t} {c}" for t, c in types.most_common()))

    print(f"  By category:")
    for c, k in Counter(e.get("category", "?") for e in entries).most_common():
        print(f"    {c:14s} {k}")

    eternal_t = sum(1 for e in entries if e.get("eternal") is True)
    eternal_f = sum(1 for e in entries if e.get("eternal") is False)
    print(f"  Eternal ratio     {eternal_t} eternal / {eternal_f} time-bound")

    with_aliases = sum(1 for e in entries if e.get("aliases"))
    print(f"  With aliases      {with_aliases} / {n} ({100*with_aliases//n}%)")

    drift = [e for e in entries
             if e.get("eternal") is False
             and "measured" not in e and "generated" not in e]
    print(f"  Drift smells      {len(drift)} (eternal:false without measured/generated)")


def stats_substrate(data, path):
    docs = data.get("docs", [])
    n = len(docs)
    total_sec = sum(len(d.get("sections", [])) for d in docs)
    with_intro = sum(1 for d in docs if d.get("intro"))
    pct = (100 * with_intro // n) if n else 0
    print(f"\n=== {path.name} (generated) ===")
    print(f"  Total docs        {n}")
    print(f"  Total sections    {total_sec}")
    print(f"  With intro        {with_intro} / {n} ({pct}%)")
    print(f"  Per doc:")
    for d in docs:
        sec = len(d.get("sections", []))
        intro_mark = "intro" if d.get("intro") else "----"
        ref = f"{d.get('repo', '?').replace('Wolfe-Jam/', '')}/{d.get('path', '?')}"
        print(f"    {sec:3d} sections  {intro_mark}  {ref}")


def stats_file(path):
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        print(f"FATAL: {path} is not a valid YAML mapping", file=sys.stderr)
        return 1
    if data.get("type") == "substrate-bundle" or "docs" in data:
        stats_substrate(data, path)
    else:
        stats_entries(data, path)
    return 0


def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["fafipedia.fafi", "substrate.fafi"]
    paths = [Path(t) for t in targets]
    existing = [p for p in paths if p.exists()]
    if not existing:
        print(f"FATAL: none of {targets} exist", file=sys.stderr)
        return 1
    file_size_block(existing)
    rc = 0
    for p in existing:
        rc |= stats_file(p)
    return rc


if __name__ == "__main__":
    sys.exit(main())
