from typing import Sequence


def dist3l(a: Sequence[float], b: Sequence[float]):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5
