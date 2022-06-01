#!/usr/bin/env python

import usb.core
import usb.util

vid = 0x0416
pid = 0x5020

# Create list of all Boox Mira devices
device_list = usb.core.find(idVendor=vid, idProduct=pid, find_all=True)

# Iterate through device list and refresh sequentially
for dev in device_list:
    dev.reset()
    
    if dev.is_kernel_driver_active(0):
        dev.detach_kernel_driver(0)
    
    dev.set_configuration()
    
    dev.write(1, '\x01', 0)
