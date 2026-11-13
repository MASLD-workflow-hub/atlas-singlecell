"""Create the data-folder layout and record its location (see DATA_LAYOUT.md). Standard library only.

usage:
  python tools/init_data_dir.py /path/to/masld_data    create the folders, write config/paths.yaml
  python tools/init_data_dir.py --check                which studies have all their downloads in 01_raw/
Never deletes or overwrites data; an existing config/paths.yaml pointing elsewhere is left unchanged."""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.paths import CONFIG, LAYOUT, REPO, data_dir  # noqa: E402


def studies():
    with open(REPO / '00_data_table' / 'table1_studies.csv', newline='') as f:
        return [r['Dataset'] for r in csv.DictReader(f)]


def init(target):
    root = Path(target).expanduser().resolve()
    for sub in LAYOUT.values():
        (root / sub).mkdir(parents=True, exist_ok=True)
    line = f'data_dir: {root}\n'
    if CONFIG.is_file() and CONFIG.read_text().strip() and line.strip() not in CONFIG.read_text():
        print(f'{CONFIG} already points elsewhere; left unchanged. Edit it by hand to switch to {root}.')
    else:
        CONFIG.parent.mkdir(exist_ok=True)
        CONFIG.write_text('# written by tools/init_data_dir.py; personal, not tracked by git\n' + line)
        print(f'wrote {CONFIG}')
    print(f'data folder ready: {root}')
    for sub in LAYOUT.values():
        print(f'  {sub}/')


def check():
    raw = data_dir() / LAYOUT['raw']
    with open(REPO / '01_download' / 'download_manifest.csv', newline='') as f:
        rows = list(csv.DictReader(f))
    complete = 0
    for s in studies():
        files = [r for r in rows if r['study'] == s]
        have = sum((raw / r['target']).is_file() and (raw / r['target']).stat().st_size == int(r['bytes']) for r in files)
        complete += have == len(files)
        print(f"{'complete' if have == len(files) else 'missing ':8}  {have:>2}/{len(files):<2} files  {s}")
    print(f'{complete} of {len(studies())} studies complete in {raw}')


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '--check':
        check()
    elif len(sys.argv) == 2 and not sys.argv[1].startswith('-'):
        init(sys.argv[1])
    else:
        sys.exit(__doc__)
