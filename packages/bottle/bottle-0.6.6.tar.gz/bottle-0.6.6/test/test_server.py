# -*- coding: utf-8 -*-
import unittest
import bottle
import urllib2
import time
from tools import tob
import sys
import os
import signal
from subprocess import Popen, PIPE

class TestServer(unittest.TestCase):
    server = 'WSGIRefServer'
    port = 12643

    def setUp(self):
        return
        cmd = [sys.executable, 'servertest.py', self.server, str(self.port)]
        self.p = Popen(cmd, stdout=PIPE)
        time.sleep(1)

    def tearDown(self):
        return
        time.sleep(1)
        os.kill(self.p.pid, signal.SIGINT)
        time.sleep(1)
        while self.p.poll() is None:
            os.kill(self.p.pid, signal.SIGTERM)

    def fetch(self, url):
        try:
            return urllib2.urlopen('http://localhost:%d/%s' % (self.port, url)).read()
        except Exception, e:
            return repr(e)

    def test_test(self):
        return    
        self.assertEqual(tob('OK'), self.fetch('test'))

class TestCherryPyServer(TestServer):
    server = 'CherryPyServer'

class TestPasteServer(TestServer):
    server = 'PasteServer'

class TestTornadoServer(TestServer):
    server = 'TornadoServer'

class TestTwistedServer(TestServer):
    server = 'TwistedServer'

class TestDieselServer(TestServer):
    server = 'DieselServer'

class TestGunicornServer(TestServer):
    server = 'GunicornServer'

class TestEventletServer(TestServer):
    server = 'EventletServer'

if __name__ == '__main__':
    unittest.main()
