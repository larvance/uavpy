from typing import Literal

GSM_LINK_TYPE = {
    0: "NONE", "NONE": 0,
    1: "UNKNOWN", "UNKNOWN": 1,
    2: "2G", "2G": 2,
    3: "3G", "3G": 3,
    4: "4G", "4G": 4
}
GsmLinkType = Literal["NONE", "UNKNOWN", "2G", "3G", "4G"]

GSM_MODEM_TYPE = {
    0: "UNKNOWN", "UNKNOWN": 0,
    1: "HUAWEI_E3372", "HUAWEI_E3372": 1
}
GsmModemType = Literal["UNKNOWN", "HUAWEI_E3372"]
