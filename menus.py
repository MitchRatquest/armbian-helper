'''
basicinfo = [
outline, 		#initial ascii drawing on screen
menu, 			#describes all selectable elements by name and area
pinsEnglish, 	#human readable pins and functions
pinsBGA,		#sysfs pin numbers on H3 chip
]
'''
supporteBoards=["orangepione","nanopineo","orangepipc","orangepizero"] #first line of /etc/armbian-release
#Bash("grep BOARD= /etc/armbian-release")[1] = board name
###########################
#
# NANOPI NEO
#
###########################
nanopineoMenu=[ #areas to highlight
"ETH0",[0,11,8,25], 
"USB0",[0,27,8,33],
"AUDIO",[3,35,7,36],
"UART",[5,38,9,39],
"USB/I2S",[5,40,19,45],
"MICROSD",[16,23,22,38],
"USBOTG",[20,11,23,19],
"GPIO",[4,3,20,10]
]

nanopineoOutline="""           .------------.  .----.
   .-------|            |--|    |-----------.
   |       |            |  |    |           |
   |       |            |  | U  |  A        |
   .-----. |   ETH0     |  | S  |  U        |
   |     | |            |  | B  |  D  U .---.
   |     | |            |  |    |  I  A |   |
   |     | |            |  |    |  O  R |   |
   |     | '------------'  '----'     T |   |
   |     |                              | U |
   | G   |                              | S |
   | P   |                              | B |
   | I   |         NANOPI NEO           | / |
   | O   |                              | I |
   |     |                              | 2 |
   |     |                              | S |
   |     |             .-------------.  |   |
   |     |             |             |  |   |
   |     |             |             |  |   |
   |     | <PIN 1      |   MICROSD   |  '---'
   '-----' .------.    |             |      |
   |       | USB  |    |             |      |
   '-------| OTG  |----'-------------'------'
           '------'                          """
nanopineoPinsEnglish=[ '',#need dummy first string?
'3.3 volts',					'5 volts',
'I2C0-SDA / PA12',				'5 volts',
'I2C0-SCK /PA11',				'Ground',
'PMW1 / PA6', 					'SPI1-CS / PA13',
'Ground',						'SPI1-CLK / PA14',
'UART2-RX / PA1',				'PD14',
'UART2-TX / PA0', 				'Ground',
'UART2-CTS / PA3', 				'PC4',
'3.3 volts',					'PC7',
'SPI0-MOSI / PC0',				'Ground',
'SPI0-MISO / PC1',				'UART2_RTS / PA2',
'SPI0-CLK / PC2',				'SPI0-CS / PC3'
]
nanopineoPinsBGA=[
-1,-1,
12,-1,
11,-1,
6,13,
-1,14,
1,110,
0,-1,
3,68,
-1,71,
64,-1,
65,2,
66,67
]
nanopineoSmallPinsEnglish=['',
'5 volts',
'USB-DP1',
'USB-DM1',
'USB-DP2',
'USB-DM2',
'GPIOL11 / IR-RX',
'SPDIF-OUT / GPIOA17',
'PCM0-SYNC / I2S0-LRC',
'PCM0-CLK / I2S0-BCK',
'PCM0-DOUT / I2S0-SDOUT',
'PCM0-DIN / I2S0-DIN',
'Ground'
]
nanopineoPinsAudio=[
'Mic-in Positive',
'Mic-in Negative',
'Line out Right',
'Ground',
'Line out left'
]

nanopineoUART=[
'Ground',
'5 volts',
'TX',
'RX'
]
neo = []
neo.append(nanopineoOutline)
neo.append(nanopineoMenu)
neo.append(nanopineoPinsEnglish)
neo.append(nanopineoPinsBGA)
neo.append(nanopineoSmallPinsEnglish)
neo.append(nanopineoPinsAudio)
neo.append(nanopineoUART)

###########################
#
# ORANGE PI ONE
#
###########################
orangepiOneMenu=[
"GPIO",[0,10,3,62],
"MICROSD",[12,36,19,51],
"HDMI",[16,16,21,31],
"USBOTG",[17,6,20,13],
"UART",[15,7,15,11],
"ETH0",[8,1,14,17],
"USB",[5,2,7,15]
]
orangepiOneOutline="""    .-----.--------------------------------------------------.-------.
    |     |                       GPIO                       | <PIN 1|
    |     |                                                  |       |
    |     '--------------------------------------------------'       |
    |                                                                |
  .-----------.                                                      |
  |    USB    |                                                      |
  '-----------'                                                      |
 .--------------.          ORANGE PI ONE                             |
 |              |                                                    |
 |              |                                                    |
 |    ETH0      |                                                    |
 |              |                   .-------------.                  |
 |              |                   |             |                  |
 '--------------'                   |             |      .----.      |
    |  UART                         |             |      |  D |      |
    |           .-------------.     |   MICROSD   |      |  C |      |
    | .-----.   |             |     |             |      |  - |      |
    | | USB |   |    HDMI     |     |             |      |  I |      |
    '-| OTG |---|             |-----'-------------'------|  N |------'
      '-----'   |             |                          '----'      
                '-------------'                                      """
orangepiOnePinsEnglish=['',
'3.3 volts',					'5 volts',
'I2C0-SDA / PA12',				'5 volts',
'I2C0-SCK /PA11',				'Ground',
'PMW1 / PA6', 					'SPI1-CS / PA13',
'Ground',						'SPI1-CLK / PA14',
'UART2-RX / PA1',				'PD14',
'UART2-TX / PA0', 				'Ground',
'UART2-CTS / PA3', 				'PC4',
'3.3 volts',					'PC7',
'SPI0-MOSI / PC0',				'Ground',
'SPI0-MISO / PC1',				'UART2_RTS / PA2',
'SPI0-CLK / PC2',				'SPI0-CS / PC3',
'Ground',						'PCM0-DIN / PA21',
'PCM0-CLK / I2C1-SDA / PA19',	'PCM0-SYNC / I2C1-SCK / PA18',
'PA7', 							'Ground',
'PA8', 							'PG8',
'PA9', 							'Ground',
'PA10',							'PG9',
'PA20',							'PG6',
'Ground',						'PG7'
]
orangepiOnePinsBGA=[
-1,-1,
12,-1,
11,-1,
6,13,
-1,14,
1,110,
0,-1,
3,68,
-1,71,
64,-1,
65,2,
66,67,
-1,21,
19,18,
7,1,
8,200,
9,-1,
10,201,
20,196,
-1,197
]

orangepiOneUART=[
'Ground',
'RX',
'TX'
]
opione=[]
opione.append(orangepiOneOutline)
opione.append(orangepiOneMenu)
opione.append(orangepiOnePinsEnglish)
opione.append(orangepiOnePinsBGA)
opione.append(orangepiOneUART)

###########################
#
# ORANGE PI PC
#
###########################
orangepiPCMenu=[
"GPIO",[0,7,3,65],
"IR",[0,66,2,71],
"USB",[4,63,6,80],
"ETH0",[7,61,13,80],
"USBX2",[14,63,19,80],
"AUDIO",[17,54,23,60],
"MIC",[20,42,22,47],
"HDMI",[18,24,23,39],
"UART",[21,17,21,21],
"CSI",[9,2,17,7],
"USBOTG",[4,1,8,6]
]


orangepiPCOutline="""  .----.--------------------------------------------------------.-.---.---.
  |    |                                                        | |IR |   |
  |    |                            GPIO                        | '---'   |
  |    '--------------------------------------------------------'         |
 .---.  ^PIN 1                                                 .---------------.
 |U  |                   <- USE ARROW KEYS ->                  |     USB       |
 |S  |                    SPACEBAR TO SELECT                   '---------------'
 |B  |                                                       .-----------------.
 '---'                    ORANGE PI PC                       |                 |
  .---.                                                      |                 |
  |   |                                                      |      ETH0       |
  |   |                                                      |                 |
  | C |                                                      |                 |
  | S |                                                      '-----------------'
  | I |                                                        .---------------.
  |   |                                                        |               |
  |   |                                                        |     USB       |
  '---'                                               .----.   |      X2       |
  |     .---.           .-------------.               | A  |   |               |
  |     | D |           |             |               | U  |   '---------------'
  |     | C |           |             |   .---.       | D  |              |   
  |     | I |    UART   |    HDMI     |   |MIC|       | I  |              |   
  '-----| N |-----------|             |---'---'-------| O  |--------------'   
        '---'           '-------------'               '----'                   """
'''
pins:
	direction in out
	value 0 1
	gnd
	5v
	3v
	spi
	i2c
	
pin=raw_input();((ord(pin[1].lower())-97)*32)+int(pin[2:])

'''
orangepiPCPins=[
'3.3 volts'					,-1,'5 volts'  					,-1,
'I2C0-SDA / PA12'			,12,'5 volts'						,-1,
'I2C0-SCK /PA11' 			,11,'Ground'						,-1,
'PMW1 / PA6'				,6, 'SPI1-CS / PA13'				,13,
'Ground'					,-1,'SPI1-CLK / PA14'				,14,
'UART2-RX / PA1'			,1, 'PD14'						,110,
'UART2-TX / PA0'			,0, 'Ground'						,-1,
'UART2-CTS / PA3'			,3, 'PC4'							,68,
'3.3 volts'					,-1,'PC7'							,71,
'SPI0-MOSI / PC0'			,64,'Ground'						,-1,
'SPI0-MISO / PC1'			,65,'UART2_RTS / PA2'				,2,
'SPI0-CLK / PC2'			,66,'SPI0-CS / PC3'				,67,
'Ground'					,-1,'PCM0-DIN / PA21'				,21,
'PCM0-CLK / I2C1-SDA / PA19',19,'PCM0-SYNC / I2C1-SCK / PA18'	,18,
'PA7'						,7, 'Ground'						,-1,
'PA8'						,8, 'PG8'							,200,
'PA9'						,9, 'Ground'						,-1,
'PA10'						,10,'PG9'							,201,
'PA20'						,20,'PG6'							,196,
'Ground'					,-1,'PG7'							,197
]
orangepiPCPinsEnglish=['',
'3.3 volts',					'5 volts',
'I2C0-SDA / PA12',				'5 volts',
'I2C0-SCK /PA11',				'Ground',
'PMW1 / PA6', 					'SPI1-CS / PA13',
'Ground',						'SPI1-CLK / PA14',
'UART2-RX / PA1',				'PD14',
'UART2-TX / PA0', 				'Ground',
'UART2-CTS / PA3', 				'PC4',
'3.3 volts',					'PC7',
'SPI0-MOSI / PC0',				'Ground',
'SPI0-MISO / PC1',				'UART2_RTS / PA2',
'SPI0-CLK / PC2',				'SPI0-CS / PC3',
'Ground',						'PCM0-DIN / PA21',
'PCM0-CLK / I2C1-SDA / PA19',	'PCM0-SYNC / I2C1-SCK / PA18',
'PA7', 							'Ground',
'PA8', 							'PG8',
'PA9', 							'Ground',
'PA10',							'PG9',
'PA20',							'PG6',
'Ground',						'PG7'
]
orangepiPCPinsBGA=[
-1,-1,
12,-1,
11,-1,
6,13,
-1,14,
1,110,
0,-1,
3,68,
-1,71,
64,-1,
65,2,
66,67,
-1,21,
19,18,
7,1,
8,200,
9,-1,
10,201,
20,196,
-1,197
]

orangepiPCUART=[
'Ground',	#nearest the DC barrel 
'RX',
'TX'		#nearest the HDMI
]

coolUSB="""  .------.
 /      /|
.------. |
| USB2 | |
|------| '
| USB1 |/ 
'------'  
"""

opipc=[]
opipc.append(orangepiPCOutline)
opipc.append(orangepiPCMenu)
opipc.append(orangepiPCPinsEnglish)
opipc.append(orangepiPCPinsBGA)
opipc.append(orangepiPCUART)

PINS="""                                   .-------.
                         3.3 volts | 1  2  | 5 volts
                    I2C_SDA / PA12 | 3  4  | 5 volts
                    I2C_SCK / PA11 | 5  6  | GND
                        PWM1 / PA6 | 7  8  | PA13 / SPI1_CS   / UART3_TX
                               GND | 9  10 | PA14 / SPI1_CLK  / UART3_RX
                    UART2_RX / PA1 | 11 12 | PD14
                    UART2_TX / PA0 | 13 14 | GND
                   UART2_CTS / PA3 | 15 16 | PC4
                         3.3 volts | 17 18 | PC7
                   SPI0-MOSI / PC0 | 19 20 | GND
                   SPI0-MISO / PC1 | 21 22 | PA2  / UART2_RTS
                    SPI0-CLK / PC2 | 23 24 | PC3  / SPI0_CS
                               GND | 25 26 | PA21 / PCM0_DIN
        PCM0-CLK / I2C1-SDA / PA19 | 27 28 | PA18 / PCM0_SYNC / SDA1_SCK
                               PA7 | 29 30 | GND
                               PA8 | 31 32 | PG8  / UART1_RTS
                               PA9 | 33 34 | GND
                              PA10 | 35 36 | PG9  / UART1_CTS
                              PA20 | 37 38 | PG6  / UART1_TX
                               GND | 39 40 | PG7  / UART1_RX
                                   '-------'                           
                                                                        
"""
###########################
#
# ORANGE PI ZERO
#
###########################


orangepiZeroOutline="""         .----.  .---------------.
 .-------|    |--|               |--------------.
 |       |    |  |               |   U          |
 .--.    |USB |  |     ETH0      |   A    .-----.
 |  |    |    |  |               |   R    |     |
 |  |    |    |  |               |   T    |     |
 |  |    '----'  |               |        |     |
 |U |            |               |        |     |
 |S |            '---------------'        |     |
 |B |   .-----.                           |     |
 |/ |   |WIFI |  USE ARROW KEYS TO MOVE   |  G  |
 |A |   |     |    SPACEBAR TO SELECT     |  P  |
 |U |   '-----'                           |  I  |
 |D |     .---------------.               |  O  |
 |I |     |               |   .------.    |     |
 |O |     |               |   |      |    |     |
 |/ |     |               |   |      |    |     |
 |T |     |ORANGE PI ZERO |   |      |    |     |
 |V |     |               |   |      |    |     |
 |  |     |               |   |      |    |     |
 |  |     |               |   |      |    |     |
 |--'   .------.----------'   '------'    '-----'
 |      |  USB |                          PIN 1^|
 '------|  OTG |--------------------------------'
        '------'                                 """
orangepiZeroMenu=[ #areas to highlight indexed at top left = 0,0 = y,x
"USB",[0,9,6,15], 
"ETH0",[0,17,8,34],
"UART",[2,37,5,38],
"GPIO",[3,42,21,48],
"USBOTG",[21,8,24,16],
"USB/AUDIO",[3,1,22,5],
"WIFI",[9,8,12,15]
]

orangepiZeroPinsEnglish=['',
'3.3 volts',					'5 volts',
'I2C0-SDA / PA12',				'5 volts',
'I2C0-SCK /PA11',				'Ground',
'PMW1 / PA6', 					'UART1-RX / PG7',
'Ground',						'UART1-TX / PG6',
'UART2-RX / PA1',				'PA7',
'UART2-TX / PA0', 				'Ground',
'UART2-CTS / PA3', 				'IC21-SCK / PA15',
'3.3 volts',					'I2C1-SDA / PA19',
'SPI1-MOSI / PA15',				'Ground',
'SPI1-MISO / PA16',				'UART2_RTS / PA2',
'SPI1-CLK / PA14',				'SPI1-CS / PA13',
'Ground',						'PA10',
]
orangepiZeroPinsBGA=[
-1,-1,
12,-1,
11,-1,
6,199,
-1,198,
1,7,
0,-1,
3,15,
-1,19,
15,-1,
16,2,
14,13,
-1,10
]

orangepiZeroPinsUSB=[
'5 volts',
'Ground',
'USB-DM2',
'USB-DP2',
'USB-DM3',
'USB-DP3',
'Line out Right',
'Line out Left',
'TV out',
'Mic bias',
'Mic in Positive',
'Mic in Negative',
'IR-RX'
]
orangepiZeroUART=[
'Ground', 
'RX',
'TX'
]
opiz=[]
opiz.append(orangepiZeroOutline)
opiz.append(orangepiZeroMenu)
opiz.append(orangepiZeroPinsEnglish)
opiz.append(orangepiZeroPinsBGA)
opiz.append(orangepiZeroPinsUSB)
opiz.append(orangepiZeroUART)
###########################
#
# HELP MENU: GPIO
#
###########################
gpioHelp="""AVAILABLE COMMANDS: 

s - initialize pin
u - unitialiaze pin
r - read pin's current value
i - set pin direction input
o - set pin direction output
1 - set pin high
0 - set pin low


The row of pins on the board have several functions
Pins marked Ground 5 volts and 3.3 volts can't be changed
The other ones can either be general purpose inputs or outputs
They are called GPIO
Some GPIO are part of other systems such as SPI I2C and I2S

----------------------------------------------------------------

Pin names are derived from a formula based on the H3 CPU:
(position of letter in alphabet - 1) * 32 + pin number
So PG14 would be pin number 206
Pins have to be initialized before they can be used
Echo your calculated pin number to /sys/class/gpio/export
This creates the directory /sys/class/gpio/gpio206
Now you can change the properties of the pins
By echoing values to the files in that directory

----------------------------------------------------------------

For more information google 'gpio with sysfs'
With patience you can learn it. Believe in yourself

Press the b key to exit this prompt


more text
more text
 _   _ _____ _     _     ___  
| | | | ____| |   | |   / _ \ 
| |_| |  _| | |   | |  | | | |
|  _  | |___| |___| |__| |_| |
|_| |_|_____|_____|_____\___/ 
                              

"""
