"""Locate the data folder (see DATA_LAYOUT.md). Standard library only.

Order: environment variable MASLD_DATA_DIR, then `data_dir:` in config/paths.yaml.
Run as a script to print the data folder (for shell scripts: DATA=$(python tools/paths.py))."""
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CONFIG = REPO / 'config' / 'paths.yaml'

# folder name of each part of the layout, relative to the data folder
LAYOUT = {
    'raw': '01_raw',
    'metadata': '02_metadata',
    'objects': '03_objects',
    'per_study': '03_objects/per_study',
    'qc': '03_objects/qc',
    'sidecars': '03_objects/sidecars',
    'annotation': '04_annotation',
    'integration': '05_integration',
    'models': '05_integration/models',
    'logs': 'logs',
}


def _from_config():
    if not CONFIG.is_file():
        return None
    for line in CONFIG.read_text().splitlines():
        line = line.split('#', 1)[0].strip()
        if line.startswith('data_dir:'):
            value = line.split(':', 1)[1].strip().strip('"').strip("'")
            return value or None
    return None


def data_dir(must_exist=True):
    """The data folder as an absolute Path."""
    value = os.environ.get('MASLD_DATA_DIR') or _from_config()
    if not value:
        raise RuntimeError('No data folder set. Run: python tools/init_data_dir.py /path/to/masld_data '
                           '(or export MASLD_DATA_DIR=/path/to/masld_data). See DATA_LAYOUT.md.')
    p = Path(value).expanduser().resolve()
    if must_exist and not p.is_dir():
        raise FileNotFoundError(f'Data folder {p} does not exist. Run: python tools/init_data_dir.py {p}')
    return p


def path(part, *names):
    """A path inside the layout, e.g. path('raw', 'wang_2023') or path('qc', 'wang_2023.h5ad')."""
    if part not in LAYOUT:
        raise KeyError(f'unknown part {part!r}; one of {sorted(LAYOUT)}')
    return data_dir().joinpath(LAYOUT[part], *names)


if __name__ == '__main__':
    print(data_dir())
