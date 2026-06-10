import asyncio
import struct
import websockets
from enum import IntEnum, IntFlag
from .data_types import UInt8, UInt16
from .data_writer import DataWriter
from .data_reader import DataReader

class Flag(IntFlag):
    NONE = 0
    REQUIRE_ACK = 1 << 0

class Type(IntEnum):
    REQUEST = 1
    RESPONSE = 2
    EVENT = 3

class Status(IntEnum):
    OK = 0
    UNKNOWN_MODULE = 1
    UNKNOWN_ACTION = 2
    INVALID_PARAMETERS = 3

class RequestError(Exception):
    def __init__(self, status: Status):
        super().__init__(f'Request Error: {status.name}')
        self.status = status

class Protocol:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.ws = None
        self._msg_id_counter = 0
        self.pending_requests: dict[int, asyncio.Future] = {}
        self._receive_task = None

    def _generate_msg_id(self) -> int:
        self._msg_id_counter += 1
        if self._msg_id_counter > 0xFFFF:
            self._msg_id_counter = 0
        return self._msg_id_counter

    def _generate_message_header(self, module_id: int, action_id: int, flags: Flag, msg_id: int, length: int) -> bytes:
        # B=uint8, H=uint16
        return struct.pack('<BBHBBH', Type.REQUEST, flags, msg_id, module_id, action_id, length)

    def _parse_message_header(self, data: bytes) -> dict:
        if len(data) < 8: raise ValueError('Invalid message header')
        
        msg_type, flags, msg_id, mod_id, act_id, length = struct.unpack('<BBHBBH', data[:8])
        
        status = None
        if msg_type == Type.RESPONSE:
            # Le statut prend la place de mod_id et act_id (octets 4 et 5).
            # On lit donc 2 octets (<H) à l'offset 4.
            status_val = struct.unpack_from('<H', data, offset=4)[0]
            try:
                status = Status(status_val)
            except ValueError:
                # Si le status n'est pas dans l'Enum
                status = status_val
            
        return {
            'type': Type(msg_type),
            'flags': Flag(flags),
            'msgId': msg_id,
            'moduleId': mod_id,
            'actionId': act_id,
            'length': length,
            'status': status
        }

    async def _on_message(self, data: bytes):
        if len(data) < 8: return
        
        header = self._parse_message_header(data)
        
        if header['type'] == Type.RESPONSE:
            future = self.pending_requests.get(header['msgId'])
            if future and not future.done():
                if header['status'] == Status.OK:
                    # On renvoie le payload utile
                    future.set_result(data[8 : 8 + header['length']])
                else:
                    future.set_exception(RequestError(header['status']))
                del self.pending_requests[header['msgId']]

    async def _receive_loop(self):
        if (not self.ws): return
        try:
            async for message in self.ws:
                await self._on_message(message if isinstance(message, bytes) else (message.encode() if isinstance(message, str) else message))
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            print(f"Receive loop error : {repr(e)}")

    async def connect(self):
        self.ws = await websockets.connect(f'ws://{self.ip}:{self.port}')
        # On lance la boucle d'écoute en arrière-plan
        self._receive_task = asyncio.create_task(self._receive_loop())

    async def disconnect(self):
        if self._receive_task:
            self._receive_task.cancel()
        if self.ws:
            await self.ws.close()
            self.ws = None

    @property
    def connected(self) -> bool:
        return self.ws is not None

    async def send_request(self, module_id: int, action_id: int, data: bytes = b'', flags: Flag = Flag.NONE) -> bytes | None:
        if not self.ws:
            raise ConnectionError('Not connected')

        msg_id = self._generate_msg_id()
        header = self._generate_message_header(module_id, action_id, flags, msg_id, len(data))
        message = header + data
        
        await self.ws.send(message)

        if flags & Flag.REQUIRE_ACK:
            loop = asyncio.get_running_loop()
            future = loop.create_future()
            self.pending_requests[msg_id] = future
            # Timeout de 2 secondes comme en TS
            return await asyncio.wait_for(future, timeout=2.0)
        
        return None