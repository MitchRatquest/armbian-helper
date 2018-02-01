#!/usr/bin/python
import subprocess, curses, curses.panel, os
from time import sleep
from menus import * #get all those stats
from functions import * #get all those functions
#################################################
#AVAILABLE BOARDS: opipc, opiz, opione, neo
board = opiz
############################################
COLUMNS=79 #default tty size - 1 
LINES=23

def initMainMenu(screen,board):
	setupScreen(screen)
	menuitems=getBoardMenu(board)		#return array of menu item strings
	currentMenuItem=menuitems[0]		#declare starting point
	highlightMenu(currentMenuItem,screen,board)
	try:
		mainMenu(screen, currentMenuItem, menuitems)
	except KeyboardInterrupt:
		curses.endwin()
		quit()

def gpioMenu(screen, board):
	initGpioMenu(screen,board)
	helpwin = initHelpMenu(screen)
	offset=4										#y offset for drawing on screen
	index=offset									#index for drawing operations
	pinNumbers=board[3]
	pinNames=board[2]
	while True:
		screen.timeout(20)
		pinStats(index-offset, screen, pinNumbers)	#upper left corner stats
		c = screen.getch()
		
		if c == curses.KEY_RIGHT:
			screen.hline(24,0," ",COLUMNS)			#clear status line
			index=index+1
			if index >= len(pinNumbers)+offset:		#out of bounds on bottom
				index=offset						#wrap selection
			for x in range(0,LINES):
				screen.chgat(x,0,curses.A_NORMAL)
			if index %2==1: #right side
				screen.chgat(index-(index/2)-1,41,COLUMNS/2,curses.A_STANDOUT)
			else:
				screen.chgat(index/2,15,25,curses.A_STANDOUT)
		if c == curses.KEY_LEFT:
			screen.hline(24,0," ",COLUMNS)			#clear status line
			if index < offset +1 :					#out of bounds on top 
				index= len(pinNumbers)+offset		#wrap selection to bottom right
			index = index-1
			for x in range(0,LINES):
				screen.chgat(x,0,curses.A_NORMAL)
			if index %2==1: #right side
				screen.chgat(index-(index/2)-1,41,COLUMNS/2,curses.A_STANDOUT)
			else:
				screen.chgat(index/2,15,25,curses.A_STANDOUT)
		if c == curses.KEY_UP:
			screen.hline(24,0," ",COLUMNS)			#clear status line
			index = index-2
			if index < offset: 						#out of bounds on the top
				index=len(pinNumbers)+offset-1		#wrap selection to bottom right
			for x in range(0,LINES):
				screen.chgat(x,0,curses.A_NORMAL)
			if index %2==1: #right side
				screen.chgat(index-(index/2)-1,41,COLUMNS/2,curses.A_STANDOUT)
			else:
				screen.chgat(index/2,15,25,curses.A_STANDOUT)
		if c == curses.KEY_DOWN:
			screen.hline(24,0," ",COLUMNS)			#clear status line
			index = index+2
			if index >=len(pinNumbers)+offset:		#out of bottom bounds
				index=offset						#wrap selection to top left
			for x in range(0,LINES):
				screen.chgat(x,0,curses.A_NORMAL)
			if index %2==1: #right side
				screen.chgat(index-(index/2)-1,41,COLUMNS/2,curses.A_STANDOUT)
			else:
				screen.chgat(index/2,15,25,curses.A_STANDOUT)
		if c == 98: #'b' key to quit
			clearScreen(screen)
			return
		if c == 115: # ord('s')
			initializePin(index-offset,screen,pinNumbers) #should be pinNumbers[index-offset],screen instead
		if c == 117: # 'u'
			uninitializePin(index-offset,screen,pinNumbers)
		if c == 114: # 'r'
			readPin(index-offset,screen,pinNumbers)
		if c == 105: # 'i'
			pinInput(index-offset,screen,pinNumbers)
		if c == 111: # 'o'
			pinOutput(index-offset,screen,pinNumbers)
		if c == 49: # '1'
			pinHigh(index-offset,screen,pinNumbers)
		if c == 48: # '0'
			pinLow(index-offset,screen,pinNumbers)
		if c == 104: # 'h'
			helpMenuShow(helpwin,gpioHelp)
		updateScreen(screen)

def mainMenu(screen, currentMenuItem, menuitems):
	while True:
		c = 0
		c = screen.getch()						#get a character

		if c == curses.KEY_RIGHT:
			try:
				currentMenuItem=menuitems[menuitems.index(currentMenuItem)+1]
			except:
				currentMenuItem=menuitems[0] #loop it
			changed=1
		if c == curses.KEY_LEFT:
			try:
				currentMenuItem=menuitems[menuitems.index(currentMenuItem)-1]
			except:
				currentMenuItem=menuitems[0] #loop it
			changed=1
		if c ==  32: #enter or spacebar for selection
			screen.addstr(10,20,"YOU HAVE SELECTED: %s" %currentMenuItem, curses.A_BOLD)
			if currentMenuItem=="GPIO":
				gpioMenu(screen,board)
				currentMenuItem=menuitems[0]
				#highlightMenu(currentMenuItem,screen,board)
			if currentMenuItem=="USB":
				#manually plug things into these ports and figure out their lsusb bus id
				#then tell the user what is plugged in and at what speed
				#same thing with USB2.0, but maybe use one of those cool cube things from asciio
				pass
			if currentMenuItem=="ETH0":
				#display ifconfig?
				#make sure its active with dmesg | grep
				#state speed
				#options like nmtui for setting up a static ip
				#dnsmasq configs?
				pass
			if currentMenuItem=="USBX2":
				#same as USB
				pass
			if currentMenuItem=="AUDIO":
				#alsamixer prompt (not sure how do swing that)
				#speaker-test
				#TV out does not work on mainline
				pass
			if currentMenuItem=="MIC":
				#arecord
				#simple visualizer? with alsa api?
				pass
			if currentMenuItem=="HDMI":
				#h3disp? does that work on mainline?
				#check /boot/boot.cmd to make sure sane settings
				# Recompile with:
				# mkimage -C none -A arm -T script -d /boot/boot.cmd /boot/boot.scr
				#check device tree
				#make sure dtc is installed
				#fancy string search sed -i stuff
				pass
			if currentMenuItem=="CSI":
				pass
			if currentMenuItem=="USBOTG":
				usbMenu(screen)
				screen.erase()
				updateScreen(screen)
				'''
				possible legacy drivers:
					g_ether
					g_serial
						warning that this already is set up
					g_mass_storage
						cdrom=y, for booting ISOs
					g_hid
					g_midi
				possible configfs stuff:
					literally anything
				options for dns server with g_ethernet
				options for iptables routing to use device as usb-ethernet dongle
				directions for possible network sharing setups on linux, windows, mac
				modify /etc/modules
				'''
		highlightMenu(currentMenuItem,screen,board)	#display selection
		updateScreen(screen)
		if c == 98: # b  key to quit
			curses.endwin()
			quit()


def usbMenu(screen):
	screen.erase()
	updateScreen(screen)
	currentGadget = "Current loaded gadget: "
	currentGadget += Bash("lsmod | grep -m1 g_ | awk '{print $1}'")[0] #current module loaded
	kernel = Bash("uname -r")[0]
	directory = "/lib/modules/" + kernel + "/kernel/drivers/usb/gadget/legacy"
	try:
		functionsSupported = Bash("ls "+directory)
		for x in range(len(functionsSupported)):
			functionsSupported[x] = functionsSupported[x].strip('.ko') #now its a nice list of gadgets
	except:
		functionsSupported = ["no usb gadget modules in your kernel"]
	title = "microUSB / USB OTG functions"
	screen.addstr(0,80/2-len(title)/2,title,curses.A_BOLD)
	screen.hline(1,0,'-',79)
	screen.addstr(2,80/2-len(currentGadget)/2,currentGadget,curses.A_BOLD)
	for x in range(len(functionsSupported)):
		screen.addstr(5+x,80/2-len(functionsSupported[x]),functionsSupported[x], curses.A_BOLD)
	
	#gadgetfs setup:
	try:
		Bash("modprobe libcomposite")
		Bash("mount -t configfs none /sys/kernel/config")#mount none cfg -t configfs?
		if findThis("ls /sys/kernel/config","usb_gadget") == 1:
			gadgetfs = "gadgetFS supported on this kernel"
	except:
		gadgetfs = "no gadgetFS support available"
	FUNCTIONS_USER_ENABLED=[]
	while True:
		c = screen.getch()
		if c == 98: # b key
			return
#setup -> go through list of gadgets -> finish
#https://www.kernel.org/doc/Documentation/usb/gadget_configfs.txt
#https://www.kernel.org/doc/Documentation/ABI/testing/configfs-usb-gadget-ecm
#https://www.kernel.org/doc/Documentation/ABI/testing/configfs-usb-gadget-acm
#https://www.kernel.org/doc/Documentation/ABI/testing/configfs-usb-gadget-mass-storage

#this is where i got the initial stuff from: 
#https://github.com/ckuethe/usbarmory/wiki/USB-Gadgets
#http://isticktoit.net/?p=1383

#https://www.kernel.org/doc/Documentation/ABI/testing/

#nice demo here: https://s3.amazonaws.com/connect.linaro.org/sfo15/Presentations/09-23-Wednesday/SFO15-311-%20ConfigFS%20Gadgets-%20An%20Introduction.pdf
def setupGadget(serial=8349982, manuf="testing", product="multigadget"):
	topdir = "/sys/kernel/config/usb_gadget"
	Bash("mkdir -p "+topdir+"/g1")
	Bash("echo 0x1d6b > "+topdir+"/g1/idVendor") # Linux Foundation
	Bash("echo 0x104 > "+topdir+"/g1/idProduct") # Multifunction Composite Gadget
	Bash("echo 0x0100 > "+topdir+"/g1/bcdDevice") # v1.0.0
	Bash("echo 0x0200 > "+topdir+"/g1/bcdUSB") # USB2
	
	Bash("mkdir -p "+topdir+"/g1/strings/0x409") #0x409 for english language strings
	Bash("echo "+str(serial)+" > "+topdir+"/g1/strings/0x409/serialnumber")
	Bash("echo "+str(manuf)+" > "+topdir+"/g1/strings/0x409/manufacturer")
	Bash("echo "+str(product)+" > "+topdir+"/g1/strings/0x409/product")

def gadgetSetupRNDIS():
	topdir = "/sys/kernel/config/usb_gadget/g1/"
	Bash("mkdir -p "+topdir+"functions/rndis.usb0")
	Bash("mkdir -p "+topdir+"configs/c.1")
	Bash("mkdir -p "+topdir+"configs/c.1/strings/0x409")
	Bash("echo 'Config 1: RNDIS network' > "+topdir+"configs/c.1/strings/0x409/configuration")
	Bash("echo 500 > "+topdir+"configs/c.1/MaxPower")
	Bash("ln -s "+topdir+"functions/rndis.usb0 "+topdir+"configs/c.1")
	#check for /etc/network/interfaces for a usb0 device and set that up according to user input
	#ex: static, dhcp, static but dnsmasq enabled, brctl, iptables for weird usb/ethernet dongle
	#static: address  netmask
	#dhcp: ifup usb0
	#static, but dnsmasq being served from 0.0.0.0
	#ifconfig usb0 0.0.0.0; ifconfig eth0 0.0.0.0; brctl addbr br0; brctl addif br0 eth0; brctl addif br0 usb0; ifup br0
	#iface br0 inet dhcp
	#	bridge_ports eth0 usb0
	#ifup br0

def finishGadget():
	topdir = "/sys/kernel/config/usb_gadget/g1/"
	Bash("echo 500 > "+topdir+"configs/c.1/MaxPower") # not until after right before attachment
	Bash("ls /sys/class/udc > "+topdir+"UDC") #finally attach functions to the hardware
	#if 'ethernet' in FUNCTIONS_USER_ENABLED:
		#ifup usb0

def disableGadget():
	Bash("echo '' > "+topdir+"UDC") #unlink 

if __name__ == '__main__':
	curses.wrapper(initMainMenu,board)
