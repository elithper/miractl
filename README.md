# miractl

A simple Python script for controlling Boox e-ink monitors – both the Boox Mira 13.3" and Boox Mira Pro 25.3" are supported. 

The script has been tested on Linux, Mac and Windows using Python 3.11.

This project is inspired by the excellent [mira-js](https://github.com/ipodnerd3019/mira-js) CLI tool.

## Dependencies

- [Cython](https://github.com/cython/cython)
- [cython-hidapi](https://github.com/trezor/cython-hidapi)

Install both via `pip`.

```
pip install Cython
pip install hidapi
```

## Setup

While the script can be run with a simple `./miractl.py [OPTIONS]`, placing it somewhere in your $PATH is recommended. For example, on Linux/Mac:

```
sudo cp ./miractl.py /usr/local/bin/miractl
sudo chmod 755 /usr/local/bin/miractl
```

If you are using Linux, you will also need to modify your udev rules.

Create a new file called `58-hid.rules`.

```
sudo touch /etc/udev/rules.d/58-hid.rules
```

Then open the file in a text editor and paste the following content.

```
SUBSYSTEM=="input", GROUP="input", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0416", ATTRS{idProduct}=="5020", MODE:="666", GROUP="plugdev"
KERNEL=="hidraw*", ATTRS{idVendor}=="0416", ATTRS{idProduct}=="5020", MODE="0666", GROUP="plugdev"
```

Finally, reload your udev rules.

```
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Usage

> Note: replace `./miractl.py` with `miractl` if you have added the script to your $PATH as described in Setup.

Get help:

```
./miractl.py -h
```

Simple refresh:

```
./miractl.py --clear
```

Configure monitor settings:

```
./miractl.py --refresh-mode {direct_update,grey_update,a2}
             --speed [1-7]
             --contrast [0-15]
             --dither-mode [0-3]
             --white-filter [0-254]
             --black-filter [0-254]
             --cool-light [0-254]
             --warm-light [0-254]
             --antiflicker {disabled,low,middle,high}
```

Any number of settings can be set in a single command, e.g.

```
./miractl.py --speed 5 --contrast 11 --cool-light 127
```

However, `--white-filter` and `--black-filter` must be set together.

```
./miractl.py --white-filter 80 --black-filter 120
```

## Display modes

There are 5 display modes which can be set using the `--display-mode` flag: `speed`, `text`, `image`, `video` and `read`.

```
./miractl.py --display-mode text
```

Since display modes are simply combinations of other flags, the display mode overrides any other settings in your command. For example, in the following command the values for `--contrast` and `--dither-mode` are ignored – the display mode takes precedence.

```
./miractl.py --display-mode speed --contrast 10 --dither-mode 2
```

The only exceptions to this are `--cool-light` and `--warm-light`. Display modes never adjust the frontlight, so they can both be configured in a single command.

```
./miractl.py --display-mode speed --warm-light 110
```

## Antiflicker

Setting `--antiflicker` allows you to select the autodithering algorithm used by the display. While there are several options (`disabled`, `low`, `middle` and `high`), only `high` is recommended.

It is especially important to set this option to `high` on newer ARM-based Macs, which often cause flickering issues otherwise.
