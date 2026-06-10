from enum import IntEnum
from ..core.data_types import UInt8
from ..core.protocol import Flag, Protocol
from ..core.module import Module

class GaitType(IntEnum):
    Creep = 0
    Walk = 1
    Run = 2
    Jump = 3

class GaitModule(Module):
    MODULE_ID = 0x02

    def __init__(self, protocol: Protocol):
        super().__init__(self.MODULE_ID, protocol)

    async def set_type(self, gait_type: GaitType, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        await self.send_action(0x00, [UInt8(gait_type)], [], flags)

    async def get_type(self) -> GaitType:
        res = await self.send_action(0x01, [], [UInt8()])
        
        if res is None:
            raise Exception("Failed to get gait type")
            
        return GaitType(res[0])