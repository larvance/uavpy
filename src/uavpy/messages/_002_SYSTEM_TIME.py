from src.uavpy import mavlink


def handle_system_time(self: "mavlink.Mavlink", msg):
    self.time_unix = msg.time_unix_usec / 1e6
    self.since_boot = msg.time_boot_ms / 1e3
