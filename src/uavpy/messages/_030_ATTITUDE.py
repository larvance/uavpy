from src.uavpy import mavlink


def handle_attitude(self: "mavlink.Mavlink", msg):
    self.since_boot = msg.time_boot_ms / 1e3
    self.roll = msg.roll
    self.pitch = msg.pitch
    self.yaw = msg.yaw
    self.velocity.roll = msg.rollspeed
    self.velocity.pitch = msg.pitchspeed
    self.velocity.yaw = msg.yawspeed
