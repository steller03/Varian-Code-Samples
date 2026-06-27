#!/usr/bin/env python3
"""Enrich probe_queue.md into a linked catalogue TOC.

For every tier-table row:
  - Solution name  -> link to the source folder in the repo (relative `../<path>`,
    looked up by ID from the registry shards' Path column)
  - Probe filename -> link to the probe file (`probes/<file>`)

Validates that every source path and every probe file actually exists; prints a summary
with warnings for anything unmapped or missing. Idempotent (won't double-link).

Usage:
    python enrich_toc.py <docs_dir>

Reads   <docs_dir>/registry/*.md   (ID -> source Path; taxonomy §5: ID=col0, Path=col2)
        <docs_dir>/probe_queue.md  (tier tables: ID=col1, Solution=col2, Probe=col5)
Writes  <docs_dir>/probe_queue.md  (in place; original saved as probe_queue.md.bak)
"""
import os
import re
import sys
import urllib.parse

ID_RE = re.compile(r"^[A-Z]{1,4}\d*-\d+$")   # DW16-16, ESAP-01, W1504-04, DS23-01, ESPL-01 ...


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_data_row(line):
    if not line.lstrip().startswith("|"):
        return False
    c = cells(line)
    return len(c) >= 6 and bool(ID_RE.match(c[1] or ""))


def load_id_paths(reg_dir):
    m = {}
    if not os.path.isdir(reg_dir):
        return m
    for fn in sorted(os.listdir(reg_dir)):
        if not fn.lower().endswith(".md"):
            continue
        for line in open(os.path.join(reg_dir, fn), encoding="utf-8"):
            if not line.lstrip().startswith("|"):
                continue
            c = cells(line)
            if len(c) >= 3 and ID_RE.match(c[0] or ""):
                m[c[0]] = c[2]
    return m


def rel_link(path):
    return "../" + urllib.parse.quote(path, safe="/")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    docs = sys.argv[1]
    queue = os.path.join(docs, "probe_queue.md")
    if not os.path.isfile(queue):
        print("not found:", queue)
        return 2

    id_path = load_id_paths(os.path.join(docs, "registry"))
    probes_dir = os.path.join(docs, "probes")
    original = open(queue, encoding="utf-8").read()

    out = []
    n_rows = n_src = n_probe = 0
    unmapped, no_path, no_probe = [], [], []

    for line in original.splitlines():
        if not is_data_row(line):
            out.append(line)
            continue
        c = cells(line)
        uid = c[1]
        n_rows += 1

        # Solution cell -> link the name (text before ' — ') to the source folder
        sol = c[2]
        if "](" not in sol:
            name, sep, rest = sol.partition(" — ")
            if uid in id_path:
                path = id_path[uid]
                c[2] = f"[{name}]({rel_link(path)}){sep}{rest}"
                n_src += 1
                if not os.path.isdir(os.path.join(docs, "..", path)):
                    no_path.append((uid, path))
            else:
                unmapped.append(uid)

        # Probe cell -> link filename to probes/<file>
        pf = c[5] if len(c) > 5 else ""
        if pf and "](" not in pf:
            c[5] = f"[{pf}](probes/{pf})"
            n_probe += 1
            if not os.path.isfile(os.path.join(probes_dir, pf)):
                no_probe.append((uid, pf))

        out.append("| " + " | ".join(c) + " |")

    with open(queue + ".bak", "w", encoding="utf-8") as f:
        f.write(original)
    with open(queue, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")

    print(f"rows enriched      : {n_rows}")
    print(f"source links built : {n_src}")
    print(f"probe links built  : {n_probe}")
    print(f"unmapped IDs (no source path): {len(unmapped)}")
    for u in unmapped:
        print("   UNMAPPED", u)
    print(f"source paths missing on disk : {len(no_path)}")
    for u, p in no_path:
        print("   NOPATH  ", u, p)
    print(f"probe files missing on disk  : {len(no_probe)}")
    for u, p in no_probe:
        print("   NOPROBE ", u, p)
    ok = not (unmapped or no_path or no_probe)
    print("\nOK \u2705 (backup: probe_queue.md.bak)" if ok
          else "\nREVIEW \u26a0\ufe0f (backup: probe_queue.md.bak)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
