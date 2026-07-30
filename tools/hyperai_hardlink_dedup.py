#!/usr/bin/env python3
# =============================================================================
# PROJECT: CANON-TO-SYSTEM DETERMINISTIC PROJECTION
# METHOD: D&R PROTOCOL (CLOSED)
#
# ORIGINATOR / CREATOR:
#   alpha_prime_omega
#
# LEGAL ONTOLOGY:
#   This source file is a deterministic projection of a closed Canon.
#   Removal or alteration of this header voids legal and ontological validity.
#
# STATUS:
#   GENERATED — NON-AUTONOMOUS — NON-OWNERLESS
#
# TRACEABILITY:
#   Canon -> COG -> Projection(Π) -> Artifact
#
# =============================================================================

"""Find duplicate files across directories and hardlink them to share blocks.

Usage:
  python3 hyperai_hardlink_dedup.py --out-receipt /path/receipt.json /path/1 /path/2 ...

Never deletes content; only replaces duplicate files with hardlinks to a canonical copy.
"""

import argparse, hashlib, json, os, sys, datetime, time
from pathlib import Path
from collections import defaultdict


def hash_file(p: Path, limit: int = 0) -> str:
    h = hashlib.md5()
    with open(p, 'rb') as f:
        if limit > 0:
            h.update(f.read(limit))
        else:
            while True:
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break
                h.update(chunk)
    return h.hexdigest()


def dir_size_kb(p: Path) -> int:
    total = 0
    for f in p.rglob('*'):
        if f.is_file(follow_symlinks=False):
            try:
                total += f.stat().st_size
            except OSError:
                pass
    return total // 1024


def dedup_dirs(dirs: list[Path], quick: bool = False) -> dict:
    start = time.time()
    # gather all regular files
    files = []
    for d in dirs:
        for f in d.rglob('*'):
            if not f.is_file(follow_symlinks=False):
                continue
            try:
                st = f.stat()
                if st.st_nlink > 1:
                    continue  # already hardlinked
                files.append((f, st.st_size))
            except OSError:
                continue

    # group by size
    by_size = defaultdict(list)
    for f, size in files:
        by_size[size].append(f)

    # for same-size files, hash first 1MB, then full if first matches
    first_hash = {}
    full_hash = defaultdict(list)
    for size, candidates in by_size.items():
        if len(candidates) == 1:
            continue
        for f in candidates:
            fh = hash_file(f, limit=1024 * 1024)
            first_hash[f] = fh

    # group by first hash
    by_first = defaultdict(list)
    for f, fh in first_hash.items():
        by_first[fh].append(f)

    for fh, candidates in by_first.items():
        if len(candidates) == 1:
            continue
        for f in candidates:
            h = hash_file(f) if not quick else fh
            full_hash[h].append(f)

    # hardlink duplicates
    hardlinks = 0
    freed_bytes = 0
    errors = []
    for h, candidates in full_hash.items():
        if len(candidates) == 1:
            continue
        # sort by path; keep the first (canonical)
        candidates.sort(key=lambda p: str(p))
        canonical = candidates[0]
        for dup in candidates[1:]:
            try:
                dup_size = dup.stat().st_size
                # remove duplicate and hardlink to canonical
                tmp = Path(str(dup) + '.dedup-tmp')
                os.link(canonical, tmp)
                os.replace(tmp, dup)
                hardlinks += 1
                freed_bytes += dup_size
            except Exception as e:
                errors.append({'file': str(dup), 'error': str(e)})

    elapsed = time.time() - start
    return {
        'scanned_files': len(files),
        'hardlinks_created': hardlinks,
        'freed_bytes': freed_bytes,
        'freed_mb': freed_bytes // 1024 // 1024,
        'elapsed_seconds': round(elapsed, 2),
        'errors': errors,
    }


def df_free_kb() -> int:
    import subprocess
    out = subprocess.run(['df', '-k', '/System/Volumes/Data'], capture_output=True, text=True).stdout
    return int(out.splitlines()[1].split()[3])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dirs', nargs='+')
    parser.add_argument('--out-receipt', required=True)
    parser.add_argument('--batch', default='P3', help='batch name for receipt')
    parser.add_argument('--quick', action='store_true', help='use first 1MB hash only (faster, slightly less safe)')
    parser.add_argument('--manifest-out', default=None)
    args = parser.parse_args()

    dirs = [Path(d).resolve() for d in args.dirs]
    started_at = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
    free_before = df_free_kb()
    result = dedup_dirs(dirs, quick=args.quick)
    free_after = df_free_kb()
    completed_at = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

    receipt = {
        'schema_version': '2026-07-27.cleanup-receipt.v1',
        'batch': args.batch,
        'system': 'hardlink_dedup',
        'started_at': started_at,
        'completed_at': completed_at,
        'status': 'ok',
        'freed_kb': result['freed_bytes'] // 1024,
        'freed_mb': result['freed_mb'],
        'free_before_kb': free_before,
        'free_after_kb': free_after,
        'scanned_files': result['scanned_files'],
        'hardlinks_created': result['hardlinks_created'],
        'elapsed_seconds': result['elapsed_seconds'],
        'errors': result['errors'],
        'dirs': [str(d) for d in dirs],
        'notes': 'Hardlinked duplicate files to share blocks; no files deleted'
    }

    out = Path(args.out_receipt)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2))
    print(f'freed_mb: {result["freed_mb"]}')
    print(f'receipt: {out}')
    print(f'df free after: {free_after // 1024} MB')


if __name__ == '__main__':
    main()