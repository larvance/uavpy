from dataclasses import dataclass
from typing import Optional

from pymavlink.dialects.v10.common import MAV_POWER_STATUS_BRICK_VALID, MAV_POWER_STATUS_SERVO_VALID, \
    MAV_POWER_STATUS_USB_CONNECTED, MAV_POWER_STATUS_PERIPH_OVERCURRENT, MAV_POWER_STATUS_PERIPH_HIPOWER_OVERCURRENT, \
    MAV_POWER_STATUS_CHANGED

from src.uavpy.utils.units import V_unit, uint16


@dataclass
class PowerStatus:
    cc: Optional[V_unit] = None
    servo: Optional[V_unit] = None
    _flags: uint16 = 0

    def is_brick_valid(self):
        return bool(self._flags & MAV_POWER_STATUS_BRICK_VALID)

    def is_servo_valid(self):
        return bool(self._flags & MAV_POWER_STATUS_SERVO_VALID)

    def is_usb_connected(self):
        return bool(self._flags & MAV_POWER_STATUS_USB_CONNECTED)

    def is_periph_overcurrent(self):
        return bool(self._flags & MAV_POWER_STATUS_PERIPH_OVERCURRENT)

    def is_periph_hipower_overcurrent(self):
        return bool(self._flags & MAV_POWER_STATUS_PERIPH_HIPOWER_OVERCURRENT)

    def has_changed(self):
        return bool(self._flags & MAV_POWER_STATUS_CHANGED)
