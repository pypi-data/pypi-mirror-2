# -*- coding: utf-8 -*-
import os
import pyaler
from webtest import TestApp
import unittest

config = os.path.join(os.path.dirname(pyaler.__file__), 'tests.yaml')

class TestPyaler(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(pyaler.make_app({}, config=config))

    def test_reset(self):
        resp = self.app.get('/arduinos/reset')
        resp.mustcontain('OK')

class TestPyalerExtension(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(pyaler.make_app({}, config=config, app='test_app'))

    def test_index(self):
        resp = self.app.get('/')
        resp.mustcontain('<title>')

