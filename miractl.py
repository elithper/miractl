#!/usr/bin/env python3

import argparse
import sys
from time import sleep

import hid

# Set vendor and product IDs
VID = 0x0416
PID = 0x5020

# Set opcodes
CLEAR = 1
REFRESH_MODE = 2
SPEED = 4
CONTRAST = 5
COOL_LIGHT = 6
WARM_LIGHT = 7
DITHER_MODE = 9
COLOUR_FILTER = 17
AUTO_DITHER_MODE = 18


# Define refresh modes
refresh_modes = {
    "direct_update": 1,
    "grey_update": 2,
    "a2": 3
}

# Define autodither (antiflicker) modes
auto_dither_modes = {
        "disabled": [0, 0, 0, 0,],
        "low": [1, 0, 30, 10],
        "middle": [1, 0, 40, 10],
        "high": [1, 0, 50, 30]
}

# Define display modes
text_mode = {
    'refresh_mode': 'a2',
    'contrast': 7,
    'speed': 6,
    'dither_mode': 1,
    'white_filter': 0,
    'black_filter': 0,
    'clear': True
}

speed_mode = {
    'refresh_mode': 'a2',
    'contrast': 8,
    'speed': 7,
    'dither_mode': 0,
    'white_filter': 0,
    'black_filter': 0,
    'clear': True
}

image_mode = {
    'refresh_mode': 'direct_update',
    'contrast': 7,
    'speed': 5,
    'dither_mode': 0,
    'white_filter': 0,
    'black_filter': 0,
    'clear': True
}

video_mode = {
    'refresh_mode': 'a2',
    'contrast': 7,
    'speed': 6,
    'dither_mode': 2,
    'white_filter': 10,
    'black_filter': 0,
    'clear': True
}

read_mode = {
    'refresh_mode': 'direct_update',
    'contrast': 7,
    'speed': 5,
    'dither_mode': 3,
    'white_filter': 12,
    'black_filter': 10,
    'clear': True
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
        setattr(args, setting, display_presets[mode][setting])


def send_code(dev, code):
    dev.write([0] + code)
    sleep(0.5)


def find_devices():
    '''
    Returns all Boox Mira devices.
    '''
    if hid.enumerate(VID, PID):
        return hid.enumerate(VID, PID)
    else:
        raise "No Boox Mira devices found"


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

    parser.add_argument('--antiflicker',
                        dest='auto_dither_mode',
                        action='store',
                        choices=['disable', 'low', 'middle', 'high']
    )

    # Print help message if no arguments are given
    return parser.parse_args(args=None if sys.argv[1:] else ['--help'])


def set_args(args, device_list):
    for device in device_list:
        dev = hid.device()
        dev.open(VID, PID, device["serial_number"])
        dev.set_nonblocking(1)

        if args.display_mode is not None:
            display_val = args.display_mode
            set_display_preset(display_val, args)
            print("Setting display mode to", display_val)

        if args.refresh_mode is not None:
            mode = refresh_modes[args.refresh_mode]
            byte_list = [REFRESH_MODE, mode]
            send_code(dev, byte_list)
            print("Refresh mode set to", mode)

        if args.contrast is not None:
            contrast_val = args.contrast
            byte_list = [CONTRAST, contrast_val]
            send_code(dev, byte_list)
            print("Contrast set to", contrast_val)

        if args.speed is not None:
            speed_val = args.speed
            byte_list = [SPEED, 11 - args.speed]
            send_code(dev, byte_list)
            print("Speed set to", speed_val)

        if args.dither_mode is not None:
            dither_val = args.dither_mode
            byte_list = [DITHER_MODE, dither_val]
            send_code(dev, byte_list)
            print("Dither mode set to", dither_val)

        if args.cool_light is not None:
            cool_light_val = args.cool_light
            byte_list = [COOL_LIGHT, cool_light_val]
            send_code(dev, byte_list)
            print("Cool light set to", cool_light_val)

        if args.warm_light is not None:
            warm_light_val = args.warm_light
            byte_list = [WARM_LIGHT, warm_light_val]
            send_code(dev, byte_list)
            print("Warm light set to", warm_light_val)

        if args.white_filter is not None and args.black_filter is not None:
            white = args.white_filter
            black = args.black_filter
            white_adjusted = 255 - white
            byte_list = [COLOUR_FILTER, white_adjusted, black]
            send_code(dev, byte_list)
            print("Colour filter set to {0}/{1} (white/black)".format(white, black))

        if args.auto_dither_mode is not None:
            adm = auto_dither_modes[args.auto_dither_mode]
            byte_list = [AUTO_DITHER_MODE, adm[0], adm[1], adm[2], adm[3]]
            send_code(dev, byte_list)
            print("Antiflicker set to", args.auto_dither_mode, adm)

        if args.clear:
            byte_list = [CLEAR]
            print("Clearing screen...")
            send_code(dev, byte_list)
        
        dev.close()

if __name__ == '__main__':
    set_args(parse_args(), find_devices())
