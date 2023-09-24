import zipfile
from pathlib import Path

import config


def get_zip_file(p: Path, file) -> bytes:
    p = Path(p)
    if not p.is_absolute():
        p = config.root / p
    z = zipfile.ZipFile(p, 'r')
    filedata = None
    with z.open(file) as f:
        filedata = f.read()
    return filedata


def get_dir_file(p: Path, file) -> bytes:
    p = Path(p)
    if not p.is_absolute():
        p = config.root / p
    filedata = None
    with open(p / Path(file), 'rb') as f:
        filedata = f.read()
    return filedata
