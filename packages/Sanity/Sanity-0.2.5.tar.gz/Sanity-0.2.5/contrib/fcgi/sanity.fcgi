#!/usr/bin/python
from flup.server.fcgi import WSGIServer
from sanity import app

WSGIServer(app, bindAddress=('127.0.0.1', 9005)).run()
