#!/usr/bin/env python3
"""Verify a triage registry shard against the filesystem.

Usage:
    python docs/verify_shard.py <repo_root> "<target_folder>" <shard.md>

Checks, per the Dispatch 1 / 1b unit definition:
  * Each ``.sln`` under <target_folder> is one unit and must be represented by
    exactly one row in the shard (matched on the solution's folder path, which
    appears in the shard's "Path" column).
  * MISSED  -> a ``.sln`` whose folder is not referenced by any shard row.
  * PHANTOM -> a shard "Path" cell that does not exist on disk.
  * INFO    -> a loose ``.cs`` script: a ``.cs`` with no ancestor ``.csproj``
    inside the target folder (i.e. a standalone single-file script, not project
    source). Each INFO line must be reconciled by hand: either it is the
    single-file twin of a catalogued unit (skip) or a unique script that should
    have its own row.

Exit code is non-zero when MISSED or PHANTOM is non-zero.

Note: for script-only folders (e.g. ESPL) there are no ``.sln`` files to diff
against, so MISSED/PHANTOM are trivially 0 and the INFO list IS the unit list;
confirm by hand that the shard has one row per INFO script.
"""
import os
import re
import sys


def repo_rel(path, root):
    return os.path.relpath(path, root).replace(os.sep, "/")


def find_files(folder, suffix):
    out = []
    for dirpath, dirnames, filenames in os.walk(folder):
        # ignore build output
        dirnames[:] = [d for d in dirnames if d not in ("bin", "obj", ".git", ".vs")]
        for f in filenames:
            if f.endswith(suffix):
                out.append(os.path.join(dirpath, f))
    return out


def has_ancestor_csproj(cs_path, folder):
    """True if any directory at-or-above the .cs (up to <folder>) holds a .csproj."""
    d = os.path.dirname(os.path.abspath(cs_path))
    stop = os.path.dirname(os.path.abspath(folder))
    while d and d != stop:
        if any(n.endswith(".csproj") for n in os.listdir(d)):
            return True
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return False


def parse_shard_paths(shard_file):
    """Return the set of repo-relative paths from the shard table's Path column."""
    paths = []
    with open(shard_file, encoding="utf-8") as fh:
        for line in fh:
            if not line.lstrip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3:
                continue
            first = cells[0].lower()
            if first in ("id", "col") or set(cells[0]) <= set("-: "):
                continue  # header / separator
            paths.append(cells[2])  # Path is the 3rd column per taxonomy §5
    return paths


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(2)
    root, folder, shard = sys.argv[1], sys.argv[2], sys.argv[3]
    folder_abs = os.path.join(root, folder)
    if not os.path.isdir(folder_abs):
        print(f"ERROR: folder not found: {folder_abs}")
        sys.exit(2)

    slns = find_files(folder_abs, ".sln")
    sln_dirs = sorted({repo_rel(os.path.dirname(s), root) for s in slns})
    shard_paths = parse_shard_paths(shard)
    shard_set = set(shard_paths)

    # MISSED: an .sln folder not covered by any shard row (allow the shard path
    # to be the sln folder itself or an ancestor/descendant match).
    missed = []
    for d in sln_dirs:
        if not any(d == p or d.startswith(p + "/") or p.startswith(d + "/") for p in shard_set):
            missed.append(d)

    # PHANTOM: a shard path that doesn't resolve to a real file or folder.
    phantom = []
    for p in shard_paths:
        if not os.path.exists(os.path.join(root, p)):
            phantom.append(p)

    # INFO: loose .cs (no ancestor .csproj within the folder).
    loose = []
    for cs in find_files(folder_abs, ".cs"):
        if not has_ancestor_csproj(cs, folder_abs):
            loose.append(repo_rel(cs, root))

    print(f"FOLDER  {folder}")
    print(f"SHARD   {shard}")
    print(f".sln units found: {len(sln_dirs)}   shard rows: {len(shard_paths)}")
    for d in sln_dirs:
        print(f"  SLN  {d}")
    for p in sorted(loose):
        print(f"  INFO loose .cs  {p}")
    for d in missed:
        print(f"  MISSED  {d}")
    for p in phantom:
        print(f"  PHANTOM {p}")
    print(f"MISSED {len(missed)}  PHANTOM {len(phantom)}  INFO {len(loose)}")
    sys.exit(1 if (missed or phantom) else 0)


if __name__ == "__main__":
    main()
