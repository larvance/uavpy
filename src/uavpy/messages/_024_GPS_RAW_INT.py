import math

from src.uavpy import mavlink
from src.uavpy.enums.common_enums import GPS_FIX_TYPE


def handle_gps_raw_int(self: "mavlink.Mavlink", msg):
    t = msg.time_usec / 1e6
    if t > 1.7e9:
        self.time_unix = t
    else:
        self.since_boot = t
    self.gps.fix_type = GPS_FIX_TYPE[msg.fix_type]
    self.gps.lat = msg.lat / 1e7
    self.gps.lon = msg.lon / 1e7
    self.gps.alt = msg.alt / 1e3
    self.gps.horizontal_dilution = None if msg.eph == 0xffff else msg.eph / 1e2
    self.gps.vertical_dilution = None if msg.epv == 0xffff else msg.epv / 1e2
    self.gps.velocity = None if msg.vel == 0xffff else msg.vel / 1e2
    self.gps.cog = None if msg.cog == 0xffff else math.radians(msg.cog / 1e2)
    self.gps.satellite_count = 0 if msg.satellites_visible == 0xff else msg.satellites_visible
    self.gps.alt_ellipsoid = msg.alt_ellipsoid / 1e3 if hasattr(msg, "alt_ellipsoid") else None
    self.gps.h_acc = msg.h_acc / 1e3 if hasattr(msg, "h_acc") else None
    self.gps.v_acc = msg.v_acc / 1e3 if hasattr(msg, "v_acc") else None
    self.gps.vel_acc = msg.vel_acc / 1e3 if hasattr(msg, "vel_acc") else None
    self.gps.hdg_acc = math.radians(msg.hdg_acc / 1e5) if hasattr(msg, "hdg_acc") else None
    self.gps.yaw = None if not hasattr(msg, "yaw") or msg.yaw == 0 or msg.yaw == 0xffff \
        else math.radians(msg.yaw / 1e2)
