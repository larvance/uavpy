from src.uavpy import mavlink
from src.uavpy.enums.common_enums import MAV_SEVERITY
from src.uavpy.utils.log import debug


def handle_status_text(self: "mavlink.Mavlink", msg):
    severity = MAV_SEVERITY[msg.severity]
    text = msg.text
    id = msg.id
    chunk_seq = msg.chunk_seq
    debug(f"STATUS_TEXT: {severity} - {text} (id: {id}, chunk_seq: {chunk_seq})")
