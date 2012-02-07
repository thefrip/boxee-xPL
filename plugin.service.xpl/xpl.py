import sys, string, select, threading, os.path
from socket import *



class Xpl() :
    
    def __init__(self, source, ip):
        self.source = source
        self.ip = ip
        self.port = 3865
        self.buff = 1500
        addr = ("0.0.0.0",self.port)
        # Try and bind to the base port
        try :
            socket.UDPSock.bind(addr)
            print("Binding to 3865")
        except :
            # A hub is running, so bind to a high port
            self.port = 50000
            print("Binding to 50000")
            addr = ("127.0.0.1",self.port)
            try :
                socket.UDPSock.bind(addr)
            except :
                self.port += 1
                
        self.heartBeat()
    
    def heartBeat(self):
        print("Sending heartbeat")
        self.sendBroadcast("xpl-stat", "*","hbeat.app", "interval=1\nport=" + str(self.port) + "\nremote-ip=" + self.ip)
        self.heartbeat_timer = threading.Timer(60, self.heartBeat)
        self.heartbeat_timer.start()

    
    def sendBroadcast(self, type, target, schema, body) :
        hbSock = socket(AF_INET,SOCK_DGRAM)
        hbSock.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
        msg = "xpl-stat\n{\nhop=1\nsource=" + self.source + "\ntarget="+target+"\n}\n"+schema+"\n{\n"+ body + "\n}\n"
        hbSock.sendto(msg,("255.255.255.255",3865))
