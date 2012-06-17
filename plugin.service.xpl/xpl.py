import sys, string, select, threading, os.path, time
from socket import *
import xbmc
from threading import Thread  


#class XplMessage() :
#    
#    def __init__(self, type, schema):
#        self.type = type
#        self.schema = schema
#        self.source =""
#        self.target = "*"
#        self.properties = {}
    
       

class Xpl() : 
    def __init__(self, source, ip):
        self.source = source
        self.ip = ip
        self.port = 3865
        self.buff = 1500
        self._stop = False
        addr = ("0.0.0.0",self.port)
        
        
        self.udpSocket = socket(AF_INET,SOCK_DGRAM)
        # Try and bind to the base port
        try :
            self.udpSocket.bind(addr)
            print("Binding to 3865")
        except :
            # A hub is running, so bind to a high port
            self.port = 50000
            foundPort = False
            while( not foundPort ):
                print("Binding to 50000")
                addr = ("127.0.0.1",self.port)
                try :
                    self.udpSocket.bind(addr)
                    foundPort = True
                except :
                    self.port += 1
        self.heartBeat()
        xbmc.log("FA:Heartbeat sent")
        t = Thread(target=self.listenForPackets)
        xbmc.log("Created listen Thread")
        t.start()
        print( "Main thread returns")
        
        
        
    def listenForPackets(self):
        xbmc.log( "FA:Listening in for packets and stuff" )
        time.sleep(2)
        try: 
            while( self._stop != True) :
                xbmc.log( "FA:waiting")
                readable, writeable, errored = select.select([self.udpSocket],[],[],60)
                if len(readable) == 1 :
                    xbmc.log("FA: Got data! Wee!")
                    data,addr = self.udpSocket.recvfrom(self.buff)
                    xbmc.log( "FA:calling parse" )
                    self.parse(data)
        except(SystemExit): 
            self.stop()
            
            
    
    def parse(self, data):
        xbmc.log( data )
    
    def heartBeat(self):
        xbmc.log( "Sending heartbeat" )
        self.sendBroadcast("xpl-stat", "*","hbeat.app", "interval=1\nport=" + str(self.port) + "\nremote-ip=" + self.ip)
        self.heartbeat_timer = threading.Timer(60, self.heartBeat)
        self.heartbeat_timer.start()

    
    def sendBroadcast(self, type, target, schema, body) :
        hbSock = socket(AF_INET,SOCK_DGRAM)
        hbSock.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
        msg = "xpl-stat\n{\nhop=1\nsource=" + self.source + "\ntarget="+target+"\n}\n"+schema+"\n{\n"+ body + "\n}\n"
        hbSock.sendto(msg,("255.255.255.255",3865))
        
    def stop(self):
        xbmc.log("FA:Stopping xpl")
        self.heartbeat_timer.cancel()
        self._stop = True
        self.sendBroadcast("xpl-stat", "*","hbeat.end", "")
        self.udpSocket.close()
