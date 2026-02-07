import argparse
import signal

import vgamepad as vg

from .handbrake_usb import Handbrake


def main():
    parser = argparse.ArgumentParser(description="Bridge a no-name USB handbrake to a virtual Xbox 360 gamepad.")
    parser.add_argument(
        "--deadzone",
        type=float,
        default=0.0,
        help="Lower deadzone percentage as a float between 0 and 1 (default: 0.0)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print handbrake values to the console",
    )
    args = parser.parse_args()

    if not 0.0 <= args.deadzone <= 1.0:
        parser.error("--deadzone must be between 0 and 1")

    hb = Handbrake(deadzone=args.deadzone)
    print("Found the handbrake device.")

    gamepad = vg.VX360Gamepad()
    print('Created the virtual X360 controller.')

    running = True

    def shutdown(sig, frame):
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, shutdown)

    while True:
        if not running:
            print('\nBye!')
            break
        
        value = hb.read()
        if args.debug:
            print(f"Handbrake value: {value / 255:.0%}")

        gamepad.right_trigger(value=value)
        gamepad.update()

    gamepad.reset()
    gamepad.update()


if __name__ == "__main__":
    main()
