from dataclasses import dataclass

from pymavlink.dialects.v10.common import MAV_SYS_STATUS_SENSOR_3D_GYRO, MAV_SYS_STATUS_SENSOR_3D_ACCEL, \
    MAV_SYS_STATUS_SENSOR_3D_MAG, MAV_SYS_STATUS_SENSOR_ABSOLUTE_PRESSURE, MAV_SYS_STATUS_SENSOR_DIFFERENTIAL_PRESSURE, \
    MAV_SYS_STATUS_SENSOR_GPS, MAV_SYS_STATUS_SENSOR_OPTICAL_FLOW, MAV_SYS_STATUS_SENSOR_VISION_POSITION, \
    MAV_SYS_STATUS_SENSOR_LASER_POSITION, MAV_SYS_STATUS_SENSOR_EXTERNAL_GROUND_TRUTH, \
    MAV_SYS_STATUS_SENSOR_ANGULAR_RATE_CONTROL, MAV_SYS_STATUS_SENSOR_ATTITUDE_STABILIZATION, \
    MAV_SYS_STATUS_SENSOR_YAW_POSITION, MAV_SYS_STATUS_SENSOR_Z_ALTITUDE_CONTROL, \
    MAV_SYS_STATUS_SENSOR_XY_POSITION_CONTROL, MAV_SYS_STATUS_SENSOR_MOTOR_OUTPUTS, MAV_SYS_STATUS_SENSOR_RC_RECEIVER, \
    MAV_SYS_STATUS_SENSOR_3D_GYRO2, MAV_SYS_STATUS_SENSOR_3D_ACCEL2, MAV_SYS_STATUS_SENSOR_3D_MAG2, \
    MAV_SYS_STATUS_GEOFENCE, MAV_SYS_STATUS_AHRS, MAV_SYS_STATUS_TERRAIN, MAV_SYS_STATUS_REVERSE_MOTOR, \
    MAV_SYS_STATUS_LOGGING, MAV_SYS_STATUS_SENSOR_BATTERY, MAV_SYS_STATUS_SENSOR_PROXIMITY, \
    MAV_SYS_STATUS_SENSOR_SATCOM, MAV_SYS_STATUS_PREARM_CHECK, MAV_SYS_STATUS_OBSTACLE_AVOIDANCE, \
    MAV_SYS_STATUS_SENSOR_PROPULSION


@dataclass
class SysStatusSensor:
    _flags: int

    def is_sensor_3d_gyro(self): return self._flags & MAV_SYS_STATUS_SENSOR_3D_GYRO

    def is_sensor_3d_accel(self): return self._flags & MAV_SYS_STATUS_SENSOR_3D_ACCEL

    def is_sensor_3d_mag(self): return self._flags & MAV_SYS_STATUS_SENSOR_3D_MAG

    def is_sensor_absolute_pressure(self): return self._flags & MAV_SYS_STATUS_SENSOR_ABSOLUTE_PRESSURE

    def is_sensor_differential_pressure(self): return self._flags & MAV_SYS_STATUS_SENSOR_DIFFERENTIAL_PRESSURE

    def is_sensor_gps(self): return self._flags & MAV_SYS_STATUS_SENSOR_GPS

    def is_sensor_optical_flow(self): return self._flags & MAV_SYS_STATUS_SENSOR_OPTICAL_FLOW

    def is_sensor_vision_position(self): return self._flags & MAV_SYS_STATUS_SENSOR_VISION_POSITION

    def is_sensor_laser_position(self): return self._flags & MAV_SYS_STATUS_SENSOR_LASER_POSITION

    def is_sensor_external_ground_truth(self): return self._flags & MAV_SYS_STATUS_SENSOR_EXTERNAL_GROUND_TRUTH

    def is_sensor_angular_rate_control(self): return self._flags & MAV_SYS_STATUS_SENSOR_ANGULAR_RATE_CONTROL

    def is_sensor_attitude_stabilization(self): return self._flags & MAV_SYS_STATUS_SENSOR_ATTITUDE_STABILIZATION

    def is_sensor_yaw_position(self): return self._flags & MAV_SYS_STATUS_SENSOR_YAW_POSITION

    def is_sensor_z_altitude_control(self): return self._flags & MAV_SYS_STATUS_SENSOR_Z_ALTITUDE_CONTROL

    def is_sensor_xy_position_control(self): return self._flags & MAV_SYS_STATUS_SENSOR_XY_POSITION_CONTROL

    def is_sensor_motor_outputs(self): return self._flags & MAV_SYS_STATUS_SENSOR_MOTOR_OUTPUTS

    def is_sensor_rc_receiver(self): return self._flags & MAV_SYS_STATUS_SENSOR_RC_RECEIVER

    def is_sensor_3d_gyro2(self): return self._flags & MAV_SYS_STATUS_SENSOR_3D_GYRO2

    def is_sensor_3d_accel2(self): return self._flags & MAV_SYS_STATUS_SENSOR_3D_ACCEL2

    def is_sensor_3d_mag2(self): return self._flags & MAV_SYS_STATUS_SENSOR_3D_MAG2

    def is_geofence(self): return self._flags & MAV_SYS_STATUS_GEOFENCE

    def is_ahrs(self): return self._flags & MAV_SYS_STATUS_AHRS

    def is_terrain(self): return self._flags & MAV_SYS_STATUS_TERRAIN

    def is_reverse_motor(self): return self._flags & MAV_SYS_STATUS_REVERSE_MOTOR

    def is_logging(self): return self._flags & MAV_SYS_STATUS_LOGGING

    def is_sensor_battery(self): return self._flags & MAV_SYS_STATUS_SENSOR_BATTERY

    def is_sensor_proximity(self): return self._flags & MAV_SYS_STATUS_SENSOR_PROXIMITY

    def is_sensor_satcom(self): return self._flags & MAV_SYS_STATUS_SENSOR_SATCOM

    def is_prearm_check(self): return self._flags & MAV_SYS_STATUS_PREARM_CHECK

    def is_obstacle_avoidance(self): return self._flags & MAV_SYS_STATUS_OBSTACLE_AVOIDANCE

    def is_sensor_propulsion(self): return self._flags & MAV_SYS_STATUS_SENSOR_PROPULSION

    # def is_extension_used(self): return self._flags & MAV_SYS_STATUS_EXTENSION_USED
