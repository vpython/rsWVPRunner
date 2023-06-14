# -*- coding: utf-8 -*-

import flask

from . import app

import os


@app.route('/css/<path:filename>')
def css_static(filename):
    return flask.send_from_directory('../css', filename)


@app.route('/lib/<path:filename>')
def lib_static(filename):
    cache_timeout = None
    return flask.send_from_directory('../lib', filename, max_age=cache_timeout)


@app.route('/package/<path:filename>')
def package_static(filename):
    return flask.send_from_directory('../package', filename)


@app.route(r'/favicon.ico')
def favicon_static():
    return flask.send_from_directory('../static/images', r'favicon.ico')


@app.route('/untrusted/run.html')
def run():
    return flask.render_template("run.html", trusted_host=os.environ.get('TRUSTED_HOST', 'localhost:5173'))


@app.route('/untrusted/<path:filename>')
def untrusted_static(filename):
    return flask.send_from_directory('../untrusted', filename)


@app.route('/')
@app.route('/index')
def root():
    return "This is a runner. Not a web page."
