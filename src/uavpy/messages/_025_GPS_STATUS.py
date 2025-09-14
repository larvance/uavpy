import math

from src.uavpy import mavlink
from src.uavpy.utils.satellite import Satellite


def handle_gps_status(self: "mavlink.Mavlink", msg):
    self.gps.satellite_count = msg.satellites_visible
    self.gps.satellites = [
        Satellite(
            used=bool(msg.satellite_used[i]),
            id=msg.satellite_prn[i],
            elevation=math.radians(msg.satellite_elevation[i]),
            azimuth=math.radians(msg.satellite_azimuth[i] * 360 / 255),
            snr=msg.satellite_snr[i]
        ) for i in range(msg.satellites_visible)
    ]
    for cb in self._gps_status_callbacks:
        cb(self.gps)
