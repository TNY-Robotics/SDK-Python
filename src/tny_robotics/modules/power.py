from ..core.data_types import Float32
from ..core.protocol import Protocol
from ..core.module import Module

class PowerModule(Module):
    MODULE_ID = 0x09

    def __init__(self, protocol: Protocol):
        super().__init__(self.MODULE_ID, protocol)

    async def get_voltage(self) -> float:
        res = await self.send_action(0x00, [], [Float32()])
        if res is None: raise Exception("Failed to get voltage")
        return float(res[0])

    async def get_current(self) -> float:
        res = await self.send_action(0x01, [], [Float32()])
        if res is None: raise Exception("Failed to get current")
        return float(res[0])

    async def get_power(self) -> float:
        res = await self.send_action(0x02, [], [Float32()])
        if res is None: raise Exception("Failed to get power")
        return float(res[0])