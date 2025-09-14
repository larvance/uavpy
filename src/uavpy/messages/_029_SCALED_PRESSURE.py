from src.uavpy import mavlink


def handle_scaled_pressure(self: "mavlink.Mavlink", msg):
    self.since_boot = msg.time_boot_ms / 1e3
    self.pressure.absolute = msg.press_abs * 1e2
    self.pressure.differential = msg.press_diff * 1e2
    self.pressure.temperature = msg.temperature / 1e2
    if msg.temperature_press_diff == 0.0:
        self.pressure.differential_temperature = None
    elif msg.temperature_press_diff == 1.0:
        self.pressure.differential_temperature = 0.0
    else:
        self.pressure.differential_temperature = msg.temperature_press_diff / 1e2
