from typing import Literal

UALBERTA_AUTOPILOT_MODE = {
    1: "MANUAL_DIRECT", "MANUAL_DIRECT": 1,
    2: "MANUAL_SCALED", "MANUAL_SCALED": 2,
    3: "AUTO_PID_ATT", "AUTO_PID_ATT": 3,
    4: "AUTO_PID_VEL", "AUTO_PID_VEL": 4,
    5: "AUTO_PID_POS", "AUTO_PID_POS": 5
}
UalbertaAutopilotMode = Literal["MANUAL_DIRECT", "MANUAL_SCALED", "AUTO_PID_ATT", "AUTO_PID_VEL", "AUTO_PID_POS"]

UALBERTA_NAV_MODE = {
    1: "AHRS_INIT", "AHRS_INIT": 1,
    2: "AHRS", "AHRS": 2,
    3: "INS_GPS_INIT", "INS_GPS_INIT": 3,
    4: "INS_GPS", "INS_GPS": 4
}
UalbertaNavMode = Literal["AHRS_INIT", "AHRS", "INS_GPS_INIT", "INS_GPS"]

UALBERTA_PILOT_MODE = {
    1: "MANUAL", "MANUAL": 1,
    2: "AUTO", "AUTO": 2,
    3: "ROTO", "ROTO": 3
}
UalbertaPilotMode = Literal["MANUAL", "AUTO", "ROTO"]
