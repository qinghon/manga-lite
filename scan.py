import dataclasses
import os
from pathlib import Path
import zipfile
import filetype
from pprint import pprint

import config
from config import support_archive_type, support_image_type, images_min_num
from manga import Manga


def scan_file_dirs(p: Path) -> list[Path]:
    archives = []

    for root, dirs, files in os.walk(p):
        for f in files:
            _f = Path(root) / Path(f)
            if not _f.is_file():
                continue
            try:
                k = filetype.guess(_f)
            except OSError as e:
                print(e)
                continue
            if not k:
                continue
            # print(f, k.mime)
            if k.mime in support_archive_type:
                archives.append(Path(f))
                continue
            if str(k.mime).startswith('image/'):
                archives.append(Path(os.path.relpath(Path(root), config.root)))
    archives = list(set(archives))
    return archives


def zip_get_filelist(p: Path) -> (bool, list[str]):
    if not zipfile.is_zipfile(p):
        return False, []

    with zipfile.ZipFile(p, 'r') as z:
        file_list = z.namelist()
        return True, file_list


FILE_TYPE_IMPL = {
    'application/zip': zip_get_filelist
}


def filter_file_dirs(ps: list[Path]):
    def filter_file(p: Path) -> (bool, list[str], str):
        k = filetype.guess(p)
        if k.mime in FILE_TYPE_IMPL.keys():
            ok, file_list = FILE_TYPE_IMPL[k.mime](p)
            image_cnt = 0
            for f in file_list:
                extension = os.path.splitext(f)[-1]
                if extension:
                    extension = extension[1:]
                if extension in support_image_type:
                    image_cnt += 1
                    if image_cnt >= images_min_num:
                        return True, file_list, k.mime

            if image_cnt < images_min_num:
                return False, file_list, k.mime
        else:
            return False, [], k.mime

    def filter_dir(p: Path) -> (bool, list):
        image_cnt = 0
        file_list = []
        for root, dirs, files in os.walk(p):
            for f in files:
                # f = Path(root) / Path(f)
                k = filetype.guess(Path(root) / Path(f))
                if k.extension in support_image_type:
                    image_cnt += 1
                    file_list.append(Path(f))
        if image_cnt > images_min_num:
            return True, file_list
        else:
            return False, file_list

    archives = {}

    for p in ps:
        ok = False
        file_list = None
        abs_p = config.root / p
        is_dir = False
        mime = ''
        if abs_p.is_file():
            ok, file_list, mime = filter_file(abs_p)
        elif abs_p.is_dir():
            ok, file_list = filter_dir(abs_p)
            is_dir = True
        if not ok:
            continue
        stat = os.stat(abs_p)
        archives[str(p)] = Manga(p, file_list, is_dir, mime, stat.st_ctime)
    return archives


if __name__ == '__main__':
    s = scan_file_dirs(Path(config.root))
    s = filter_file_dirs(s)
    pprint(s)
