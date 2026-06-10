from enum import IntEnum, IntFlag
from typing import TypedDict
from ..core.data_types import Bool, Float32, UInt8
from ..core.protocol import Flag, Protocol
from ..core.module import Module

class LegJointFlag(IntFlag):
    HipRoll = 1 << 0
    HipPitch = 1 << 1
    KneePitch = 1 << 2

class LegId(IntEnum):
    FrontLeft = 0
    BackLeft = 1
    BackRight = 2
    FrontRight = 3

class LegPosition(TypedDict):
    x_m: float
    y_m: float
    z_m: float

class LegModule(Module):
    MODULE_ID = 0x04

    def __init__(self, protocol: Protocol):
        super().__init__(self.MODULE_ID, protocol)

    async def set_enabled(self, leg_id: LegId, joint_flag: LegJointFlag, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        await self.send_action(0x00, [UInt8(leg_id), UInt8(joint_flag)], [], flags)

    async def get_enabled(self, leg_id: LegId) -> LegJointFlag:
        res = await self.send_action(0x01, [UInt8(leg_id)], [UInt8()])
        if res is None: raise Exception(f"Failed to get enabled state for leg {leg_id}")
        return LegJointFlag(res[0])

    async def set_position(self, id: LegId, x_m: float, y_m: float, z_m: float, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        in_args = [UInt8(id), Float32(x_m), Float32(y_m), Float32(z_m)]
        await self.send_action(0x02, in_args, [], flags)

    async def get_target_position(self, id: LegId) -> LegPosition:
        res = await self.send_action(0x03, [UInt8(id)], [Float32(), Float32(), Float32()])
        if res is None: raise Exception(f"Failed to get target position for leg {id}")
        return {
            'x_m': res[0],
            'y_m': res[1],
            'z_m': res[2]
        }

    async def get_grounded(self, id: LegId) -> bool:
        res = await self.send_action(0x04, [UInt8(id)], [Bool()])
        if res is None: raise Exception(f"Failed to get grounded state for leg {id}")
        return bool(res[0])