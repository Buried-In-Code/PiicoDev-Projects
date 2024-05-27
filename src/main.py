import gc
import ntptime
from machine import WDT
from network import STA_IF, WLAN
from utime import sleep

from config import password, ssid

wlan = WLAN(STA_IF)
watchdog = WDT(timeout=8000)  # 8 Seconds

try:
    from bin_lights import BinLights

    bin_lights = BinLights()
except ImportError:
    bin_lights = None
try:
    from temperature_screen import TemperatureScreen

    temperature_screen = TemperatureScreen()
except ImportError:
    temperature_screen = None


def connect_to_wifi() -> None:
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")


def set_time() -> None:
    while True:
        try:
            ntptime.settime()
            return
        except OSError as err:
            print("Failed to set time:", err)


def custom_sleep() -> None:
    for _ in range(12):
        gc.collect()
        watchdog.feed()
        sleep(5)


connect_to_wifi()
set_time()

print(f"Bin Lights enabled: {bin_lights is not None}")
print(f"Temperature Screen enabled: {temperature_screen is not None}")
while True:
    if bin_lights:
        bin_lights.update()

    for _ in range(12):  # Waiting 1hr
        if temperature_screen:
            temperature_screen.update()

        for _ in range(5):  # Waiting 5mins
            print("Waiting 1min...")
            custom_sleep()  # Waiting 1min
