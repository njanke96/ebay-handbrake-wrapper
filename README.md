# ebay-handbrake-wrapper

Simple Python script that bridges cheap no-name USB handbrake devices (the kind found on eBay/AliExpress) to a virtual Xbox 360 controller using [vgamepad](https://github.com/yannbouteiller/vgamepad). The handbrake input is mapped to the right trigger of the virtual gamepad.

For handbrakes that are recognized by `lsusb` as a `Bus 001 Device 007: ID 046d:c219 Logitech, Inc. F710 Gamepad [DirectInput Mode]`.

Only Linux is supported, if your handbrake is not working on Windows, this is not the solution!

## Caveats

- Most games will have existing bindings for RT (probably throttle). Make sure to clear these.
- If a game supports X360 controllers but not rebinding its default controls, this won't work.
  - I can't imagine a game that would support both racing wheels AND not support control rebinding, but who knows.
- If you use an X360 controller along with a handbrake, this won't work unless the game supports multiple X360 controllers.

## Quickstart

1. Clone the repo:

```sh
git clone https://github.com/njanke96/ebay-handbrake-wrapper.git
```

2. Copy the included udev rule so the device can be accessed without root:

```sh
cd path/to/repo
sudo cp udev-rule/99-ebay-handbrake.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

3. Unplug (if plugged in) and (re)plug in the handbrake.

4. Install:

With uv:

```sh
uv tool install .
```

With pipx:

```sh
pipx install .
```

## Usage

```
usage: ebay-handbrake [-h] [--deadzone DEADZONE] [--debug]

Bridge a no-name USB handbrake to a virtual Xbox 360 gamepad.

options:
  -h, --help           show this help message and exit
  --deadzone DEADZONE  Lower deadzone percentage as a float between 0 and 1 (default: 0.0)
  --debug              Print handbrake values to the console
```

## Steam integration

You can start the handbrake automatically when launching a game via Steam launch options:

```sh
/home/yourusername/.local/bin/ebay-handbrake --deadzone 0.1 & %command%; pgrep ebay-handbrake | xargs kill
```

This starts `ebay-handbrake` in the background, and launches the game.

This will not work for Flatpak steam installations.
