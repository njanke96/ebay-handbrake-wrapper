# pyright: reportAttributeAccessIssue=warning, reportIndexIssue=warning

from usb import core, util


VENDOR_ID = 0x046D
PRODUCT_ID = 0xC219
HANDBRAKE_BYTE = 3


class Handbrake:
    """Interface to 'eBay' or 'no-name' USB handbrake devices that appear as
    generic DirectInput gamepads.

    Opens the USB device on construction and provides a method to read
    the current handbrake position as a value from 0 to 255.
    """

    def __init__(self, deadzone: float = 0.0):
        """Open the USB handbrake device.

        Args:
            deadzone: A value between 0 and 1 representing the percentage of
                lower input values to ignore. Values within the deadzone return
                0, and the remaining range is scaled back to 0-255.

        Raises:
            ValueError: If the device is not found or has no IN endpoint.
        """
        dev = core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
        if dev is None:
            raise ValueError("Device not found. Is the USB handbrake connected?")

        if dev.is_kernel_driver_active(0):
            dev.detach_kernel_driver(0)

        dev.set_configuration()

        cfg = dev.get_active_configuration()
        intf = cfg[(0, 0)]

        descriptor = util.find_descriptor(
            intf,
            custom_match=lambda e: util.endpoint_direction(e.bEndpointAddress) == util.ENDPOINT_IN,
        )
        if descriptor is None:
            raise ValueError("Is")

        self.dev = dev
        self.descriptor = descriptor
        self.deadzone = deadzone

    def read(self) -> int:
        """Read the current handbrake position.

        Returns:
            An integer from 0 (released) to 255 (fully applied), with the
            deadzone applied.
        """
        data = self.dev.read(self.descriptor.bEndpointAddress, self.descriptor.wMaxPacketSize, timeout=1000)
        raw = int(data[HANDBRAKE_BYTE])
        threshold = self.deadzone * 255
        if raw <= threshold:
            return 0
        return int((raw - threshold) / (255 - threshold) * 255)


# Support running the module directly for a value read test
if __name__ == "__main__":
    hb = Handbrake(deadzone=0.05)
    while True:
        print("Handbrake:", hb.read())
