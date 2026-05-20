#!/usr/bin/env python3
"""FAFipedia linter — schema + drift smells.

Branches on file shape:
  - typed-entries (e.g., fafipedia.fafi) → schema + drift checks per entry
  - substrate-bundle (substrate.fafi)    → sha + sections presence; intro warns

Run: python3 .fafipedia/linter.py <file.fafi> [<file2.fafi> ...]
"""
import sys
import yaml
from pathlib import Path

VALID_TYPES = {"Fact", "Procedure", "Index"}
VALID_CATEGORIES = {
    "format", "stack", "architecture", "agent",
    "ecosystem", "infrastructure", "philosophy",
}
REQUIRED = ("id", "type", "category", "key", "value", "eternal", "source")


def lint_entries(data, path):
    errors = []
    for entry in data.get("entries", []):
        eid = entry.get("id", "<no-id>")
        for field in REQUIRED:
            if field not in entry:
                errors.append(f"{path}:{eid}: missing required field '{field}'")
        t = entry.get("type")
        if t and t not in VALID_TYPES:
            errors.append(f"{path}:{eid}: invalid type '{t}' (allowed: {sorted(VALID_TYPES)})")
        c = entry.get("category")
        if c and c not in VALID_CATEGORIES:
            errors.append(f"{path}:{eid}: invalid category '{c}' (allowed: {sorted(VALID_CATEGORIES)})")
        # eternal:false requires time-provenance — `measured` (for facts) OR
        # `generated` (for derived entries like the A-Z index)
        if entry.get("eternal") is False and "measured" not in entry and "generated" not in entry:
            errors.append(f"{path}:{eid}: eternal:false without 'measured' or 'generated' (drift smell)")
    return errors


def lint_substrate(data, path):
    errors = []
    for doc in data.get("docs", []):
        ref = f"{doc.get('repo', '<no-repo>')}/{doc.get('path', '<no-path>')}"
        if not doc.get("sha"):
            errors.append(f"{path}:{ref}: missing 'sha' (drift-honesty)")
        if not doc.get("sections"):
            errors.append(f"{path}:{ref}: empty 'sections' (no prose-strong content)")
        # empty intro is the honest sentinel — warn, don't fail (signals source
        # README would benefit from an `<!-- faf: ... -->` meta line)
        if doc.get("intro", "") == "":
            print(f"WARN {path}:{ref}: intro empty (consider faf-meta in source README)")
    return errors


def lint_file(path_str):
    path = Path(path_str)
    if not path.exists():
        print(f"FATAL: {path} does not exist", file=sys.stderr)
        return 1
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        print(f"FATAL: {path} is not a valid YAML mapping", file=sys.stderr)
        return 1
    if data.get("type") == "substrate-bundle" or "docs" in data:
        errors = lint_substrate(data, path)
    else:
        errors = lint_entries(data, path)
    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK {path}")
    return 0


if __name__ == "__main__":
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["fafipedia.fafi"]
    rc = 0
    for t in targets:
        rc |= lint_file(t)
    sys.exit(rc)
