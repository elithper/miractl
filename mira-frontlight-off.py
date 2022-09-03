#!/usr/bin/env python

import usb.core
import usb.util
import time

vid = 0x0416
pid = 0x5020

# Create list of all Boox Mira devices
device_list = usb.core.find(idVendor=vid, idProduct=pid, find_all=True)

def lightoff(dev):
    dev.reset()    
    if dev.is_kernel_driver_active(0):
        dev.detach_kernel_driver(0)
    dev.set_configuration()
    
    # Turn off cool light
    dev.write(1, '\x06\x00', 0)
    
    # Wait 100 milliseconds    
    time.sleep(0.1)
    
    # Turn off warm light
    dev.write(1, '\x07\x00', 0)

def main():
    # Iterate through device list and disable frontlights sequentially
    for dev in device_list:
        lightoff(dev)

if __name__ == "__main__":
    main()
