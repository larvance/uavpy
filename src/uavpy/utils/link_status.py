from dataclasses import dataclass

from src.uavpy.utils.units import Bps_unit, fractional_percent, B_unit, uint32


@dataclass
class LinkStatus:
    transmit_buffer: fractional_percent = 0.0
    receive_buffer: fractional_percent = 0.0
    transmit_speed: Bps_unit = 0.0
    receive_speed: Bps_unit = 0.0
    received_invalid: B_unit = 0.0
    transmit_overflows: B_unit = 0.0
    receive_overflows: B_unit = 0.0
    messages_sent: uint32 = 0
    messages_received: uint32 = 0
    messages_lost: uint32 = 0
