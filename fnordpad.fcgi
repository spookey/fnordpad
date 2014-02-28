#!/usr/bin/env python2
from werkzeug.contrib.fixers import LighttpdCGIRootFix
from flup.server.fcgi import WSGIServer
from app import app

if __name__ == '__main__':
    app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app, app_root='/')
    WSGIServer(app).run()

