import asyncio
import time
from .core.protocol import Protocol
from .modules.system import SystemModule
from .modules.protocol import ProtocolModule
from .modules.gait import GaitModule
from .modules.body import BodyModule
from .modules.leg import LegModule
from .modules.joint import JointModule
from .modules.motor import MotorModule
from .modules.imu import IMUModule
from .modules.power import PowerModule
from .modules.adc import ADCModule
from .modules.i2c import I2CModule
from .modules.wifi import WiFiModule

class TNY360:
    def __init__(self, ip: str = '192.168.4.1', port: int = 5621):
        self._protocol = Protocol(ip, port)
        self._latency: float = 0.0
        self._latency_task: asyncio.Task | None = None
        
        self.system = SystemModule(self._protocol)
        self.protocol = ProtocolModule(self._protocol)
        self.gait = GaitModule(self._protocol)
        self.body = BodyModule(self._protocol)
        self.leg = LegModule(self._protocol)
        self.joint = JointModule(self._protocol)
        self.motor = MotorModule(self._protocol)
        self.imu = IMUModule(self._protocol)
        self.power = PowerModule(self._protocol)
        self.adc = ADCModule(self._protocol)
        self.i2c = I2CModule(self._protocol)
        self.wifi = WiFiModule(self._protocol)

    async def _latency_loop(self):
        while self.connected:
            start = time.time()
            try:
                await self.system.ping()
            except Exception:
                pass
            
            latency = (time.time() - start) * 1000 # Convert to ms
            
            if self._latency == 0:
                self._latency = latency
            else:
                self._latency = self._latency * 0.8 + latency * 0.2
                
            await asyncio.sleep(2.0)

    async def connect(self):
        await self._protocol.connect()
        self._latency_task = asyncio.create_task(self._latency_loop())

    async def disconnect(self):
        if self._latency_task:
            self._latency_task.cancel()
        await self._protocol.disconnect()

    @property
    def connected(self) -> bool:
        return self._protocol.connected

    @property
    def latency(self) -> float:
        return self._latency