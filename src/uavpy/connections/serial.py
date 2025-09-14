from src.uavpy.mavlink import Mavlink


class SerialMavlink(Mavlink):
    def __init__(
            self,
            location=None,
            bauds=None,
            timeout=5
    ):
        super().__init__(location or ["/dev/serial0"], bauds or [115200, 57600, 921600], timeout)
