import unittest
from xpl import *

class TestXpl(unittest.TestCase):
    
    def setUp(self):
        self.unit = Xpl("parasit-xbmc.unittest", "192.168.0.135")

    def test_sendXplMessage(self):
        print "testMethod"
        self.unit.sendBroadcast("xpl-stat", "*", "media.mptrnspt", "mp=xbmc")
        time.sleep(10)
        self.unit.stop()
        