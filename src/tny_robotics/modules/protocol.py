from ..core.data_types import Float32, UInt16
from ..core.protocol import Flag, Protocol
from ..core.module import Module

class ProtocolModule(Module):
    MODULE_ID = 0x01

    def __init__(self, protocol: Protocol):
        super().__init__(self.MODULE_ID, protocol)

    async def set_stream_frequency(self, frequency: float, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        await self.send_action(0x00, [Float32(frequency)], [], flags)

    async def set_stream_flags(self, stream_flags: Flag, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        await self.send_action(0x01, [UInt16(stream_flags)], [], flags)