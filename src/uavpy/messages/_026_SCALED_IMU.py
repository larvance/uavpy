import math

from src.uavpy import mavlink


def handle_scaled_imu(self: "mavlink.Mavlink", msg):
    self.since_boot = msg.time_boot_ms / 1e3
    self.accelerometer.x = msg.xacc / 1e3
    self.accelerometer.y = msg.yacc / 1e3
    self.accelerometer.z = msg.zacc / 1e3
    self.gyroscope.x = math.radians(msg.xgyro / 1e3)
    self.gyroscope.y = math.radians(msg.ygyro / 1e3)
    self.gyroscope.z = math.radians(msg.zgyro / 1e3)
    self.magnetometer.x = msg.xmag / 1e3
    self.magnetometer.y = msg.ymag / 1e3
    self.magnetometer.z = msg.zmag / 1e3
    if msg.temperature == 0.0:
        self.temperature = None
    elif msg.temperature == 1.0:
        self.temperature = 0.0
    else:
        self.temperature = msg.temperature / 1e2
