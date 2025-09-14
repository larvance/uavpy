from dataclasses import dataclass
from typing import List

from src.uavpy.enums.common_enums import MavSysStatusSensorExtended
from src.uavpy.utils.sys_status_sensor import SysStatusSensor


@dataclass
class OnboardControlSensors:
    present = SysStatusSensor(0)
    enabled = SysStatusSensor(0)
    health = SysStatusSensor(0)
    present_extended: List[MavSysStatusSensorExtended] = 0
    enabled_extended: List[MavSysStatusSensorExtended] = 0
    health_extended: List[MavSysStatusSensorExtended] = 0
