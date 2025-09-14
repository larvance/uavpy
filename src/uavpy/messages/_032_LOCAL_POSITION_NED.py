from src.uavpy import mavlink


def handle_local_position_ned(self: "mavlink.Mavlink", msg):
    self.since_boot = msg.time_boot_ms / 1e3
    self.north = msg.x
    self.east = msg.y
    self.up = -msg.z
    self.velocity.north = msg.vx
    self.velocity.east = msg.vy
    self.velocity.up = -msg.vz
