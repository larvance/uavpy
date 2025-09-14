from time import sleep

from src.uavpy.connections import ArduPilotSITLMavlink

drone = ArduPilotSITLMavlink()

sleep(2)

drone.arm(blocking=True)

sleep(2)

drone.takeoff(5, blocking=True)

sleep(2)

drone.disarm(blocking=True)
