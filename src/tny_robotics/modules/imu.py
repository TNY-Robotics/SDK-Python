from enum import IntEnum
from typing import TypedDict
from ..core.data_types import Float32, UInt8
from ..core.protocol import Flag, Protocol
from ..core.module import Module

class IMUCalibrationState(IntEnum):
    Uncalibrated = 0
    Calibrating = 1
    Calibrated = 2
    Error = 3

class Vector3D(TypedDict):
    x: float
    y: float
    z: float

class AccelerationData(TypedDict):
    x_g: float
    y_g: float
    z_g: float

class AngularVelocityData(TypedDict):
    x_rads: float
    y_rads: float
    z_rads: float

class OrientationData(TypedDict):
    x_rad: float
    y_rad: float
    z_rad: float

class IMUModule(Module):
    MODULE_ID = 0x07

    def __init__(self, protocol: Protocol):
        super().__init__(self.MODULE_ID, protocol)

    async def get_acceleration(self) -> AccelerationData:
        res = await self.send_action(0x00, [], [Float32(), Float32(), Float32()])
        if res is None: raise Exception("Failed to get IMU acceleration")
        return {
            'x_g': res[0],
            'y_g': res[1],
            'z_g': res[2]
        }

    async def get_angular_velocity(self) -> AngularVelocityData:
        res = await self.send_action(0x01, [], [Float32(), Float32(), Float32()])
        if res is None: raise Exception("Failed to get IMU angular velocity")
        return {
            'x_rads': res[0],
            'y_rads': res[1],
            'z_rads': res[2]
        }

    async def get_down_vector(self) -> Vector3D:
        res = await self.send_action(0x02, [], [Float32(), Float32(), Float32()])
        if res is None: raise Exception("Failed to get IMU down vector")
        return {
            'x': res[0],
            'y': res[1],
            'z': res[2]
        }

    async def get_orientation(self) -> OrientationData:
        res = await self.send_action(0x03, [], [Float32(), Float32(), Float32()])
        if res is None: raise Exception("Failed to get IMU orientation")
        return {
            'x_rad': res[0],
            'y_rad': res[1],
            'z_rad': res[2]
        }

    async def get_calibration_state(self) -> IMUCalibrationState:
        res = await self.send_action(0x04, [], [UInt8()])
        if res is None: raise Exception("Failed to get IMU calibration state")
        return IMUCalibrationState(res[0])

    async def get_calibration_data(self):
        raise NotImplementedError("Not implemented")

    async def set_calibration_data(self):
        raise NotImplementedError("Not implemented")

    async def start_calibration(self, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        await self.send_action(0x07, [], [], flags)

    async def stop_calibration(self, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        await self.send_action(0x08, [], [], flags)

    async def get_calibration_progress(self) -> float:
        res = await self.send_action(0x09, [], [Float32()])
        if res is None: raise Exception("Failed to get IMU calibration progress")
        return float(res[0])