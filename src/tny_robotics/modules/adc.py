from ..core.data_types import Float32
from ..core.protocol import Protocol
from ..core.module import Module

class ADCModule(Module):
    MODULE_ID = 0x0F

    def __init__(self, protocol: Protocol):
        super().__init__(self.MODULE_ID, protocol)

    async def get_all_channels(self) -> list[float]:
        out_args = [Float32() for _ in range(16)]
        res = await self.send_action(0x00, [], out_args)
        
        if res is None: 
            raise Exception("Failed to get ADC channels")
            
        return [float(v) for v in res]