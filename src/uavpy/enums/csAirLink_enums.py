from typing import Literal

AIRLINK_AUTH_RESPONSE_TYPE = {
    0: "ERROR_LOGIN_OR_PASS", "ERROR_LOGIN_OR_PASS": 0,
    1: "AUTH_OK", "AUTH_OK": 1
}
AirlinkAuthResponseType = Literal["ERROR_LOGIN_OR_PASS", "AUTH_OK"]
