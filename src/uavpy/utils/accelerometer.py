from dataclasses import dataclass

from src.uavpy.utils.units import mps2_unit


@dataclass
class Accelerometer:
    x: mps2_unit = 0.0
    y: mps2_unit = 0.0
    z: mps2_unit = 0.0
