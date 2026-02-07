# ebay-handbrake-wrapper

Bridges cheap no-name USB handbrake devices (the kind found on eBay/AliExpress) to a virtual Xbox 360 controller using [vgamepad](https://github.com/yannbouteiller/vgamepad). The handbrake input is mapped to the right trigger of the virtual gamepad.

Linux only.

## udev rule

Copy the included udev rule so the device can be accessed without root:

```sh
sudo cp udev-rule/99-ebay-handbrake.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Then unplug and replug the handbrake.

## Installation

With uv:

```sh
uv tool install /path/to/ebay-handbrake-wrapper
```

With pipx:

```sh
pipx install /path/to/ebay-handbrake-wrapper
```

## Usage

```sh
ebay-handbrake
ebay-handbrake --deadzone 0.1
ebay-handbrake --debug
```

### Options

- `--deadzone FLOAT` - Ignore the lower portion of the input range (0.0 to 1.0). Useful if the handbrake doesn't fully return to zero.
- `--debug` - Print the current handbrake value as a percentage.
