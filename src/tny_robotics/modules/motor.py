from enum import IntEnum
from ..core.data_types import Float32, UInt8
from ..core.protocol import Flag, Protocol
from ..core.module import Module

class MotorId(IntEnum):
    FrontLeftHipRoll = 0
    FrontLeftHipPitch = 1
    FrontLeftKneePitch = 2
    BackLeftHipRoll = 3
    BackLeftHipPitch = 4
    BackLeftKneePitch = 5
    BackRightHipRoll = 6
    BackRightHipPitch = 7
    BackRightKneePitch = 8
    FrontRightHipRoll = 9
    FrontRightHipPitch = 10
    FrontRightKneePitch = 11
    EarLeft = 12
    EarRight = 13

class MotorCalibrationState(IntEnum):
    Uncalibrated = 0
    Calibrating = 1
    Calibrated = 2
    Error = 3

class MotorModule(Module):
    MODULE_ID = 0x06

    def __init__(self, protocol: Protocol):
        super().__init__(self.MODULE_ID, protocol)

    async def set_pwm_duty_cycle(self, motor_id: MotorId, duty_ms: float, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        await self.send_action(0x00, [UInt8(motor_id), Float32(duty_ms)], [], flags)

    async def get_pwm_duty_cycle(self, motor_id: MotorId) -> float:
        res = await self.send_action(0x01, [UInt8(motor_id)], [Float32()])
        if res is None: 
            raise Exception(f"Failed to get PWM duty cycle for motor {motor_id}")
        return float(res[0])

    async def get_calibration_state(self, motor_id: MotorId) -> MotorCalibrationState:
        res = await self.send_action(0x02, [UInt8(motor_id)], [UInt8()])
        if res is None: 
            raise Exception(f"Failed to get calibration state for motor {motor_id}")
        return MotorCalibrationState(res[0])

    async def get_calibration_data(self, motor_id: MotorId):
        raise NotImplementedError("Not implemented")

    async def set_calibration_data(self, motor_id: MotorId):
        raise NotImplementedError("Not implemented")

    async def start_calibration(self, motor_id: MotorId, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        await self.send_action(0x05, [UInt8(motor_id)], [], flags)

    async def stop_calibration(self, motor_id: MotorId, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        await self.send_action(0x06, [UInt8(motor_id)], [], flags)

    async def get_calibration_progress(self, motor_id: MotorId) -> float:
        res = await self.send_action(0x07, [UInt8(motor_id)], [Float32()])
        if res is None: 
            raise Exception(f"Failed to get calibration progress for motor {motor_id}")
        return float(res[0])