import gc
import ujson
from machine import WDT
from network import STA_IF, WLAN
from utime import sleep

import urequests

from config import bin_rotation, modules, password, show_lights, ssid, timezone
from utils import Day

wlan = WLAN(STA_IF)
watchdog = WDT(timeout=8000)  # 8 Seconds


def connect_to_wifi() -> None:
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")


def load_state() -> tuple[int, int]:
    try:
        with open("state.json") as stream:
            data = ujson.load(stream)
            return data["last_updated"], data["index"]
    except OSError as err:
        print("Error loading state:", err)
        return None, 0


def save_state(last_updated: int, index: int) -> None:
    try:
        with open("state.json", "w") as stream:
            ujson.dump({"last_updated": last_updated, "index": index}, stream)
    except OSError as err:
        print("Error saving state:", err)


def get_current_date() -> tuple[int, Day]:
    try:
        response = urequests.get(f"http://worldtimeapi.org/api/timezone/{timezone}")
        data = response.json()
        return data["week_number"], Day(value=data["day_of_week"])
    except Exception as err:  # noqa: BLE001
        print("Error fetching current date:", err)
        return None, None


def disable_lights() -> None:
    for module in modules:
        module.clear()
        module.show()


def enable_lights(index: int) -> None:
    disable_lights()
    for bin in bin_rotation[index]:  # noqa: A001
        modules[bin.module].setPixel(bin.led, bin.colour)
    for module in modules:
        module.show()


connect_to_wifi()
last_updated, index = load_state()
while True:
    for module in modules:
        module.pwrLED(True)

    week_number, day_of_week = get_current_date()
    if week_number is not None:
        if last_updated is not None:
            if week_number != last_updated:
                index = 1 - index
        last_updated = week_number
        save_state(last_updated=last_updated, index=index)
    if day_of_week is not None:
        if day_of_week in show_lights:
            enable_lights(index=index)
        else:
            disable_lights()

    for module in modules:
        module.pwrLED(False)

    gc.collect()
    # Wait 1hr
    for _ in range(60 * 60 // 5):
        watchdog.feed()
        sleep(5)
