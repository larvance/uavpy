from src.uavpy import mavlink
from src.uavpy.enums.extra_enums import CONTROL_ACKNOWLEDGEMENT
from src.uavpy.utils.log import DroneException
from src.uavpy.utils.units import uint8


def handle_operator_control_ack(self: "mavlink.Mavlink", msg):
    gcs_system_id: uint8 = msg.gcs_system_id
    control_request: uint8 = msg.control_request
    if gcs_system_id != self.connection.source_system:
        return
    if CONTROL_ACKNOWLEDGEMENT[msg.ack] == "UNSUPPORTED_ENCRYPTION":
        raise DroneException("MAVLink passkey encryption is not supported.")
    self.is_in_control = not control_request
