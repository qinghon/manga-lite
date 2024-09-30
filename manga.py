import dataclasses
from pathlib import Path
from image import *


@dataclasses.dataclass
class Manga:
    _p: Path = None
    _file_list: list[str] = None
    is_dir = False
    _compress_type = ''
    _ctime = 0

    def __init__(self, p, file_list, is_dir=False, compress_type='', ctime=0):
        self._p = p
        self._file_list = file_list
        self._file_list.sort()
        self.is_dir = is_dir
        self._compress_type = compress_type
        self._ctime = ctime

    def get_file(self, file) -> bytes:
        if self._compress_type == 'application/zip':
            return get_zip_file(self._p, file)
        if self._compress_type == 'application/tar':
            return get_tar_file(self._p, file)
        elif self.is_dir:
            return get_dir_file(self._p, file)

    @property
    def get_cover_name(self) -> str:
        for x in self._file_list:
            if x.__class__ == str and "cover" in x:
                return x
        return self._file_list[0]

    def get_cover(self) -> bytes:
        return self.get_file(self.get_cover_name)

    def file_list(self):
        return self._file_list

    @property
    def filename(self):
        return str(self._p)
    @property
    def ctime(self):
        return self._ctime
