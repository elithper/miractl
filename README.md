# miractl

This repo contains a series of simple Python scripts for controlling Boox Mira e-Ink monitors.

## Dependencies

You will need to have python3 installed. In addition, the following module is required:

- `pyusb`

Install the latest official release.

`python -m pip install pyusb`

If you are using linux, you will also need to modify your udev rules.

Create a new file called `58-hid.rules`.

`sudo touch /etc/udev/rules.d/58-hid.rules`

Then open the file in a text editor and paste the following content.

```
SUBSYSTEM=="input", GROUP="input", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0416", ATTRS{idProduct}=="5020", MODE:="666", GROUP="plugdev"
KERNEL=="hidraw*", ATTRS{idVendor}=="0416", ATTRS{idProduct}=="5020", MODE="0666", GROUP="plugdev"
```
Finally, reload your udev rules.

`sudo udevadm control --reload-rules && sudo udevadm trigger`

## Usage

Run like any other Python script.

`./mira-refresh.py`
