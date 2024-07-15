import gc
from machine import WDT
from network import STA_IF, WLAN
from utime import sleep

from bin_lights import BinLights
from clock import Clock
from config import password, ssid
from temperature_screen import TemperatureScreen

wlan = WLAN(STA_IF)


def connect_to_wifi() -> None:
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")


def sleep_min(value: int = 1) -> None:
    for _ in range(value):
        for _ in range(12):
            gc.collect()
            watchdog.feed()
            sleep(5)


connect_to_wifi()

clock = Clock()
bin_lights = BinLights(clock=clock)
temperature_screen = TemperatureScreen(clock=clock)
watchdog = WDT(timeout=8000)  # 8 Seconds

while True:
    bin_lights.update()  # Run every hr

    for _ in range(12):
        temperature_screen.update()  # Run every 5min

        print("Waiting 5min...")
        sleep_min(value=5)
