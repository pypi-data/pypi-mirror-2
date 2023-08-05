# -*- coding: utf-8 -*-
from pyaler import app

@app.route('/')
def index():
    return '<html><title>live</title></html>'
