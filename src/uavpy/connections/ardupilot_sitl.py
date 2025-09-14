from src.uavpy.mavlink import Mavlink


class ArduPilotSITLMavlink(Mavlink):
    def __init__(
            self,
            bauds=None,
            timeout=5
    ):
        super().__init__(["udp:127.0.0.1:14550", "tcp:127.0.0.1:5760"], bauds or [57600, 115200, 921600], timeout)
