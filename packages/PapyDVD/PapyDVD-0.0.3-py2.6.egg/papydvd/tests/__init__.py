# -*- coding: utf-8 -*-

import unittest
from repoze.bfg.configuration import Configurator
from repoze.bfg import testing

def _initTestingDB():
    from papydvd.models import initialize_sql
    session = initialize_sql('sqlite://')
    return session

class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()
        self.config.begin()
        _initTestingDB()

    def tearDown(self):
        self.config.end()

    def test_it(self):
        from papydvd.views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['root'].name, 'root')
        self.assertEqual(info['project'], 'PapyDVD')
