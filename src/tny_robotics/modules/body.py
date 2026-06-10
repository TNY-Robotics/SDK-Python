from enum import IntFlag
from typing import TypedDict
from ..core.data_types import Float32, UInt16
from ..core.protocol import Flag, Protocol
from ..core.module import Module
from .joint import JointId

class BodyJointFlag(IntFlag):
    FrontLeftHipRoll = 1 << JointId.FrontLeftHipRoll
    FrontLeftHipPitch = 1 << JointId.FrontLeftHipPitch
    FrontLeftKneePitch = 1 << JointId.FrontLeftKneePitch
    BackLeftHipRoll = 1 << JointId.BackLeftHipRoll
    BackLeftHipPitch = 1 << JointId.BackLeftHipPitch
    BackLeftKneePitch = 1 << JointId.BackLeftKneePitch
    BackRightHipRoll = 1 << JointId.BackRightHipRoll
    BackRightHipPitch = 1 << JointId.BackRightHipPitch
    BackRightKneePitch = 1 << JointId.BackRightKneePitch
    FrontRightHipRoll = 1 << JointId.FrontRightHipRoll
    FrontRightHipPitch = 1 << JointId.FrontRightHipPitch
    FrontRightKneePitch = 1 << JointId.FrontRightKneePitch
    EarLeft = 1 << JointId.EarLeft
    EarRight = 1 << JointId.EarRight
    All = (1 << len(JointId)) - 1
    Zero = 0

class VelocityTarget(TypedDict):
    x_ms: float
    y_ms: float
    z_rads: float

class PostureTarget(TypedDict):
    pos_x_m: float
    pos_y_m: float
    pos_z_m: float
    rot_x_rad: float
    rot_y_rad: float
    rot_z_rad: float

class BodyModule(Module):
    MODULE_ID = 0x03

    def __init__(self, protocol: Protocol):
        super().__init__(self.MODULE_ID, protocol)

    async def set_enabled(self, joint_flag: BodyJointFlag, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        await self.send_action(0x00, [UInt16(joint_flag)], [], flags)

    async def get_enabled(self) -> BodyJointFlag:
        res = await self.send_action(0x01, [], [UInt16()])
        return BodyJointFlag(res[0]) if res else BodyJointFlag(0)

    async def set_velocity(self, x_ms: float, y_ms: float, z_rads: float, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        await self.send_action(0x02, [Float32(x_ms), Float32(y_ms), Float32(z_rads)], [], flags)

    async def get_target_velocity(self) -> VelocityTarget:
        res = await self.send_action(0x03, [], [Float32(), Float32(), Float32()])
        if res is None: 
            raise Exception("Failed to get target velocity")
        return {
            'x_ms': res[0],
            'y_ms': res[1],
            'z_rads': res[2]
        }

    async def set_posture(self, pos_x_m: float, pos_y_m: float, pos_z_m: float, rot_x_rad: float, rot_y_rad: float, rot_z_rad: float, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        in_args = [
            Float32(pos_x_m), Float32(pos_y_m), Float32(pos_z_m),
            Float32(rot_x_rad), Float32(rot_y_rad), Float32(rot_z_rad)
        ]
        await self.send_action(0x04, in_args, [], flags)

    async def get_posture(self) -> PostureTarget:
        out_args = [Float32() for _ in range(6)]
        res = await self.send_action(0x05, [], out_args)
        if res is None: 
            raise Exception("Failed to get posture")
        return {
            'pos_x_m': res[0],
            'pos_y_m': res[1],
            'pos_z_m': res[2],
            'rot_x_rad': res[3],
            'rot_y_rad': res[4],
            'rot_z_rad': res[5]
        }