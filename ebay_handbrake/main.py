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
        "--axis-index",
        type=int,
        default=3,
        help="Index of the handbrake axis byte in the USB data packet (default: 3). Use --debug to find your index if the default doesn't work.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print handbrake values to the console",
    )
    args = parser.parse_args()

    if not 0.0 <= args.deadzone <= 1.0:
        parser.error("--deadzone must be between 0 and 1")

    hb = Handbrake(deadzone=args.deadzone, axis_index=args.axis_index, debug_values=args.debug)
    print("Found the handbrake device.")

    gamepad = vg.VX360Gamepad()
    print('Created the virtual X360 controller.')

    running = True

    def shutdown(_sig, _frame):
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, shutdown)

    while True:
        if not running:
            print('\nBye!')
            break
        
        gamepad.right_trigger(value=hb.read())
        gamepad.update()

    gamepad.reset()
    gamepad.update()


if __name__ == "__main__":
    main()
