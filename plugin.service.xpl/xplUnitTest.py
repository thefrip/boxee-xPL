import unittest
from xpl import *

class TestXpl(unittest.TestCase):
    
    def setUp(self):
        addr = ("0.0.0.0",self.port)
        # Try and bind to the base port
        try :
            socket.UDPSock.bind(addr)
            print("Binding to 3865")
        finally:
            print("at last")
        self.unit = Xpl("parasit-xbmc.unittest", "127.0.0.1")

    def test_sendXplMessage(self):
        print "testMethod"
        self.unit.sendBroadcast("xpl-stat", "*", "media.mptrnspt", "mp=xbmc")
        
