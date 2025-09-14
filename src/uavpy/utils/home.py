from dataclasses import dataclass


@dataclass
class HomeApproach:
    north: float = 0.0
    east: float = 0.0
    up: float = 0.0


@dataclass
class Home:
    lat: float = 0.0
    lon: float = 0.0
    alt: float = 0.0
    north: float = 0.0
    east: float = 0.0
    up: float = 0.0
    approach = HomeApproach()
