import math

from src.uavpy import mavlink


def handle_global_position_int(self: "mavlink.Mavlink", msg):
    self.since_boot = msg.time_boot_ms / 1e3
    self.lat = math.radians(msg.lat / 1e7)
    self.lon = math.radians(msg.lon / 1e7)
    self.alt = msg.alt / 1e3
    self.relative_alt = msg.relative_alt / 1e3
    self.velocity.north = msg.vx / 1e2
    self.velocity.east = msg.vy / 1e2
    self.velocity.up = -msg.vz / 1e2
    # self.gps.cog = None if msg.hdg == 0xffff else math.radians(msg.hdg / 100)
