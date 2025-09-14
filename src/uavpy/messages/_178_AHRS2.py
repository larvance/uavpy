import math

from src.uavpy import mavlink


def handle_ahrs2(self: "mavlink.Mavlink", msg):
    self.dcm.roll = msg.roll
    self.dcm.pitch = msg.pitch
    self.dcm.yaw = msg.yaw
    self.dcm.lat = math.radians(msg.lat / 1e7)
    self.dcm.lon = math.radians(msg.lng / 1e7)
    self.dcm.alt = msg.altitude
