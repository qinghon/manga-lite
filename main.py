import time
import argparse
import datetime
import threading
import time
from urllib.parse import unquote

import filetype
from flask import Flask, make_response, abort
from flask import render_template

import config
from scan import scan_file_dirs, filter_file_dirs

app = Flask(__name__)
files = {}
files_list = []


@app.route('/')
def index():
    return render_template('index.html', files=files_list)


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


def scan_loop():
    global files
    global files_list
    while True:
        pl = scan_file_dirs(config.root)
        s = filter_file_dirs(pl)
        files = s
        files_list = [f for uid, f in s.items()]
        files_list.sort(key=lambda m: m.ctime, reverse=True)
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "scan over, found ", len(files))
        time.sleep(60 * 60 * 24)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--root', default='/tmp', type=str)
    p.add_argument('--port', default=1324, type=int)
    p.add_argument('--host', default='0.0.0.0', type=str)
    arg = p.parse_args()
    config.root = arg.root

    l = threading.Thread(target=scan_loop)
    l.start()

    app.run(host=arg.host, port=arg.port)
