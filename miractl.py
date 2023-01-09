#!/usr/bin/env python

import argparse
import usb.core
import usb.util

# Set opcodes
CLEAR = 1
REFRESH_MODE = 2
SPEED = 4
CONTRAST = 5
COOL_LIGHT = 6
WARM_LIGHT = 7
DITHER_MODE = 9
COLOUR_FILTER = 11


# Define refresh modes
refresh_modes = {
    "direct_update": 1,
    "grey_update": 2,
    "a2": 3
}

# Define display modes
text_mode = {
    'refresh_mode': 'a2',
    'contrast': 7,
    'speed': 6,
    'dither_mode': 1,
    'white_filter': 0,
    'black_filter': 0
}

speed_mode = {
    'refresh_mode': 'a2',
    'contrast': 8,
    'speed': 7,
    'dither_mode': 0,
    'white_filter': 0,
    'black_filter': 0
}

image_mode = {
    'refresh_mode': 'direct',
    'contrast': 7,
    'speed': 5,
    'dither_mode': 0,
    'white_filter': 0,
    'black_filter': 0
}

video_mode = {
    'refresh_mode': 'a2',
    'contrast': 7,
    'speed': 6,
    'dither_mode': 2,
    'white_filter': 10,
    'black_filter': 0
}

read_mode = {
    'refresh_mode': 'direct',
    'contrast': 7,
    'speed': 5,
    'dither_mode': 3,
    'white_filter': 12,
    'black_filter': 10
}

# Combine display modes into dict
display_presets = {
    'text': text_mode,
    'speed': speed_mode,
    'image': image_mode,
    'video': video_mode,
    'read': read_mode
}

def set_display_preset(mode, args):
    for setting in display_presets[mode]:
        print('Setting', setting, 'to:', display_presets[mode][setting])
        setattr(args, setting, display_presets[mode][setting])
    print(args)

def send_code(dev, code):
    dev.reset()
    if dev.is_kernel_driver_active(0):
        dev.detach_kernel_driver(0)
    dev.set_configuration()
    dev.write(1, code, 0)


def find_devices():
    '''
    Returns all Boox Mira devices.
    '''
    VID = 0x0416
    PID = 0x5020

    # Find initial Boox Mira device
    dev = usb.core.find(idVendor=VID, idProduct=PID)
    
    # Generate device list
    if dev is not None:
        return usb.core.find(idVendor=VID, idProduct=PID, find_all=True)
    else:
        raise 'No Boox Mira devices found'

def parse_args():
    parser = argparse.ArgumentParser(
        prog = 'miractl',
        description = 'A tool for controlling and configuring Boox Mira displays.')

    parser.add_argument('--display-mode',
                        dest='display_mode',
                        action='store',
                        choices=['speed', 'text', 'image', 'video', 'read']
    )

    parser.add_argument('--refresh-mode',
                        dest='refresh_mode',
                        action='store',
                        choices=['direct_update', 'grey_update', 'a2']
    )

    parser.add_argument('--clear',
                        dest='clear',
                        action='store_true',
                        default=False
    )

    parser.add_argument('--speed',
                        dest='speed',
                        action='store',
                        type=int,
                        choices=range(1, 8),
                        metavar="[1-7]"
    )

    parser.add_argument('--contrast',
                        dest='contrast',
                        action='store',
                        type=int,
                        choices=range(0, 16),
                        metavar="[0-15]"
    )

    parser.add_argument('--dither-mode',
                        dest='dither_mode',
                        action='store',
                        type=int,
                        choices=range(0, 4),
                        metavar="[0-3]"
    )

    parser.add_argument('--white-filter',
                        dest='white_filter',
                        action='store',
                        type=int,
                        choices=range(0, 255),
                        metavar="[0-254]"
    )

    parser.add_argument('--black-filter',
                        dest='black_filter',
                        action='store',
                        type=int,
                        choices=range(0, 255),
                        metavar="[0-254]"
    )

    parser.add_argument('--cool-light',
                        dest='cool_light',
                        action='store',
                        type=int,
                        choices=range(0, 255),
                        metavar="[0-254]"
    )

    parser.add_argument('--warm-light',
                        dest='warm_light',
                        action='store',
                        type=int,
                        choices=range(0, 255),
                        metavar="[0-254]"
    )

    return parser.parse_args()


def set_args(args, device_list):
    for dev in device_list:
        if args.display_mode is not None:
            set_display_preset(args.display_mode, args)

        if args.speed is not None:
            speed_val = 11 - args.speed
            byte_list = [SPEED, speed_val]
            send_code(dev, byte_list)

        if args.contrast is not None:
            byte_list = [CONTRAST, args.contrast]
            send_code(dev, byte_list)

        if args.dither_mode is not None:
            byte_list = [DITHER_MODE, args.dither_mode]
            send_code(dev, byte_list)

        if args.refresh_mode is not None:
            mode = refresh_modes[args.refresh_mode]
            byte_list = [REFRESH_MODE, mode]
            send_code(dev, byte_list)

        if args.cool_light is not None:
            byte_list = [COOL_LIGHT, args.cool_light]
            send_code(dev, byte_list)

        if args.warm_light is not None:
            byte_list = [WARM_LIGHT, args.warm_light]
            send_code(dev, byte_list)

        if args.white_filter is not None and args.black_filter is not None:
            white = 255 - args.white_filter
            black = args.black_filter
            byte_list = [COLOUR_FILTER, white, black]
            send_code(dev, byte_list)

        if args.clear:
            byte_list = [CLEAR]
            send_code(dev, byte_list)


if __name__ == '__main__':
    set_args(parse_args(), find_devices())