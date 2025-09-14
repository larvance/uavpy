from dataclasses import dataclass
from typing import Optional

from src.uavpy.utils.units import rps_unit, float32, rad_unit, m_unit


@dataclass
class DCMDrift:
    x: Optional[rps_unit] = None
    y: Optional[rps_unit] = None
    z: Optional[rps_unit] = None


@dataclass
class DCM:
    lat: Optional[rad_unit] = None
    lon: Optional[rad_unit] = None
    alt: Optional[m_unit] = None
    roll: Optional[rad_unit] = None
    pitch: Optional[rad_unit] = None
    yaw: Optional[rad_unit] = None
    drift = DCMDrift()
    acceleration_weight: Optional[float32] = None
    renormalisation: Optional[float32] = None
    error_roll_pitch: Optional[float32] = None
    error_yaw: Optional[float32] = None
