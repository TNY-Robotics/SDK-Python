from ..core.data_types import Bool, Float32, UInt8
from ..core.protocol import Flag, Protocol
from ..core.module import Module
from .motor import MotorId

JointId = MotorId

class JointModule(Module):
    MODULE_ID = 0x05

    def __init__(self, protocol: Protocol):
        super().__init__(self.MODULE_ID, protocol)

    async def set_enabled(self, id: JointId, enabled: bool, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        await self.send_action(0x00, [UInt8(id), Bool(enabled)], [], flags)

    async def get_enabled(self, id: JointId) -> bool:
        res = await self.send_action(0x01, [UInt8(id)], [Bool()])
        if res is None: raise Exception(f"Failed to get enabled state for joint {id}")
        return bool(res[0])

    async def set_angle(self, id: JointId, angle: float, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        await self.send_action(0x02, [UInt8(id), Float32(angle)], [], flags)

    async def get_target_angle(self, id: JointId) -> float:
        res = await self.send_action(0x03, [UInt8(id)], [Float32()])
        if res is None: raise Exception(f"Failed to get target angle for joint {id}")
        return float(res[0])

    async def get_feedback_angle(self, id: JointId) -> float:
        res = await self.send_action(0x04, [UInt8(id)], [Float32()])
        if res is None: raise Exception(f"Failed to get feedback angle for joint {id}")
        return float(res[0])

    async def get_model_angle(self, id: JointId) -> float:
        res = await self.send_action(0x05, [UInt8(id)], [Float32()])
        if res is None: raise Exception(f"Failed to get model angle for joint {id}")
        return float(res[0])

    async def get_estimated_angle(self, id: JointId) -> float:
        res = await self.send_action(0x06, [UInt8(id)], [Float32()])
        if res is None: raise Exception(f"Failed to get estimated angle for joint {id}")
        return float(res[0])

    async def set_joint_angles(self, angles: list[float], wait_response: bool = False):
        if len(angles) != 14:
            raise ValueError("Invalid angles array length. Expected 14.")
        in_args = [Float32(angle) for angle in angles]
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        await self.send_action(0x07, in_args, [], flags)

    async def get_joint_angles(self) -> list[float]:
        out_args = [Float32() for _ in range(14)]
        res = await self.send_action(0x08, [], out_args)
        if res is None: raise Exception("Failed to get joint angles")
        return [float(v) for v in res]