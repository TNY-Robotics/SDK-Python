from .data_types import DataType

class DataReader:
    def __init__(self, data: bytes):
        self.buffer = data
        self.offset = 0

    def read(self, data_type: DataType) -> DataType:
        if len(self.buffer) < self.offset + data_type.size():
            raise ValueError('Not enough data to read')
        value = data_type.from_bytes(self.buffer, self.offset)
        self.offset += data_type.size()
        return value