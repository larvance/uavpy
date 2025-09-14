from src.uavpy import mavlink
from src.uavpy.enums.commands_enum import MAV_COMMAND
from src.uavpy.enums.common_enums import MAV_RESULT
from src.uavpy.utils.units import int32, uint8


def handle_command_ack(self: "mavlink.Mavlink", msg):
    command = MAV_COMMAND[msg.command]
    result = MAV_RESULT[msg.result]
    progress = msg.progress / 1e2 if msg.progress != 0xff and result == "IN_PROGRESS" else None
    result_param2: int32 = msg.result_param2
    target_system: uint8 = msg.target_system
    target_component: uint8 = msg.target_component
