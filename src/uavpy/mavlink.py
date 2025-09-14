import threading
from asyncio import Future
from collections import defaultdict
from pprint import pformat
from time import time
from typing import List, Optional, Union, Set, Callable, DefaultDict, Dict

import serial
from pymavlink import mavutil
from pymavlink.mavutil import mavserial

from src.uavpy.enums.commands import MAV_CMD_COMPONENT_ARM_DISARM, MAV_CMD_NAV_TAKEOFF
from src.uavpy.enums.common_enums import MAV_PARAM_TYPE, MAV_MODE, \
    MavParamType, MAV_RESULT
from src.uavpy.enums.extra_enums import CONTROL_ACKNOWLEDGEMENT, CommandAckResponse
from src.uavpy.enums.minimal_enums import MavType, MavState
from src.uavpy.messages._000_HEARTBEAT import handle_heartbeat
from src.uavpy.messages._001_SYS_STATUS import handle_sys_status
from src.uavpy.messages._002_SYSTEM_TIME import handle_system_time
from src.uavpy.messages._004_PING import handle_ping
from src.uavpy.messages._006_CHANGE_OPERATOR_CONTROL_ACK import handle_operator_control_ack
from src.uavpy.messages._008_LINK_NODE_STATUS import handle_link_node_status
from src.uavpy.messages._022_PARAM_VALUE import handle_param_value
from src.uavpy.messages._024_GPS_RAW_INT import handle_gps_raw_int
from src.uavpy.messages._025_GPS_STATUS import handle_gps_status
from src.uavpy.messages._026_SCALED_IMU import handle_scaled_imu
from src.uavpy.messages._029_SCALED_PRESSURE import handle_scaled_pressure
from src.uavpy.messages._030_ATTITUDE import handle_attitude
from src.uavpy.messages._031_ATTITUDE_QUATERNION import handle_attitude_quaternion
from src.uavpy.messages._032_LOCAL_POSITION_NED import handle_local_position_ned
from src.uavpy.messages._033_GLOBAL_POSITION_INT import handle_global_position_int
from src.uavpy.messages._074_VFR_HUD import handle_vfr_hud
from src.uavpy.messages._077_COMMAND_ACK import handle_command_ack
from src.uavpy.messages._125_POWER_STATUS import handle_power_status
from src.uavpy.messages._163_AHRS import handle_ahrs
from src.uavpy.messages._178_AHRS2 import handle_ahrs2
from src.uavpy.messages._242_HOME_POSITION import handle_home_position
from src.uavpy.messages._253_STATUS_TEXT import handle_status_text
from src.uavpy.utils.accelerometer import Accelerometer
from src.uavpy.utils.dcm import DCM
from src.uavpy.utils.gyroscope import Gyroscope
from src.uavpy.utils.home import Home
from src.uavpy.utils.link_status import LinkStatus
from src.uavpy.utils.log import DroneException, debug
from src.uavpy.utils.magnetometer import Magnetometer
from src.uavpy.utils.onboard_control_sensors import OnboardControlSensors
from src.uavpy.utils.power_status import PowerStatus
from src.uavpy.utils.pressure_status import PressureStatus
from src.uavpy.utils.raw_gps_status import RawGpsStatus
from src.uavpy.utils.timeout import timeout_future
from src.uavpy.utils.units import fractional_percent, uint32, rad_unit, degC_unit, \
    timestamp, s_unit, uint8, V_unit, A_unit, uint16, m_unit, float32, mps_unit
from src.uavpy.utils.velocity import Velocity


class Mavlink:
    def __init__(self, connection_strings: Union[List[str], str] = None, baud_rates: Union[List[str], str] = None,
                 timeout=5):
        if connection_strings is None or baud_rates is None:
            raise DroneException("Connection strings and baud rates must be specified.")

        for connection_string in connection_strings:
            for baud_rate in baud_rates or [115200]:
                try:
                    self.connection_string = connection_string
                    self.baud_rate = baud_rate
                    debug(f"Trying connection {self.connection_string} at {baud_rate} baud...")
                    self.connection: mavserial = mavutil.mavlink_connection(connection_string, baud=baud_rate)
                    beat = self.connection.wait_heartbeat(timeout=timeout)
                    if beat:
                        break
                except serial.serialutil.SerialException:
                    continue
            else:
                continue
            break
        else:
            raise DroneException(
                f"Failed to connect to any specified connection strings: {connection_strings} with bauds: {baud_rates}")

        self.control_passkey = b"MY_PASSKEY"

        # In most packets:
        self.time_unix: Optional[timestamp] = None
        self.since_boot: Optional[s_unit] = None

        # HEARTBEAT
        self.last_heartbeat: Optional[timestamp] = None
        self.autopilot: Optional[str] = None
        self.type: Optional[MavType] = None
        self.base_mode: Optional[uint8] = None
        self.custom_mode: Optional[uint32] = None
        self.system_status: Optional[MavState] = None
        self.mavlink_version: Optional[uint8] = None
        self.mode: str = "UNKNOWN"
        self.is_armed: bool = False

        # SYS_STATUS
        self.onboard_control_sensors = OnboardControlSensors()
        self.load: Optional[fractional_percent] = None
        self.voltage_battery: Optional[V_unit] = None
        self.current_battery: Optional[A_unit] = None
        self.battery_remaining: Optional[fractional_percent] = None  # if not sent, None
        self.communication_drop_rate: Optional[fractional_percent] = None
        self.communication_errors: Optional[uint16] = None
        self.errors_count1: Optional[uint16] = None
        self.errors_count2: Optional[uint16] = None
        self.errors_count3: Optional[uint16] = None
        self.errors_count4: Optional[uint16] = None

        # LINK_NODE_STATUS
        self.link_status = LinkStatus()

        # CHANGE_OPERATOR_CONTROL_ACK
        self.is_in_control: bool = False

        # GPS_RAW_INT, GPS_STATUS
        self.gps = RawGpsStatus()
        self.accelerometer = Accelerometer()
        self.gyroscope = Gyroscope()
        self.magnetometer = Magnetometer()
        self.dcm = DCM()
        self.temperature: Optional[degC_unit] = None

        # ATTITUDE, ATTITUDE_QUATERNION
        self.oll: Optional[rad_unit] = None
        self.pitch: Optional[rad_unit] = None
        self.yaw: Optional[rad_unit] = None

        # ATTITUDE, ATTITUDE_QUATERNION, LOCAL_POSITION_NED
        self.velocity = Velocity()

        # LOCAL_POSITION_NED
        self.north: Optional[m_unit] = None
        self.east: Optional[m_unit] = None
        self.up: Optional[m_unit] = None

        # GLOBAL_POSITION_INT
        self.lat: Optional[rad_unit] = None
        self.lon: Optional[rad_unit] = None
        self.alt: Optional[m_unit] = None
        self.relative_alt: Optional[m_unit] = None

        # SCALED_PRESSURE
        self.pressure = PressureStatus()

        # HOME_POSITION
        self.home = Home()

        # VFR_HUD
        self.airspeed: Optional[mps_unit] = None
        self.groundspeed: Optional[mps_unit] = None
        self.heading: Optional[rad_unit] = None
        self.throttle: Optional[fractional_percent] = None
        self.climb: Optional[mps_unit] = None

        # POWER_STATUS
        self.power_status = PowerStatus()

        self._msg_handlers = {
            "HEARTBEAT": handle_heartbeat,  # (0)
            "SYS_STATUS": handle_sys_status,  # (1)
            "SYSTEM_TIME": handle_system_time,  # (2)
            "PING": handle_ping,  # (4) DEPRECATED since 2011-08: Replaced by TIMESYNC
            "CHANGE_OPERATOR_CONTROL_ACK": handle_operator_control_ack,  # (6)
            "LINK_NODE_STATUS": handle_link_node_status,  # (8) WIP
            "PARAM_VALUE": handle_param_value,  # (22)
            "GPS_RAW_INT": handle_gps_raw_int,  # (24)
            "GPS_STATUS": handle_gps_status,  # (25)
            "SCALED_IMU": handle_scaled_imu,  # (26)
            "SCALED_PRESSURE": handle_scaled_pressure,  # (29)
            "ATTITUDE": handle_attitude,  # (30)
            "ATTITUDE_QUATERNION": handle_attitude_quaternion,  # (31)
            "LOCAL_POSITION_NED": handle_local_position_ned,  # (32)
            "GLOBAL_POSITION_INT": handle_global_position_int,  # (33)
            "VFR_HUD": handle_vfr_hud,  # (74)
            "COMMAND_ACK": handle_command_ack,  # (77)
            "POWER_STATUS": handle_power_status,  # (125)
            "AHRS": handle_ahrs,  # (163)
            "AHRS2": handle_ahrs2,  # (178)
            "HOME_POSITION": handle_home_position,  # (242)
            "STATUS_TEXT": handle_status_text,  # (253)
        }

        self._msg_requests: DefaultDict[str, List[Callable]] = defaultdict(list)

        self.params = {}
        self.total_params: Optional[int] = None
        self.unhandled_msgs: Set[str] = set()

        self.process_msg(beat)

        self._running = threading.Event()
        self._thread = None
        self._start_loop()

    def _start_loop(self):
        if self._thread and self._thread.is_alive():
            return

        self._running.set()
        self._thread = threading.Thread(target=self._message_loop, daemon=True)
        self._thread.start()

    def _stop_loop(self):
        self._running.clear()
        if self._thread:
            self._thread.join()
            self._thread = None

    def _message_loop(self):
        while self._running.is_set():
            try:
                self.process_msg(self.connection.recv_msg())
            except Exception as e:
                debug(f"Error in message loop: {e}")

    def process_msg(self, msg):
        if msg is None:
            return
        type = msg.get_type()
        if type in self._msg_handlers:
            self._msg_handlers[type](self, msg)
        else:
            if type not in self.unhandled_msgs:
                debug(f"Unhandled message type: {type}")
            self.unhandled_msgs.add(type)
        self._msg_requests[type] = list(filter(lambda cb: not cb(msg), self._msg_requests[type]))

    def wait_msg(self, msg_type: str, condition: Callable = None, then: Callable = None, blocking=False,
                 timeout: s_unit = None) -> Future:
        if blocking:
            self._stop_loop()
            t = time()
            while timeout is None or t + timeout > time():
                msg = self.connection.recv_msg()
                self.process_msg(msg)
                if msg and msg.get_type() == msg_type and (not condition or condition(msg)):
                    self._start_loop()
                    return then(msg) if then else None
            self._start_loop()
            return None

        def rec(msg):
            if not condition or condition(msg):
                fut.set_result(then(msg) if then else None)
                return True
            return False

        self._msg_requests[msg_type].append(rec)
        fut = timeout_future(timeout)
        return fut

    def __control_request_send(self, control_request, version=0):
        self.connection.mav.change_operator_control_send(
            self.connection.target_system,
            control_request,
            version,
            self.control_passkey
        )

    def takeover(self, blocking=False, timeout: s_unit = None, release=False) -> Optional[Future]:
        if len(self.control_passkey) > 25:
            raise DroneException("Passkey too long, must be 25 bytes or less.")
        self.control_passkey += b'\0' * (25 - len(self.control_passkey))
        control_request = 1 if release else 0

        self.__control_request_send(control_request)

        def condition(msg):
            if msg.control_request != control_request or msg.gcs_system_id != self.connection.source_system:
                return False
            ack = CONTROL_ACKNOWLEDGEMENT[msg.ack] in ("ACCEPTED", "ALREADY_UNDER_CONTROL")
            if not ack:
                return False
            return True

        return self.wait_msg(
            "CHANGE_OPERATOR_CONTROL_ACK",
            condition=condition,
            blocking=blocking,
            timeout=timeout
        )

    def release_control(self, blocking=False, timeout: s_unit = None) -> Optional[Future]:
        return self.takeover(blocking, timeout, release=True)

    def set_manual(self, blocking=False, timeout: s_unit = None) -> Future:
        self.connection.set_mode_manual()  # todo: do we get an ACK back?
        return self.wait_msg(
            "HEARTBEAT", condition=lambda msg: self.mode == "MANUAL", blocking=blocking, timeout=timeout
        )

    def set_guided(self, blocking=False, timeout: s_unit = None):
        self.connection.set_mode(MAV_MODE.GUIDED_ARMED if self.is_armed else MAV_MODE.GUIDED_DISARMED)
        return self.wait_msg(
            "HEARTBEAT", condition=lambda msg: self.mode == "GUIDED", blocking=blocking, timeout=timeout
        )

    def set_auto(self, blocking=False, timeout: s_unit = None):
        self.connection.set_mode_auto()
        return self.wait_msg(
            "HEARTBEAT", condition=lambda msg: self.mode == "AUTO", blocking=blocking, timeout=timeout
        )

    def set_stabilize(self, blocking=False, timeout: s_unit = None):
        self.connection.set_mode(MAV_MODE.STABILIZE_ARMED if self.is_armed else MAV_MODE.STABILIZE_DISARMED)
        return self.wait_msg(
            "HEARTBEAT", condition=lambda msg: self.mode == "STABILIZE", blocking=blocking, timeout=timeout
        )

    def arm(self, blocking=False, timeout: s_unit = None) -> Union[CommandAckResponse, Future[CommandAckResponse]]:
        self.connection.arducopter_arm()

        def then(msg):
            res = MAV_RESULT[msg.result]
            if res == "ACCEPTED":
                self.is_armed = True
                return True
            if res == "IN_PROGRESS":
                return msg.progress / 1e2 if msg.progress != 0xff else 0.0
            return res

        return self.wait_msg(
            "COMMAND_ACK",
            condition=lambda msg: msg.command == MAV_CMD_COMPONENT_ARM_DISARM,
            then=then,
            blocking=blocking,
            timeout=timeout
        )

    def disarm(self, blocking=False, timeout: s_unit = None) -> Union[CommandAckResponse, Future[CommandAckResponse]]:
        self.connection.arducopter_disarm()

        def then(msg):
            res = MAV_RESULT[msg.result]
            if res == "ACCEPTED":
                self.is_armed = False
                return True
            if res == "IN_PROGRESS":
                return msg.progress / 1e2 if msg.progress != 0xff else 0.0
            return res

        return self.wait_msg(
            "COMMAND_ACK",
            condition=lambda msg: msg.command == MAV_CMD_COMPONENT_ARM_DISARM,
            then=then,
            blocking=blocking,
            timeout=timeout
        )

    def get_param(self, param_name: str, blocking=False, timeout: s_unit = None) -> Union[float32, Future[float32]]:
        if len(param_name) > 16:
            raise DroneException("Parameter name too long, must be 16 characters or less.")
        param_name_str = param_name
        param_name = param_name.encode("utf-8")
        param_name += b"\0" * (16 - len(param_name))

        self.connection.mav.param_request_read_send(
            self.connection.target_system,
            self.connection.target_component,
            param_name,
            -1
        )

        return self.wait_msg(
            "PARAM_VALUE",
            condition=lambda msg: msg.param_id == param_name_str,
            then=lambda msg: msg.param_value,
            blocking=blocking,
            timeout=timeout
        )

    def get_all_params(self, blocking=False, timeout: s_unit = None) \
            -> Union[Dict[str, float], Future[Dict[str, float]]]:
        params = set()

        self.connection.mav.param_request_list_send(
            self.connection.target_system,
            self.connection.target_component
        )

        def condition(msg):
            params.add(msg.param_id)
            return len(params) >= self.total_params if self.total_params is not None else False

        return self.wait_msg(
            "PARAM_VALUE",
            condition=condition,
            then=lambda _: self.params,
            blocking=blocking,
            timeout=timeout
        )

    def set_param(self, param_name: str, param_value: Union[int, float],
                  param_type: MavParamType = MAV_PARAM_TYPE["REAL32"], blocking=False, timeout: s_unit = None):
        if len(param_name) > 16:
            raise DroneException("Parameter name too long, must be 16 characters or less.")
        param_name_str = param_name
        param_name = param_name.encode("utf-8")
        param_name += b"\0" * (16 - len(param_name))
        param_value = float(param_value)

        self.connection.mav.param_set_send(
            self.connection.target_system,
            self.connection.target_component,
            param_name,
            float(param_value),
            int(param_type)
        )

        return self.wait_msg(
            "PARAM_VALUE",
            condition=lambda msg: msg.param_id == param_name_str,
            then=lambda msg: msg.param_value == param_value and MAV_PARAM_TYPE[msg.param_type] == param_type,
            blocking=blocking,
            timeout=timeout
        )

    def set_home(self, lat: float, lon: float, alt: float, blocking=False, timeout: s_unit = None) -> Optional[Future]:
        ilat = int(lat * 1e7)
        ilon = int(lon * 1e7)
        ialt = int(alt * 1e3)
        self.connection.mav.set_home_position_send(
            self.connection.target_system,
            ilat, ilon, ialt,
            0.0, 0.0, 0.0,
            [1.0, 0.0, 0.0, 0.0],
            0.0, 0.0, 0.0
        )

        return self.wait_msg(
            "HOME_POSITION",
            condition=lambda msg: msg.latitude == ilat and msg.longitude == ilon and msg.altitude == ialt,
            blocking=blocking,
            timeout=timeout
        )

    def takeoff(self, target_relative_alt: m_unit, blocking=False, timeout: s_unit = None) -> Optional[Future]:
        if not self.is_armed:
            raise DroneException("Cannot takeoff: vehicle is not armed.")
        if self.mode != "GUIDED":
            raise DroneException("Cannot takeoff: vehicle is not in GUIDED mode.")
        if self.alt is None:
            raise DroneException("Cannot takeoff: current altitude unknown.")
        if self.relative_alt is None:
            raise DroneException("Cannot takeoff: current relative altitude unknown.")
        if self.home.alt is None:
            raise DroneException("Cannot takeoff: home altitude unknown.")

        self.connection.mav.command_long_send(
            self.connection.target_system,
            self.connection.target_component,
            22,  # MAV_CMD_NAV_TAKEOFF
            0,  # confirmation
            0, 0, 0, 0,  # param1-4 (takeoff pitch, empty)
            0, 0,  # param5-6 (latitude, longitude - empty)
            target_relative_alt  # param7 (altitude)
        )

        return self.wait_msg(
            "COMMAND_ACK",
            condition=lambda msg: msg.command == MAV_CMD_NAV_TAKEOFF and MAV_RESULT[msg.result] == "ACCEPTED",
            blocking=blocking,
            timeout=timeout
        )

    def __repr__(self):
        props = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return f"{self.__class__.__name__}({{\n {pformat(props, indent=2)[1:-1]}\n}})"
