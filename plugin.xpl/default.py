################################################################################
#
# xPL interface for Boxee
#
# Version 1.0
#
# Copyright (C) 2010 by Sam Steele
# http://www.c99.org/
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# Linking this library statically or dynamically with other modules is
# making a combined work based on this library. Thus, the terms and
# conditions of the GNU General Public License cover the whole
# combination.
# As a special exception, the copyright holders of this library give you
# permission to link this library with independent modules to produce an
# executable, regardless of the license terms of these independent
# modules, and to copy and distribute the resulting executable under
# terms of your choice, provided that you also meet, for each linked
# independent module, the terms and conditions of the license of that
# module. An independent module is a module which is not derived from
# or based on this library. If you modify this library, you may extend
# this exception to your version of the library, but you are not
# obligated to do so. If you do not wish to do so, delete this
# exception statement from your version.
#
################################################################################
import sys, string, select, threading, os.path
import xbmc
from socket import *
from xpl import *



class XplPlayer( xbmc.Player ) :
# xPL source name

	source = "parasit-xbmc." + gethostname().replace("-", "").split(".")[0][:16].lower()
	xpl = Xpl(source, xbmc.getIPAddress())
	lastState = ""
	lastKind = ""
	lastAudioTag = None
	lastVideoTag = None
	
	def __init__ ( self ):
		xbmc.Player.__init__( self )
		self.xpl.parse = self.parseBroadcast
		
		
	def onStartUp(self):
		self.monitorXbmc("startup")

	def onShutdown(self):
		self.monitorXbmc("shutdown")

	def onPlayBackStarted(self):
		self.monitorXbmc("play")

	def onPlayBackEnded(self):
		self.monitorXbmc("stop")
		
	def onPlayBackStopped(self):
		self.monitorXbmc("stop")

	def onPlayBackPaused(self):
		self.monitorXbmc("pause")
		
	def onPlayBackResumed(self):
		self.monitorXbmc("play")
	

	def parseBroadcast(self, data):
		# xbmc.log("FA, data:" + data)
		parts = data.split("\n")
		msgtype = parts[0].lower()
		offset = 2
		values = dict()
		if parts[offset-1] == "{":
			while parts[offset] != "}":
				part = parts[offset]
				if part != "}":
					value=part.split("=")
					if len(value) == 2:
						values[value[0].lower()]=value[1]
					offset = offset + 1
				else:
					break
		offset = offset + 1
		schema = parts[offset].lower()
		offset = offset + 2
		if parts[offset-1] == "{":
			while parts[offset] != "}":
				part = parts[offset]
				if part != "}":
					value=part.split("=")
					if len(value) == 2:
						values[value[0].lower()]=value[1]
					offset = offset + 1
				else:
					break
		
		
		
		if (values['target'] != "*" and values['target'] != "parasit-xbmc.*" and values['target'] != self.source) or values['source'] == self.source:
			return
	
		if msgtype == "xpl-cmnd":
			
			if schema =="osd.basic":
				if( values['command'].lower() == "write" or values['command'].lower() == "clear"):
					if( values['text'] ):
						displayTime = values.get('delay', "20")
						self.osdMessage("xPL Message", values['text'].replace("\\n", "\n"), displayTime, "")
			
			if schema =="cid.basic" or schema =="cid.netcall" or schema =="cid.meteor" :
				if( values['calltype'].lower() == "inbound"):
					cln = values['cln']
					if( len(cln) == 0 ):
						cln = "Incoming\x201A call"
					self.osdMessage(cln, values['phone'], 20, "phone")	
			
			
			if schema == "media.basic":
				print "Got media command:" + values['command']
				if values['command'].lower() == "stop":
					xbmc.executebuiltin('PlayerControl(Stop)')
				if values['command'].lower() == "play":
					xbmc.executebuiltin('PlayerControl(Play)')
				if values['command'].lower() == "pause":
					if xbmc.Player().isPlaying():
						xbmc.executebuiltin('PlayerControl(Play)')
				if values['command'].lower() == "skip":
					xbmc.executebuiltin('PlayerControl(Next)')
					
			if schema == "media.request":
				if values['request'].lower() == "devinfo":
					self.xpl.sendBroadcast("xpl-stat", values['source'],"media.devinfo", "name=Boxee xPL Interface\nversion=1.0\nauthor=Sam Steele\ninfo-url=http://www.c99.org/\nmp-list=boxee\n")
				
				if values['request'].lower() == "devstate":
					self.xpl.sendBroadcast("xpl-stat", values['source'],"media.devstate", "power=on\nconnected=true\n")
	
				if values['request'].lower() == "mpinfo":
					self.xpl.sendBroadcast("xpl-stat", values['source'],"media.mpinfo", "mp=xbmc\nname=Boxee\ncommand-list=play,stop,pause,skip\naudio=true\nvideo=true\n")
	
				if values['request'].lower() == "mptrnspt":
					self.xpl.sendBroadcast("xpl-stat", values['source'],"media.mptrnspt", "mp=xbmc\ncommand="+self.lastState+"\n")
	
				if values['request'].lower() == "mpmedia":
					media = "mp=xbmc\n"
					if xbmc.Player().isPlaying():
						if xbmc.Player().isPlayingAudio():
							tag = xbmc.Player().getMusicInfoTag();
							media = "mp=xbmc\n"
							media = media + "kind=audio\n"
							media = media + "title=" + tag.getTitle() + "\n"
							media = media + "album=" + tag.getAlbum() + "\n"
							media = media + "artist=" + tag.getArtist() + "\n"
							media = media + "duration=" + str(xbmc.Player().getTotalTime()) + "\n"
							media = media + "format=" + os.path.splitext(xbmc.Player().getPlayingFile())[1][1:] + "\n"
						else:
							tag = xbmc.Player().getVideoInfoTag();
							media = "mp=xbmc\n"
							media = media + "kind=video\n"
							media = media + "title=" + tag.getTitle() + "\n"
							media = media + "album=" + "\n"
							media = media + "artist=" + "\n"
							media = media + "duration=" + str(xbmc.Player().getTotalTime()) + "\n"
							media = media + "format=" + os.path.splitext(xbmc.Player().getPlayingFile())[1][1:] + "\n"
							
					self.xpl.sendBroadcast("xpl-stat", values['source'],"media.mpmedia", media)


	def monitorXbmc(self, status):
		kind = self.lastKind
		if xbmc.Player().isPlaying():
			try: 
				if xbmc.Player().isPlayingAudio():
					kind = "audio"
					if kind != self.lastKind:
						self.lastState = "stop"
						
						self.xpl.sendBroadcast("xpl-trig", "*","media.mptrnspt", "mp=xbmc\ncommand=stop\nkind=" + self.lastKind)
				
					tag = xbmc.Player().getMusicInfoTag();
					if self.lastAudioTag is None or self.lastAudioTag.getTitle() != tag.getTitle() or self.lastAudioTag.getArtist() != tag.getArtist() or self.lastAudioTag.getAlbum() != tag.getAlbum():
						media = "mp=xbmc\n"
						media = media + "kind=audio\n"
						media = media + "title=" + tag.getTitle() + "\n"
						media = media + "album=" + tag.getAlbum() + "\n"
						media = media + "artist=" + tag.getArtist() + "\n"
						media = media + "duration=" + str(xbmc.Player().getTotalTime()) + "\n"
						media = media + "format=" + os.path.splitext(xbmc.Player().getPlayingFile())[1][1:] + "\n"
						media = media + "state=" + status + "\n"
						self.xpl.sendBroadcast("xpl-trig", "*","media.mpmedia", media)
						self.lastAudioTag = tag
				if xbmc.Player().isPlayingVideo():
					kind = "video"
					if kind != self.lastKind:
						self.lastState = "stop"
						self.xpl.sendBroadcast("xpl-trig", "*","media.mptrnspt", "mp=xbmc\ncommand=stop\nkind=" + self.lastKind)
				
					tag = xbmc.Player().getVideoInfoTag();
					if self.lastVideoTag is None or self.lastVideoTag.getTitle() != tag.getTitle():
						#media = media + "state=" + status + "\n"
						media = "mp=xbmc\n"
						media = media + "kind=video\n"
						media = media + "title=" + tag.getTitle() + "\n"
						media = media + "album=" + "\n"
						media = media + "artist=" + "\n"
						media = media + "duration=" + str(xbmc.Player().getTotalTime()) + "\n"
						media = media + "format=" + os.path.splitext(xbmc.Player().getPlayingFile())[1][1:] + "\n"
						media = media + "state=" + status + "\n"
						self.xpl.sendBroadcast("xpl-trig", "*","media.mpmedia", media)
						self.lastVideoTag = tag
			except: 
				media = "mp=xbmc\n"
				media = media + "kind=unknown\n"
				media = media + "title=Exception, should be playing video but none gotten\n"
	 			media = media + "album=\n"
			  	media = media + "artist=\n"
	  			media = media + "duration=00:00\n"
	 			media = media + "format=" + os.path.splitext(xbmc.Player().getPlayingFile())[1][1:] + "\n"
	 			media = media + "state=" + status + "\n"
	 			self.xpl.sendBroadcast("xpl-trig", "*","media.mpmedia", media)
	
		else:
			lastAudioTag = None
			lastVideoTag = None
				
		if status != self.lastState: 
			self.xpl.sendBroadcast("xpl-trig", "*","media.mptrnspt", "mp=xbmc\ncommand="+status+"\nkind=" + kind)
		self.lastState = status
		self.lastKind = kind
		#	dialog = xbmcgui.Dialog()
		#	dialog.ok('Status', 'Status: %s' % (state))


	def osdMessage(self, title, message, displayTimeSeconds, icon):
		#todo: messages containing , or . will screw stuff up. Must find a way to fix
		executeString = "Notification(%s,%s,%s,%s)" % ( title, message ,str(displayTimeSeconds) + "000", icon )
		
		xbmc.executebuiltin(executeString)
		
	def destroy(self):
		self.xpl.stop()
		
player=XplPlayer()
player.onStartUp()

while (not xbmc.abortRequested):
	xbmc.sleep(1000)

player.onShutdown()
xbmc.log("xpl: Destruction requested. Stopping plugin") 
player.destroy()
