from dataclasses import field, dataclass
from typing import Optional, List

from src.uavpy.enums.common_enums import GpsFixType
from src.uavpy.utils.satellite import Satellite
from src.uavpy.utils.units import rad_unit, mps_unit, m_unit


@dataclass
class RawGpsStatus:
    fix_type: GpsFixType = "NO_GPS"
    lat: float = 0.0
    lon: float = 0.0
    alt: float = 0.0
    horizontal_dilution: Optional[float] = None
    vertical_dilution: Optional[float] = None
    velocity: Optional[mps_unit] = None
    cog: Optional[rad_unit] = None
    satellite_count: int = 0
    satellites: List[Satellite] = field(default_factory=list)
    alt_ellipsoid: Optional[m_unit] = None
    h_acc: Optional[m_unit] = None
    v_acc: Optional[m_unit] = None
    vel_acc: Optional[mps_unit] = None
    hdg_acc: Optional[rad_unit] = None
    yaw: Optional[rad_unit] = None
