# miractl

A simple Python script for controlling Boox e-ink monitors – both the Boox Mira 13.3" and Boox Mira Pro 25.3" are supported.

The project is inspired by the excellent [mira-js](https://github.com/ipodnerd3019/mira-js) CLI tool.

## Dependencies

You will need to have python3 installed. In addition, the following module is required:

- `pyusb`

Install the latest official release.

```
python -m pip install pyusb
```

## Setup

While the script can be run with a simple `./miractl.py [OPTIONS]`, placing it somewhere in your PATH is recommended.

```
sudo cp ./miractl.py /usr/local/bin/miractl
sudo chmod 755 /usr/local/bin/miractl
```

If you are using linux, you will also need to modify your udev rules.

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

> Note: replace `./miractl.py` with `miractl` if you have added the script to your PATH as described in Setup.

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
./miractl.py [--refresh-mode {direct_update,grey_update,a2}] [--speed [1-7]] [--contrast [0-15]] [--dither-mode [0-3]] [--white-filter [0-254]][--black-filter [0-254]] [--cool-light [0-254]] [--warm-light [0-254]]
```

Any number of settings can be set in a single command, e.g.

```
./miractl.py --speed 5 --contrast 11 --cool-light 127
```

However, `--white-filter` and `--black-filter` must be set together.

```
./miractl.py --white-filter 80 --black-filter 120
```
