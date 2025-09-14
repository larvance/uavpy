from src.uavpy import mavlink


def handle_ping(self: "mavlink.Mavlink", msg):
    if msg.target_system == 0 and msg.target_component == 0:
        self.connection.mav.ping_send(
            time_usec=int(msg.time_usec),
            seq=msg.seq,
            target_system=msg.target_system,
            target_component=msg.target_component
        )
