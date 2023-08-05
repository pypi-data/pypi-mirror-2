# -*- coding: utf-8 -*-
import os
from pyaler import app
from bottle import request, send_file

@app.route('/')
def index():
    image = request.environ['pyaler.app_config']['image']
    return '''<html><head>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.js"></script>
    <script type="text/javascript" src="/static/demo.js"></script>
    </head><body><img src="/static/%(image)s" /><div id="control"></div></body></html>''' % locals()

@app.route('/static/:filename')
def static_file(filename):
    if filename.endswith('.js'):
        send_file(os.path.basename(filename), root=os.path.dirname(__file__))
    else:
        image = request.environ['pyaler.app_config']['image']
        send_file(os.path.basename(image), root=os.path.dirname(image))

