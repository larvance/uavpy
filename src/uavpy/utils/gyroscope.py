from dataclasses import dataclass

from src.uavpy.utils.units import rps_unit


@dataclass
class Gyroscope:
    x: rps_unit = 0.0
    y: rps_unit = 0.0
    z: rps_unit = 0.0
