from scipy.spatial.transform import Rotation

from src.uavpy import mavlink


def handle_attitude_quaternion(self: "mavlink.Mavlink", msg):
    self.since_boot = msg.time_boot_ms / 1e3
    q = [msg.q1, msg.q2, msg.q3, msg.q4]
    if hasattr(msg, "repr_offset_q") and msg.repr_offset_q != [0, 0, 0, 0]:
        offset_q = msg.repr_offset_q
        r_orig = Rotation.from_quat([q[1], q[2], q[3], q[0]])  # x,y,z,w
        r_offset = Rotation.from_quat([offset_q[1], offset_q[2], offset_q[3], offset_q[0]])
        r = r_orig * r_offset
    else:
        r = Rotation.from_quat([q[1], q[2], q[3], q[0]])

    self.roll, self.pitch, self.yaw = r.as_euler('xyz', degrees=False)
    self.velocity.roll = msg.rollspeed
    self.velocity.pitch = msg.pitchspeed
    self.velocity.yaw = msg.yawspeed
