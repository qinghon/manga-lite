import dataclasses
from pathlib import Path
from image import *


@dataclasses.dataclass
class Manga():
    _p: Path = None
    _file_list: list[str] = None
    is_dir = False
    _compress_type = ''

    def __init__(self, p, file_list, is_dir=False, compress_type=''):
        self._p = p
        self._file_list = file_list
        self._file_list.sort()
        self.is_dir = is_dir
        self._compress_type = compress_type

    def get_file(self, file) -> bytes:
        if self._compress_type == 'application/zip':
            return get_zip_file(self._p, file)
        elif self.is_dir:
            return get_dir_file(self._p, file)

    def file_list(self):
        return self._file_list
