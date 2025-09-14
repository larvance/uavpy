from src.uavpy import mavlink


def handle_ahrs(self: "mavlink.Mavlink", msg):
    self.dcm.drift.x = msg.omegaIx
    self.dcm.drift.y = msg.omegaIy
    self.dcm.drift.z = msg.omegaIz
    self.dcm.acceleration_weight = msg.accel_weight
    self.dcm.renormalisation = msg.renorm_val
    self.dcm.error_roll_pitch = msg.error_rp
    self.dcm.error_yaw = msg.error_yaw
