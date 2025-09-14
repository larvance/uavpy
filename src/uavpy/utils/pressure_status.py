from dataclasses import dataclass
from typing import Optional

from src.uavpy.utils.units import degC_unit, Pascal_unit


@dataclass
class PressureStatus:
    absolute: Optional[Pascal_unit] = None
    differential: Optional[Pascal_unit] = None
    temperature: Optional[degC_unit] = None
    differential_temperature: Optional[degC_unit] = None
