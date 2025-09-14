import math

from src.uavpy import mavlink


def handle_vfr_hud(self: "mavlink.Mavlink", msg):
    self.airspeed = msg.airspeed
    self.groundspeed = msg.groundspeed
    self.heading = math.radians(msg.heading)
    self.throttle = msg.throttle / 1e2
    self.alt = msg.alt
    self.climb = msg.climb
