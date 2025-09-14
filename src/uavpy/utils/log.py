import os

os.environ["LIBCAMERA_LOG_LEVELS"] = "*:2"


class DroneException(Exception):
    pass


debug_enabled = True


def debug(*msg, **kw):
    if debug_enabled:
        print(*msg, **kw)