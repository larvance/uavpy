from time import time

from src.uavpy import mavlink
from src.uavpy.enums.extra_enums import PX4_CUSTOM_MODES
from src.uavpy.enums.minimal_enums import MAV_MODE_FLAG, MAV_AUTOPILOT, MAV_TYPE, MAV_STATE
from src.uavpy.utils.log import debug


def handle_heartbeat(self: "mavlink.Mavlink", msg):
    if self.last_heartbeat is None:
        debug(f"Connected to {self.connection_string} at {self.baud_rate} baud.")
    self.type = MAV_TYPE[msg.type]
    self.autopilot = MAV_AUTOPILOT[msg.autopilot]
    self.base_mode = msg.base_mode
    self.custom_mode = msg.custom_mode
    self.system_status = MAV_STATE[msg.system_status]
    self.mavlink_version = msg.mavlink_version
    self.last_heartbeat = time()
    is_armed = bool(self.base_mode & MAV_MODE_FLAG["SAFETY_ARMED"])
    self.is_armed = is_armed
    if not self.is_armed:
        self.mode = "DISARMED"
    elif self.base_mode & MAV_MODE_FLAG["MANUAL_INPUT_ENABLED"]:
        self.mode = "MANUAL"
    elif self.base_mode & MAV_MODE_FLAG["GUIDED_ENABLED"]:
        self.mode = "GUIDED"
    elif self.base_mode & MAV_MODE_FLAG["AUTO_ENABLED"]:
        self.mode = PX4_CUSTOM_MODES.get(msg.custom_mode, "AUTO")
    elif self.base_mode & MAV_MODE_FLAG["STABILIZE_ENABLED"]:
        self.mode = "STABILIZE"
    elif self.base_mode & MAV_MODE_FLAG["TEST_ENABLED"]:
        self.mode = "TEST"
    elif self.base_mode & MAV_MODE_FLAG["HIL_ENABLED"]:
        self.mode = "HIL"
    else:
        self.mode = "UNKNOWN"
