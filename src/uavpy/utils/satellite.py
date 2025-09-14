from dataclasses import dataclass

from src.uavpy.utils.units import dB_unit, rad_unit, uint8


@dataclass
class Satellite:
    used: bool
    id: uint8
    elevation: rad_unit
    azimuth: rad_unit
    snr: dB_unit
