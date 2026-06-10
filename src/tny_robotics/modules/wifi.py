from ..core.data_types import StringType
from ..core.protocol import Flag, Protocol
from ..core.module import Module

class WiFiModule(Module):
    MODULE_ID = 0x10

    def __init__(self, protocol: Protocol):
        super().__init__(self.MODULE_ID, protocol)

    async def connect_to_ap(self, ssid: str, password: str, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        await self.send_action(0x00, [StringType(ssid), StringType(password)], [], flags)