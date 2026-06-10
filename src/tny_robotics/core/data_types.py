import struct
from abc import ABC, abstractmethod
from typing import Any, List

class DataType(ABC):
    value: Any

    @abstractmethod
    def size(self) -> int: pass
    
    @abstractmethod
    def to_bytes(self) -> bytes: pass
    
    @abstractmethod
    def from_bytes(self, data: bytes, offset: int) -> 'DataType': pass

class UInt8(DataType):
    def __init__(self, value: int = 0):
        if not (0 <= value <= 0xFF): raise ValueError("Value must be between 0 and 255")
        self.value = value
    def size(self) -> int: return 1
    def to_bytes(self) -> bytes: return struct.pack('<B', self.value)
    def from_bytes(self, data: bytes, offset: int) -> 'UInt8':
        return UInt8(struct.unpack_from('<B', data, offset)[0])

class UInt16(DataType):
    def __init__(self, value: int = 0):
        if not (0 <= value <= 0xFFFF): raise ValueError("Value must be between 0 and 65535")
        self.value = value
    def size(self) -> int: return 2
    def to_bytes(self) -> bytes: return struct.pack('<H', self.value)
    def from_bytes(self, data: bytes, offset: int) -> 'UInt16':
        return UInt16(struct.unpack_from('<H', data, offset)[0])

class UInt32(DataType):
    def __init__(self, value: int = 0):
        if not (0 <= value <= 0xFFFFFFFF): raise ValueError("Value must be between 0 and 4294967295")
        self.value = value
    def size(self) -> int: return 4
    def to_bytes(self) -> bytes: return struct.pack('<I', self.value)
    def from_bytes(self, data: bytes, offset: int) -> 'UInt32':
        return UInt32(struct.unpack_from('<I', data, offset)[0])

class Float32(DataType):
    def __init__(self, value: float = 0.0):
        self.value = float(value)
    def size(self) -> int: return 4
    def to_bytes(self) -> bytes: return struct.pack('<f', self.value)
    def from_bytes(self, data: bytes, offset: int) -> 'Float32':
        return Float32(struct.unpack_from('<f', data, offset)[0])

class Bool(DataType):
    def __init__(self, value: bool = False):
        self.value = bool(value)
    def size(self) -> int: return 1
    def to_bytes(self) -> bytes: return struct.pack('<?', self.value)
    def from_bytes(self, data: bytes, offset: int) -> 'Bool':
        return Bool(struct.unpack_from('<?', data, offset)[0])

class StringType(DataType):
    def __init__(self, value: str = ""):
        if len(value) > 0xFFFF: raise ValueError("String length must be between 0 and 65535")
        if not value.isascii(): raise ValueError("String must contain only ASCII characters")
        self.value = value
        
    def size(self) -> int: return len(self.value) + 2
    
    def to_bytes(self) -> bytes:
        encoded = self.value.encode('ascii')
        return struct.pack(f'<H{len(encoded)}s', len(encoded), encoded)
        
    def from_bytes(self, data: bytes, offset: int) -> 'StringType':
        length = struct.unpack_from('<H', data, offset)[0]
        string_val = struct.unpack_from(f'<{length}s', data, offset + 2)[0].decode('ascii')
        return StringType(string_val)