from machine import WDT
from network import STA_IF, WLAN
from utime import sleep

from config import password, ssid

wlan = WLAN(STA_IF)
watchdog = WDT(timeout=8000)  # 8 Seconds


def safe_import(module_name: str, class_name: str):  # noqa: ANN201
    try:
        module = __import__(module_name)
        return getattr(module, class_name)()
    except ImportError:
        return None


bin_lights = safe_import("bin_lights", "BinLights")
temperature_screen = safe_import("temperature_screen", "TemperatureScreen")


def connect_to_wifi() -> None:
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")


connect_to_wifi()
while True:
    # Every 1hr
    if bin_lights:
        bin_lights.update()

    for _ in range(12):
        # Every 5mins
        if temperature_screen:
            temperature_screen.update()

        for _ in range(60):
            watchdog.feed()
            sleep(5)
