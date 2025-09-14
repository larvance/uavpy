from dataclasses import dataclass

from src.uavpy.utils.units import mps_unit, rps_unit


@dataclass
class Velocity:
    north: mps_unit = 0.0
    east: mps_unit = 0.0
    up: mps_unit = 0.0
    yaw: rps_unit = 0.0
    pitch: rps_unit = 0.0
    roll: rps_unit = 0.0