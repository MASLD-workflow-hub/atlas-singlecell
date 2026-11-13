#!/usr/bin/env python
"""Download the public data of the 28 atlas studies into <data folder>/01_raw/ (standard library only).

Reads 01_download/download_manifest.csv: one row per file, with its URL, size and checksum. Each file goes to
<data folder>/01_raw/<accession>/<file>. A file that two studies share is downloaded once.

  python 01_download/scripts/download.py                      # everything (about 84 GB)
  python 01_download/scripts/download.py --study wang_2023 gribben_2024
  python 01_download/scripts/download.py --role counts        # count matrices only, without the author label files
  python 01_download/scripts/download.py --dry-run            # list what would be fetched, and the size
  python 01_download/scripts/download.py --verify             # re-check the checksums of files already on disk

Safe to interrupt and run again: a partial file (.part) resumes where it stopped, and a complete file is skipped.
A file is complete when its size matches the manifest; after a download its sha256 (or the publisher's md5) is checked
too, and a mismatch stops the run with the file kept as .bad for inspection."""
import argparse
import csv
import hashlib
import shutil
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from tools.paths import path  # noqa: E402

MANIFEST = REPO / '01_download' / 'download_manifest.csv'
CHUNK = 8 << 20
UA = {'User-Agent': 'atlas-singlecell-downloader'}


def human(n):
    for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
        if n < 1024 or unit == 'TB':
            return f'{n:.1f} {unit}' if unit != 'B' else f'{n} B'
        n /= 1024


def checksum_ok(p, row):
    """sha256 (our download) if recorded, else the publisher's md5, else size only."""
    if row['sha256']:
        algo, want = hashlib.sha256(), row['sha256']
    elif row['md5']:
        algo, want = hashlib.md5(), row['md5']
    else:
        return True, 'size'
    with open(p, 'rb') as f:
        while chunk := f.read(CHUNK):
            algo.update(chunk)
    return algo.hexdigest() == want, algo.name


def fetch(row, dest, retries=5):
    part = dest.with_name(dest.name + '.part')
    size = int(row['bytes'])
    for attempt in range(1, retries + 1):
        have = part.stat().st_size if part.exists() else 0
        if have > size:
            part.unlink(); have = 0
        if have == size:
            break
        req = urllib.request.Request(row['url'], headers=dict(UA, **({'Range': f'bytes={have}-'} if have else {})))
        try:
            with urllib.request.urlopen(req, timeout=120) as resp, open(part, 'ab' if have else 'wb') as out:
                if have and resp.status != 206:          # server ignored the range: start again
                    out.truncate(0); have = 0
                t0, done = time.time(), have
                while chunk := resp.read(CHUNK):
                    out.write(chunk); done += len(chunk)
                    rate = (done - have) / max(time.time() - t0, 1e-6)
                    print(f'\r    {human(done)} / {human(size)}  {human(rate)}/s   ', end='', flush=True)
                print()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            print(f'\n    attempt {attempt} failed: {e}; retrying in {10 * attempt} s')
            time.sleep(10 * attempt)
    if not part.exists() or part.stat().st_size != size:
        raise SystemExit(f'could not download {row["url"]} (size mismatch after {retries} attempts)')
    ok, how = checksum_ok(part, row)
    if not ok:
        bad = dest.with_name(dest.name + '.bad'); part.rename(bad)
        raise SystemExit(f'{how} mismatch for {dest.name}; kept as {bad}. Delete it and run again.')
    part.rename(dest)
    return how


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--study', nargs='+', help='only these studies (Dataset column of 00_data_table/table1_studies.csv)')
    ap.add_argument('--role', choices=['counts', 'author_metadata'], help='only this kind of file')
    ap.add_argument('--dry-run', action='store_true', help='list the files and sizes, download nothing')
    ap.add_argument('--verify', action='store_true', help='also checksum files already on disk')
    a = ap.parse_args()

    rows = list(csv.DictReader(open(MANIFEST, newline='')))
    studies = sorted({r['study'] for r in rows})
    if a.study:
        unknown = set(a.study) - set(studies)
        if unknown:
            sys.exit(f'unknown study: {", ".join(sorted(unknown))}. Known: {", ".join(studies)}')
        rows = [r for r in rows if r['study'] in a.study]
    if a.role:
        rows = [r for r in rows if r['role'] == a.role]
    files = {}
    for r in rows:                                       # one entry per target file, with every study that uses it
        files.setdefault(r['target'], dict(r, studies=[]))['studies'].append(r['study'])

    raw = path('raw')
    todo = [f for t, f in files.items() if not (raw / t).exists()]
    total, need = sum(int(f['bytes']) for f in files.values()), sum(int(f['bytes']) for f in todo)
    print(f'{len(files)} files ({human(total)}) for {len({s for f in files.values() for s in f["studies"]})} studies; '
          f'{len(todo)} to download ({human(need)}) into {raw}')
    if a.dry_run:
        for t, f in sorted(files.items()):
            state = 'on disk' if (raw / t).exists() else 'to fetch'
            print(f'  {state:8}  {human(int(f["bytes"])):>9}  {t}   ({", ".join(f["studies"])})')
        return
    free = shutil.disk_usage(raw).free
    if need > free:
        sys.exit(f'not enough space: need {human(need)}, {human(free)} free on {raw}')

    log = path('logs', f'download_{time.strftime("%Y%m%d_%H%M%S")}.tsv')
    with open(log, 'w') as lg:
        lg.write('target\tstatus\tcheck\n')
        for i, (t, f) in enumerate(sorted(files.items()), 1):
            dest = raw / t
            dest.parent.mkdir(parents=True, exist_ok=True)
            print(f'[{i}/{len(files)}] {t}  ({human(int(f["bytes"]))}; {", ".join(f["studies"])})')
            if dest.exists():
                if dest.stat().st_size != int(f['bytes']):
                    sys.exit(f'    {dest} exists with a different size than the manifest; move it away and run again')
                status, how = 'on disk', 'size'
                if a.verify:
                    ok, how = checksum_ok(dest, f)
                    if not ok:
                        sys.exit(f'    {how} mismatch for {dest}; delete it and run again')
                print(f'    on disk ({how} ok)')
            else:
                status, how = 'downloaded', fetch(f, dest)
                print(f'    done ({how} ok)')
            lg.write(f'{t}\t{status}\t{how}\n')
    print(f'all {len(files)} files present; log: {log}')


if __name__ == '__main__':
    main()
