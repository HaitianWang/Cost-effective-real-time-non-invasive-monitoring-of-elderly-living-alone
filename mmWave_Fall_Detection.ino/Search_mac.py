import asyncio
from bleak import BleakScanner

async def scan():
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Device: {device.name}, MAC Address: {device.address}")

asyncio.run(scan())
