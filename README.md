<div align="center">

# tny-robotics-sdk

[![PyPI version](https://img.shields.io/pypi/v/tny-robotics-sdk.svg?color=blue)](https://pypi.org/project/tny-robotics-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://www.python.org/)

**The official Python SDK for all TNY Robotics robots**

[🌐 Website](https://tny-robotics.com/) • [📦 PyPI Package](https://pypi.org/project/tny-robotics-sdk/) • [💬 Discord](https://discord.gg/XGABkx5A4y)

</div>

---

## 🚀 Overview

`tny-robotics-sdk` provides a clean, asynchronous API to communicate with your TNY Robotics robot.

It handles all the complex binary WebSocket framing and event loop bindings under the hood using `asyncio`, letting you focus on building advanced robotics applications, telemetry scripts, or AI/control algorithms.

### ✨ Features
* **Native Async:** Built entirely on top of `asyncio` and `websockets` for high-performance, non-blocking I/O.
* **Fully Typed:** Strict type hints and `TypedDict` implementations for excellent auto-completion and Developer Experience (DX) in VS Code, PyCharm, etc.
* **Modular:** Access robot features cleanly through dedicated modules (`robot.system`, `robot.joint`, `robot.power`, etc.).

---

## 📦 Installation

Install the package using `pip` (or your preferred environment manager like `poetry` or `pipenv`):

```bash
pip install tny-robotics-sdk

```

---

## 💻 Quick Start

Here is a simple example to connect to your TNY-360 and test the connection latency:

```python
import asyncio
import time
from tny_robotics import TNY360

async def main():
    print('Creating TNY-360 instance...')
    # Replace with your robot's IP address
    robot = TNY360('192.168.4.1')

    try:
        print('Connecting to TNY-360...')
        await robot.connect()
        print('Connected successfully!')
    except Exception as err:
        print('Connection error:', err)
        return

    # Ping test
    print('Sending pings...')
    start = time.time()
    for _ in range(10):
        await robot.system.ping()
    end = time.time()
    
    # Calculate average time in milliseconds
    avg_time = ((end - start) * 1000) / 10
    print(f"Average response time: {avg_time:.2f} ms.")
    
    # Clean disconnect
    await robot.disconnect()

if __name__ == '__main__':
    asyncio.run(main())

```

---

## 🧩 API Structure

The SDK is organized into intuitive modules. Here are some examples of what you can do:

### System & Settings

```python
# Get robot statistics
stats = await robot.system.get_statistics()
print(f"Temperature: {stats['temp_c']}°C, CPU0 Usage: {stats['cpu_usage']['core0']}%")

# Change AutoLife mode
from tny_robotics import AutoLifeLevel
await robot.system.set_auto_life_level(AutoLifeLevel.Safeguard)

```

### Motion & Joints

```python
import math
from tny_robotics import MotorId

# Set the front-right knee joint to 30 degrees (converted to radians)
await robot.joint.set_angle(MotorId.FrontRightKneePitch, 30 * (math.pi / 180))

# Get the current angle of the back-left hip roll joint
cur_angle = await robot.joint.get_feedback_angle(MotorId.BackLeftHipRoll)
print(f"Current Hip Roll Angle: {cur_angle * (180 / math.pi):.2f} degrees")

```

### Sensors & Telemetry *(Coming soon)*

```python
# Subscribe to continuous Lidar distance updates
# (Implementation in progress)

```

---

## 🤝 Contributing

This SDK is part of the open-source TNY-Robotics ecosystem.
Found a bug or want to add a new module? [Open an Issue](https://github.com/TNY-Robotics/SDK-Python/issues) or submit a Pull Request!

## 📄 License

This SDK is licensed under the **MIT License**.
*You are free to use it in your open-source or commercial applications, just include the copyright notice.*

Need help? Contact us [by mail](https://www.google.com/search?q=mailto%3Acontact%40tny-robotics.com) or join our [Discord](https://discord.gg/XGABkx5A4y).