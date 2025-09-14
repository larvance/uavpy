from src.uavpy import mavlink
from src.uavpy.enums.common_enums import MAV_PARAM_TYPE
from src.uavpy.utils.units import float32, uint16


def handle_param_value(self: "mavlink.Mavlink", msg):
    param_id: str = msg.param_id
    param_value: float32 = msg.param_value
    param_type = MAV_PARAM_TYPE[msg.param_type]
    param_count: uint16 = msg.param_count
    # param_index: uint16 = msg.param_index

    self.params[param_id] = param_value, param_type
    self.total_params = param_count
