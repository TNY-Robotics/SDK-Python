from ..core.data_types import Bool, UInt8
from ..core.protocol import Protocol
from ..core.module import Module

class I2CModule(Module):
    MODULE_ID = 0x0E

    def __init__(self, protocol: Protocol):
        super().__init__(self.MODULE_ID, protocol)

    async def probe_device(self, address: int) -> bool:
        res = await self.send_action(0x00, [UInt8(address)], [Bool()])
        
        if res is None: 
            raise Exception(f"Failed to probe I2C device at address {hex(address)}")
            
        return bool(res[0])

    async def write_registers(self, address: int, register: int, data: list[int]):
        in_args = [UInt8(address), UInt8(register)] + [UInt8(v) for v in data]
        await self.send_action(0x01, in_args, [])

    async def read_registers(self, address: int, register: int, length: int) -> list[int]:
        in_args = [UInt8(address), UInt8(register), UInt8(length)]
        out_args = [UInt8() for _ in range(length)]
        
        res = await self.send_action(0x02, in_args, out_args)
        
        if res is None: 
            raise Exception(f"Failed to read I2C registers at address {hex(address)}")
            
        return [int(v) for v in res]