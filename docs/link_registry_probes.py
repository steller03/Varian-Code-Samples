#!/usr/bin/env python3
"""Make each registry shard's Probe cell a clickable link.

Walks <docs_dir>/registry/*.md and rewrites any Probe cell that names a probe file
(`→ probes/<file>` or a bare `<file>.md`) into `[<original text>](../probes/<file>)`.
Validates the target exists. Idempotent. Edits in place — use git to review/revert.

Usage: python link_registry_probes.py <docs_dir>
"""
import os
import re
import sys

ID_RE = re.compile(r"^[A-Z]{1,4}\d*-\d+$")
PROBE_RE = re.compile(r"([\w.\-]+\.md)\s*$")   # trailing probe filename in the cell


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    docs = sys.argv[1]
    reg = os.path.join(docs, "registry")
    probes = os.path.join(docs, "probes")
    if not os.path.isdir(reg):
        print("not found:", reg)
        return 2

    total = linked = 0
    missing = []
    for fn in sorted(os.listdir(reg)):
        if not fn.lower().endswith(".md"):
            continue
        path = os.path.join(reg, fn)
        out, changed = [], False
        for line in open(path, encoding="utf-8").read().splitlines():
            c = cells(line)
            if not (line.lstrip().startswith("|") and c and ID_RE.match(c[0] or "")):
                out.append(line)
                continue
            total += 1
            cell = c[-1]
            m = PROBE_RE.search(cell) if (cell and "](" not in cell) else None
            if m:
                f = m.group(1)
                c[-1] = f"[{cell}](../probes/{f})"
                linked += 1
                changed = True
                if not os.path.isfile(os.path.join(probes, f)):
                    missing.append((fn, f))
                out.append("| " + " | ".join(c) + " |")
            else:
                out.append(line)
        if changed:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("\n".join(out) + "\n")

    print(f"shard rows scanned : {total}")
    print(f"probe cells linked : {linked}")
    print(f"probe files missing: {len(missing)}")
    for s, f in missing:
        print("   NOPROBE", s, f)
    ok = not missing
    print("\nOK \u2705" if ok else "\nREVIEW \u26a0\ufe0f")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
