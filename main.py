import io
from pathlib import Path
import filetype
import flask
from urllib.parse import unquote

from flask import render_template
from flask import Flask, make_response, send_file, abort

import config
from image import get_zip_file
from scan import scan_file_dirs, filter_file_dirs
import argparse

app = Flask(__name__)
files = {}


@app.route('/')
def index():
    return render_template('index.html', files=files)


@app.route('/manga/<uid>')
def manga(uid):
    uid = unquote(uid)
    # print(uid, uid in files, type(uid), files.keys())

    if uid in files:
        return render_template('manga.html', file=uid, images=files[uid].file_list())
    else:
        abort(404)


@app.route('/image/<uid>/<image>')
def image(uid, image):
    if not uid in files:
        abort(404)
    m = files[uid]
    image_binary = m.get_file(image)
    if image_binary is None:
        abort(500)

    resp = make_response(image_binary)
    k = filetype.guess(image_binary)
    if k:
        resp.headers.set('Content-Type', k.mime)
    resp.headers.set('cache-control', 'max-age=31536000')
    return resp


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--root', default='/tmp', type=str)
    p.add_argument('--port', default=1324, type=int)
    p.add_argument('--host', default='0.0.0.0', type=str)
    arg = p.parse_args()
    config.root = arg.root
    s = scan_file_dirs(arg.root)
    s = filter_file_dirs(s)
    files = s

    app.run(host=arg.host, port=arg.port)
