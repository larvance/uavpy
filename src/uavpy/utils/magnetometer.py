from dataclasses import dataclass

from src.uavpy.utils.units import Gauss_unit


@dataclass
class Magnetometer:
    x: Gauss_unit = 0.0
    y: Gauss_unit = 0.0
    z: Gauss_unit = 0.0
