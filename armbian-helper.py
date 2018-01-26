#!/usr/bin/python
import subprocess, curses, curses.panel, os
from time import sleep
from menus import * #get all those stats
#################################################
#AVAILABLE BOARDS: opipc, opiz, opione, neo
board = opiz
############################################
COLUMNS=79 #default tty size - 1 
LINES=24

def make_panel(h,l, y,x):
	win = curses.newwin(h,l, y,x)
	win.erase()
	win.box()
	panel = curses.panel.new_panel(win)
	return win, panel

def test(stdscr,board):
	setupScreen(stdscr)
	menuitems=getBoardMenu(board)		#return array of menu item strings
	currentMenuItem=menuitems[0]		#declare starting point
	highlightMenu(currentMenuItem,stdscr,board)
	try:
		mainMenu(stdscr, currentMenuItem, menuitems)
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
	#	pin = pinNumbers[index - offset]			#real pin being referenced
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

def initializePin(index,screen,pinNumbers):
	screen.hline(24,0," ",COLUMNS) #clear line completely
	if pinNumbers[index] == -1:
		response = "cannot init this pin"
	elif createPinsysfs(pinNumbers[index]) == 0:
		response = "successfully initialized pin " + str((index)+1)
	screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)

def uninitializePin(index,screen,pinNumbers):
	response=''
	screen.hline(24,0," ",COLUMNS) #clear line completely
	if pinNumbers[index] == -1:
		response = "cannot uninit this pin"
	elif removePinsysfs(pinNumbers[index]) == 0:
		response = "successfully uninitialized pin " + str((index)+1)
	elif removePinsysfs(pinNumbers[index]) == -1:
		response = "pin wasn't initialized"
	screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)

def readPin(index,screen,pinNumbers):
	screen.hline(24,0," ",COLUMNS) #clear line completely
	if pinNumbers[index] == -1:
		response = "This pin's state is not able to be changed"
		pass
	else:
		screen.hline(24,0," ",COLUMNS)
		value = readPinsysfs(pinNumbers[index])
		if value is None:
			response = "This pin is not initialized"
		else:
			response = "Pin "+str(index+1)+"'s value is "+str(value)
	screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)

def pinInput(index, screen, pinNumbers):
	screen.hline(24,0," ",COLUMNS) #clear line completely
	if pinNumbers[index] == -1:
		response = "This pin's state is not able to be changed"
		pass
	else:
		value = directionPinsysfs(pinNumbers[index],'in')
		if value == 0:
			response = "Pin "+str(index+1)+" is an input pin and can sink up to 10 milliamps"
		if value == -1:
			response = "Pin is already set to input"
	screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)

def pinOutput(index, screen, pinNumbers):
	screen.hline(24,0," ",COLUMNS) #clear line completely
	if pinNumbers[index] == -1:
		response = "This pin's state is not able to be changed"
		screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)
		pass
	else:
		value = directionPinsysfs(pinNumbers[index],'out')
		if value == 0:
			response = "Pin "+str(index)+" is an output pin and can source up to 10 milliamps"
		if value == -1:
			response = "Pin is already set to output"
		screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)

def pinHigh(index,screen,pinNumbers):
	screen.hline(24,0," ",COLUMNS) #clear line completely
	response=''
	if pinNumbers[index] == -1:
		response = "This pin's state is not able to be changed"
	elif os.path.isdir('/sys/class/gpio/gpio'+str(orangepiPCPins[(index-3)*2-1])) == False: #not configured
		createPinsysfs(pinNumbers[index])
	elif readSysfs(pinNumbers[index], 'direction') == 'in':
		response = "This pin is an input and cannot be set to 1 (3.3 volts)"
		screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)
	else:
		
		value = valuePinsysfs(pinNumbers[index],'On')
		if value == 0:
			response = "Pin "+str(index)+"'s value is set to 1 (3.3 volts)"
		if value == -1:
			response = "Pin's value is already at 1"
	screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)

def pinLow(index,screen,pinNumbers):
	screen.hline(24,0," ",COLUMNS) #clear line completely
	if pinNumbers[index] == -1:
		response = "This pin's state is not able to be changed"
	elif os.path.isdir('/sys/class/gpio/gpio'+str(pinNumbers[index])) == False: #not configured
		createPinsysfs(pinNumbers[index])
		response = 'pin not configured'
	elif readSysfs(pinNumbers[index],'direction').strip('\n')=='in':
		response = "This is set to input and cannot be pulled low"
	else:
		value = valuePinsysfs(pinNumbers[index],0)
		if value == 0:
			response = "Pin "+str(index)+"'s value is set to 0 (ground)"
		if value == -1:
			response = "Pin's value is already at 0"
	screen.addstr(24,80/2-len(response)/2,response,curses.A_STANDOUT)

def initGpioMenu(screen,board,index=4):
	screen.erase()
	updateScreen(screen)
	warning="White arrow on board always points to pin 1"
	screen.addstr(0,COLUMNS/2-len(warning)/2,warning,curses.A_BOLD)
	pinNumbers=board[3]
	pinNames=board[2]
	offset=1
	for x in range(0,len(pinNumbers)+1): #create pin numbers
		if x % 2==1: 				#right side
			screen.addstr((x+offset-(x/2)), (COLUMNS/2-1), str(x), curses.A_BOLD)			 #put even numbers on right side 
			screen.addstr((x+offset-(x/2)), (COLUMNS/2-4)-len(pinNames[x]), pinNames[x])	 #names on right side at the right offset
		else:
			screen.addstr((x+offset-(x/2)), (COLUMNS/2+2), str(x), curses.A_BOLD) 			#put odd numbers on left side
			screen.addstr((x+offset-(x/2)), (COLUMNS/2+7), pinNames[x])						#names on left side
	#now draw a box
	screen.addstr(offset,36,'.-------.') 							#top bar
	screen.addstr(offset+len(pinNumbers)/2+1,36,"'-------'")		#bottom bar
	screen.vline(offset+1,36,'|',len(pinNumbers)/2)					#left side
	screen.vline(offset+1,44,'|',len(pinNumbers)/2)					#right side
	helpstring = "press h for help"
	screen.addstr(offset+len(pinNumbers)/2+2,(COLUMNS/2)-(len(helpstring))/2,helpstring,curses.A_BOLD)
	index=4											#place on screen to draw
	screen.chgat(index/2,15,25,curses.A_STANDOUT)	#first pin
	updateScreen(screen)

def initHelpMenu(screen):
	helpwin=make_panel(LINES,COLUMNS,0,0)
	helpwin[1].hide()
	helpindex=0
	return helpwin

def helpMenuShow(windowpanel,string):
	windowpanel[1].show()
	windowpanel[0].refresh()
	windowpanel[0].timeout(500)
	index = 0
	helpMenuUpdate(windowpanel,string,index)
	while True:
		c = windowpanel[0].getch()
		if c == 98: # b key
			windowpanel[1].hide()
			return
		if c == 66: #arrow down
			index = index + 1
			index = helpMenuUpdate(windowpanel,string,index)
			if index > len(string)-LINES-1:
				index = index -1
		if c == 65: #arrow up
			index = index - 1
			index = helpMenuUpdate(windowpanel,string,index)
			if index <= 0:
				index = index + 1
		updateScreen(windowpanel[0])

def helpMenuUpdate(windowpanel,gpio,index):
	for x in range(LINES-3): #clear window without erasing border
		windowpanel[0].addstr(1+x,2,'                                                                  ')
	for x in range(LINES-4):
		try:
			windowpanel[0].addstr(2+x,4,str(gpio.strip('\n').split('\n')[x+index]))
		except:
			pass
		warning = "up/down arrow to scroll, b to exit"
		windowpanel[0].addstr(LINES-2,4,warning,curses.A_BOLD)
	return index

def mainMenu(stdscr, currentMenuItem, menuitems):
	while True:
		c = 0
		c = stdscr.getch()						#get a character

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
			stdscr.addstr(10,20,"YOU HAVE SELECTED: %s" %currentMenuItem, curses.A_BOLD)
			if currentMenuItem=="GPIO":
				gpioMenu(stdscr,board)
				currentMenuItem=menuitems[0]
				#highlightMenu(currentMenuItem,stdscr,board)
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
				usbMenu(stdscr)
				stdscr.erase()
				updateScreen(stdscr)
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
		updateScreen(stdscr)
		highlightMenu(currentMenuItem,stdscr,board)	#display selection
		if c == 98: # b  key to quit
			curses.endwin()
			quit()

def pinStats(pin,screen,pinNumbers):
	for x in range(0,5):
		screen.addstr(x,0,'             ')
	actualpin = pinNumbers[pin]  #get actual pin number, aka PC7=71 or whatever
	if actualpin == -1:
		slot1="cant change"
		screen.addstr(0,0,slot1,curses.A_STANDOUT)
		updateScreen(screen)
		return
	else:
		slot1='sysfs#: '
		screen.addstr(0,0,slot1+str(actualpin),curses.A_STANDOUT)
		if os.path.isdir('/sys/class/gpio/gpio'+str(actualpin)) == False:#no config dir
			configured1="This pin not"
			configured2="configured"
			screen.addstr(1,0,configured1,curses.A_STANDOUT)
			screen.addstr(2,1,configured2,curses.A_STANDOUT)
		else:
			success="configured"
			screen.addstr(1,0,success,curses.A_STANDOUT)
			status = "cur val: " + str(readPinsysfs(actualpin))  
			screen.addstr(2,0,status,curses.A_STANDOUT) 
			status2 = "cur dir: "
			file = '/sys/class/gpio/gpio'+str(actualpin)+'/direction'
			p = subprocess.Popen(['cat',file],stdout=subprocess.PIPE)
			out, err = p.communicate()
			status2 += out.strip('\n')
			screen.addstr(3,0,status2,curses.A_STANDOUT) 
			status3= "activelow: "
			activelow=str(readSysfs(actualpin,'active_low').strip('\n'))
			screen.addstr(4,0,status3+activelow,curses.A_STANDOUT)
	updateScreen(screen)

def highlightMenu(menuitem,screen,board): #need to pass it stdscr
	'''
	takes a string which is in an array and highlights the element it is referring to as described in the array
	"STRING"[starty,startx,endy,endx]
	
	   startx
	starty-> .------------------.
	         |                  |
	         |                  |
	         .------------------. <---endy
	                            ^endx
	'''
	try:											#errors out sometimes
		for x in range(0,len(board[0].split('\n'))): #redraw screen with outline
			screen.addstr(x,0,board[0].split('\n')[x])
	except:
		pass
	counter = 0
	for x in range(board[1][board[1].index(menuitem)+1][0],board[1][board[1].index(menuitem)+1][2]+1): #only highlight the areas that need it
		screen.addstr((board[1][board[1].index(menuitem)+1][0])+counter,board[1][board[1].index(menuitem)+1][1],board[0].split('\n')[x][board[1][board[1].index(menuitem)+1][1]:board[1][board[1].index(menuitem)+1][3]], curses.A_BOLD | curses.A_STANDOUT)
		counter=counter+1
	updateScreen(screen)
def setupScreen(screen):
	try:
		curses.curs_set(0)
		screen.nodelay(1)
	except:
		pass
	curses.start_color()
	curses.use_default_colors() 
	for i in range(0, curses.COLORS):
		curses.init_pair(i+1, i, 0)
	screen.timeout(-1)
	#screen.bkgd(' ', curses.color_pair(0 ) )

def clearScreen(screen):
	for x in range(0,LINES):
		screen.hline(x,0,' ',COLUMNS) 		#erase entire screen
		screen.chgat(x,0,curses.A_NORMAL)	#reset to normal attributes

def updateScreen(screen):
	curses.panel.update_panels()
	screen.refresh()

def getBoardMenu(board):
	menuitems=[]
	for x in range(0,len(board[1]),2): #get menu item titles
		menuitems.append(board[1][x])  
	return menuitems
def createPinsysfs(pin):
	if os.path.isdir('/sys/class/gpio/gpio'+str(pin)) == False:
		command = 'echo ' + str(pin) + ' > /sys/class/gpio/export'
		subprocess.call(command,shell=True)
		return 0
	else:
		return -1

def removePinsysfs(pin):
	if os.path.isdir('/sys/class/gpio/gpio'+str(pin)) == True:
		command = 'echo ' + str(pin) + ' > /sys/class/gpio/unexport'
		subprocess.call(command,shell=True)
		return 0
	else:
		return -1

def directionPinsysfs(pin,direction):
	if os.path.isdir('/sys/class/gpio/gpio'+str(pin)) == True:
		command = 'echo ' + str(direction) + ' > /sys/class/gpio/gpio' + str(pin) + '/direction'
		subprocess.call(command, shell=True)
		return 0
	else:
		return -1

def valuePinsysfs(pin, value):
	if os.path.isdir('/sys/class/gpio/gpio'+str(pin)) == True:
		if value == "True" or value == "On" or value ==  1:
			value = 1
		else:
			value = 0
		command = 'echo ' + str(value) + ' > /sys/class/gpio/gpio'+str(pin)+'/value'
		subprocess.call(command,shell=True)
		if readSysfs(pin, 'direction') == 'in': #can't set input high
			return -1
		return 0
	else:
		return -1

def readPinsysfs(pin):
	if os.path.isdir('/sys/class/gpio/gpio'+str(pin)) == True:
		file = '/sys/class/gpio/gpio'+str(pin)+'/value'
		p = subprocess.Popen(["cat",file],stdout=subprocess.PIPE)
		out, err = p.communicate()
		return out.strip('\n')

def readSysfs(pin, filename):
	file = '/sys/class/gpio/gpio'+str(pin)+'/'+str(filename)
	p = subprocess.Popen(["cat",file],stdout=subprocess.PIPE)
	out, err = p.communicate()
	return out.strip('\n')


def readFile(filename):
	with open(filename,"r+") as a:
		lines = a.readlines()
	return lines

def writeFile(filename,strings):
	with open(filename,"w+") as a:
		a.write(strings)
	a.close()

def replaceModules(replace): #modify boot modules
	original = readfile('/etc/modules')
	newstring = ''
	for line in original:
		if line.strip('\n') == replace:
			newstring += replace + '\n'
		newstring += line
	writefile('/etc/modules',newstring)

def Bash(command):
	return subprocess.check_output(['bash','-c',command]).strip('\n').split('\n')

def findThis(command,pattern):
	try:
		Bash(command).index(pattern) 
		return 1
	except:
		return -1

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
	curses.wrapper(test,board)
