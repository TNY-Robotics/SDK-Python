from typing import Any, Optional, Sequence
from .data_types import DataType
from .data_writer import DataWriter
from .data_reader import DataReader
from .protocol import Protocol, Flag

class Module:
    def __init__(self, module_id: int, protocol: Protocol):
        if not (0 <= module_id <= 255):
            raise ValueError('Module ID must be between 0 and 255')
        self.module_id = module_id
        self.protocol = protocol

    async def send_action(self, action_id: int, in_args: Sequence[DataType] | None = None, out_args: Sequence[DataType] | None = None, flags: Flag = Flag.NONE) -> Optional[list[Any]]:        
        in_args = in_args or []
        out_args = out_args or []
        
        if not (0 <= action_id <= 255):
            raise ValueError(f'Action ID {action_id} must be between 0 and 255')

        writer = DataWriter()
        for arg in in_args:
            writer.write(arg)

        if out_args:
            flags |= Flag.REQUIRE_ACK

        data = writer.to_bytes()
        response = await self.protocol.send_request(self.module_id, action_id, data, flags)

        if (not response or len(response) == 0) and not out_args:
            return None
            
        if isinstance(response, bytes):
            reader = DataReader(response)
            results = []
            for arg in out_args:
                results.append(reader.read(arg).value)
            return results
            
        raise ValueError('Invalid response data')