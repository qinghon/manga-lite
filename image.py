import tarfile
import zipfile
from pathlib import Path
from functools import lru_cache
import config


@lru_cache()
def get_zip_fd(p: Path) -> zipfile.ZipFile:
    z = zipfile.ZipFile(p, 'r')
    return z


def get_zip_file(p: Path, file) -> bytes:
    p = Path(p)
    if not p.is_absolute():
        p = config.root / p
    z = get_zip_fd(p)
    filedata = None
    with z.open(file) as f:
        filedata = f.read()
    return filedata


@lru_cache()
def get_tar_fd(p: Path) -> tarfile.TarFile:
    z = tarfile.open(p, 'r')
    return z


def get_tar_file(p: Path, file) -> bytes:
    p = Path(p)
    if not p.is_absolute():
        p = config.root / p
    tf = get_tar_fd(p)
    filedata = None
    file_info = tf.getmember(file)
    with tf.extractfile(file_info) as f:
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
