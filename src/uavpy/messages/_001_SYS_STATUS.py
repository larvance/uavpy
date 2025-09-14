from src.uavpy import mavlink
from src.uavpy.enums.common_enums import MAV_SYS_STATUS_SENSOR
from src.uavpy.utils import flag_conv
from src.uavpy.utils.sys_status_sensor import SysStatusSensor


def handle_sys_status(self: "mavlink.Mavlink", msg):
    self.onboard_control_sensors.present = SysStatusSensor(msg.onboard_control_sensors_present)
    self.onboard_control_sensors.enabled = SysStatusSensor(msg.onboard_control_sensors_enabled)
    self.onboard_control_sensors.health = SysStatusSensor(msg.onboard_control_sensors_health)
    for k in "present", "enabled", "health":
        setattr(
            self.onboard_control_sensors, k,
            flag_conv(getattr(msg, f"onboard_control_sensors_{k}"), MAV_SYS_STATUS_SENSOR)
        )
    if hasattr(msg, "onboard_control_sensors_extended"):
        self.onboard_control_sensors.present_extended = 1
        self.onboard_control_sensors.enabled_extended = 1
        self.onboard_control_sensors.health_extended = 1
    else:
        self.onboard_control_sensors.present_extended = 0
        self.onboard_control_sensors.enabled_extended = 0
        self.onboard_control_sensors.health_extended = 0

    self.load = msg.load / 1e3
    self.voltage_battery = msg.voltage_battery / 1e3
    self.current_battery = msg.current_battery / 1e2
    self.battery_remaining = None if msg.battery_remaining == -1 else msg.battery_remaining / 1e2
    self.communication_drop_rate = msg.drop_rate_comm / 1e4
    self.communication_errors = msg.errors_comm
    self.errors_count1 = msg.errors_count1
    self.errors_count2 = msg.errors_count2
    self.errors_count3 = msg.errors_count3
    self.errors_count4 = msg.errors_count4
