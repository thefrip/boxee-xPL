# What
the xbmc.xpl plugin will xpl enable xbmc. This plugin supports the media scheme, as well as
the osd and cid schemes. Read more about [xpl](http://xplproject.org.uk/). 

#Disclaimer
This is based on the [work](https://github.com/c99koder/boxee-xPL) of [Sam Steel](https://github.com/c99koder).
I have just made some minor modifications and made it fit with the new plugin
architecture of xbmc.   

#Installation
This is early versions for betatesters. I will try to submit this plugin to the main
xbmc repository when the software has been tested for a period. In the xbmc repository they
prefer to include only stable plugins, so for now there will be the install via zip option. 

1. Download latest version [here](https://github.com/fredrikaubert/boxee-xPL/downloads)
2. In xbmc: Settings -> Add-ons -> Install from zip file
3. Browse to where you stored the zipfile, and select it
4. Restart xbmc (known issue)
5. Voila, now xbmc should send xpl messages on the network, and respond to  


# License
[GNU General Public License](https://www.gnu.org/licenses/gpl-2.0.html). 
This is based on the work of Sam Steel which are licensed as GNU, hence GPL is the only 
option. Xbmc itself is also GPL, so it kind of makes sense. 











About
=====
Boxee-xPL is a script that allows Boxee or XBMC to interface with home automation software such as misterhouse over the xPL protocol.
Current supported commands are play, stop, skip, and pause.  Media information is broadcast whenever a new song or video starts.

Installation
============
Copy boxee-xPL.py into your XBMC scripts folder:

Boxee on linux: ~/.boxee/UserData/scripts
Boxee on Mac OS X: ~/Library/Application Support/BOXEE/UserData/scripts

Create a new file named "autoexec.py" in the scripts folder, and paste in the following two lines:

import xbmc
xbmc.executescript('special://masterprofile/scripts/boxee-xPL.py')

Usage
=====
Boxee will register itself on the network and respond to requests according to the MEDIA.BASIC schema.
A sample script is included for connecting Boxee to misterhouse. Copy the files in the misterhouse/ folder
into your misterhouse code/ folder, and edit boxee.pl to set the hostname of the computer running Boxee.
