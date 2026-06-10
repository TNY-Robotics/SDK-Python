from typing import List
from .data_types import DataType

class DataWriter:
    def __init__(self):
        self.buffer: List[DataType] = []

    def write(self, data: DataType) -> 'DataWriter':
        self.buffer.append(data)
        return self

    def to_bytes(self) -> bytes:
        return b''.join([data.to_bytes() for data in self.buffer])

    def size(self) -> int:
        return sum(data.size() for data in self.buffer)