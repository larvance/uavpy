from dataclasses import dataclass
from typing import Tuple


@dataclass
class Vec3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    @classmethod
    def __class_getitem__(cls, item):
        return Tuple[cls, cls, cls]
