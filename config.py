import pathlib

support_archive_type = [
    'application/zip',
    'application/gzip',
    'application/x-xz',
    'application/x-bzip2',
]

support_image_type = [
    'png',
    'jpg',
]

images_min_num = 4

root = pathlib.Path('/tmp')