from src.uavpy.mavlink import Mavlink


class MicroUSBMavlink(Mavlink):
    def __init__(
            self,
            locations=None,
            bauds=None,
            timeout=5
    ):
        super().__init__(locations or ["/dev/ttyACM0", "/dev/ttyAMA0"], bauds or [115200, 57600, 921600], timeout)
