from enum import IntEnum, IntFlag
from typing import TypedDict
from ..core.data_types import Float32, StringType, UInt8, UInt32
from ..core.protocol import Flag, Protocol
from ..core.module import Module

class AutoLifeFlags(IntFlag):
    None_ = 0
    Safeguard = 1 << 0
    AutoGait = 1 << 1
    AutoPosture = 1 << 2
    Animate = 1 << 3
    Wandering = 1 << 4

class AutoLifeLevel(IntEnum):
    Off = AutoLifeFlags.None_
    Safeguard = AutoLifeFlags.Safeguard
    Animate = AutoLifeFlags.Safeguard | AutoLifeFlags.AutoGait | AutoLifeFlags.AutoPosture | AutoLifeFlags.Animate
    Full = AutoLifeFlags.Safeguard | AutoLifeFlags.AutoGait | AutoLifeFlags.AutoPosture | AutoLifeFlags.Animate | AutoLifeFlags.Wandering

class CpuUsage(TypedDict):
    core0: float
    core1: float

class RamUsage(TypedDict):
    internal_total: int
    internal_used: int
    psram_total: int
    psram_used: int

class SystemStatistics(TypedDict):
    temp_c: float
    cpu_usage: CpuUsage
    ram_usage: RamUsage

class SystemModule(Module):
    MODULE_ID = 0x00

    def __init__(self, protocol: Protocol):
        super().__init__(self.MODULE_ID, protocol)

    async def ping(self):
        await self.send_action(0x00, [], [], Flag.REQUIRE_ACK)

    async def reboot(self):
        await self.send_action(0x01, [], [])

    async def set_settings(self, settings_json: str, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        await self.send_action(0x02, [StringType(settings_json)], [], flags)

    async def get_settings(self) -> str:
        res = await self.send_action(0x03, [], [StringType()])
        if res is None: raise Exception("Failed to get system settings")
        return str(res[0])

    async def set_auto_life_level(self, level: AutoLifeLevel, wait_response: bool = False):
        flags = Flag.REQUIRE_ACK if wait_response else Flag.NONE
        await self.send_action(0x04, [UInt8(level)], [], flags)

    async def get_auto_life_level(self) -> AutoLifeLevel:
        res = await self.send_action(0x05, [], [UInt8()])
        if res is None: raise Exception("Failed to get auto life level")
        return AutoLifeLevel(res[0])

    async def get_statistics(self) -> SystemStatistics:
        out_args = [
            Float32(), Float32(), Float32(),  # Temp, Core0, Core1
            UInt32(), UInt32(), UInt32(), UInt32()  # Ram internal/psram
        ]
        res = await self.send_action(0x06, [], out_args)
        if res is None: raise Exception("Failed to get system statistics")
        
        return {
            'temp_c': float(res[0]),
            'cpu_usage': {
                'core0': float(res[1]),
                'core1': float(res[2])
            },
            'ram_usage': {
                'internal_total': int(res[3]),
                'internal_used': int(res[4]),
                'psram_total': int(res[5]),
                'psram_used': int(res[6])
            }
        }