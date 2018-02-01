#!/usr/bin/python
import curses, curses.panel, os, subprocess

COLUMNS=79 #default tty size - 1 
LINES=23

def make_panel(h,l, y,x):
	win = curses.newwin(h,l, y,x)
	win.erase()
	win.box()
	panel = curses.panel.new_panel(win)
	return win, panel

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

def highlightMenu(menuitem,screen,board): #need to pass it screen
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
