from typing import Literal

ICAROUS_TRACK_BAND_TYPES = {
    0: "NONE", "NONE": 0,
    1: "NEAR", "NEAR": 1,
    2: "RECOVERY", "RECOVERY": 2
}
IcarousTrackBandTypes = Literal["NONE", "NEAR", "RECOVERY"]

ICAROUS_FMS_STATE = {
    0: "IDLE", "IDLE": 0,
    1: "TAKEOFF", "TAKEOFF": 1,
    2: "CLIMB", "CLIMB": 2,
    3: "CRUISE", "CRUISE": 3,
    4: "APPROACH", "APPROACH": 4,
    5: "LAND", "LAND": 5
}
IcarousFmsState = Literal["IDLE", "TAKEOFF", "CLIMB", "CRUISE", "APPROACH", "LAND"]
