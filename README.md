# armbian-helper
Interactive Hardware Manager for ARM boards running Armbian

## Main concept
There is no main compendium of knowledge about the allwinner CPUs and the single board computers based on their products. You have to hunt for any information and the amount of yak shaving is immense. This is disadvantageous for anyone just trying to get their board up the way they want. 

This repo hopes to shave some hours from research and protoyping by combining common operations into a textual user interface which will be intuitive and hopefully helpful.

Currently only aiming to support the H3 CPU, but this could be extended to other similar chips with similar capabilities.

## Usage
run ./armbian-helper.py and use the arrow keys to select the interface you would like to interact with. Currently only the GPIO interface is managable via sysfs. Press 'h' in any menu for a help window, and press 'm' for more detailed information. 

![example](https://github.com/MitchRatquest/armbian-helper/blob/master/example.gif?raw=true)

## TODO:
- decide whether to support 3.4.113 or not
- autodetect board
- benchmark sysfs vs gpiod
- add USB OTG legacy and configfs configurations
- test IR
- get USB physical positions in relation to their actual data addresses
- dtc compiler for dtbs
- test HDMI with h3disp
- ethernet stats
- iptables forwarding 
- hostapd
- anything to do with wireless
- get CSI camera for testing
