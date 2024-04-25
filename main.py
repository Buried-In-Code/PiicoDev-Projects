import gc
import ujson
from network import WLAN, STA_IF
from machine import WDT
from utime import sleep

import urequests

from config import ssid, password, timezone, modules, weekly_options

wlan = WLAN(STA_IF)
watchdog = WDT(timeout=8000)  # 8 Seconds


def connect_to_wifi():
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    return ip


def load_state() -> tuple[int, int]:
    try:
        with open("state.json", "r") as stream:
            data = ujson.load(stream)
            return data["index"], data["week"]
    except OSError:
        return 0, None


def save_state(index: int, week: int):
    try:
        with open("state.json", "w") as stream:
            ujson.dump({"index": index, "week": week}, stream)
    except OSError as e:
        print("Error saving state:", e)


def get_week() -> int:
    try:
        response = urequests.get(f"http://worldtimeapi.org/api/timezone/{timezone}")
        response = response.json()
        return response.get("week_number", None)
    except Exception as e:
        print("Error fetching week number:", e)
        return None


def change_lights(index: int) -> int:
    for module in modules:
        module.clear()

    for bin in weekly_options[index]:
        weekly_options[bin.module_index].setPixel(bin.light_index, bin.colour)
    for module in modules:
        module.show()

    index = (index + 1) % len(weekly_options)
    return index


ip = connect_to_wifi()
index, week = load_state()
while True:
    new_week = get_week()
    if new_week is not None and week is not None:
        week_difference = new_week - week
        if week_difference < 0:  # New year
            week_difference += 52  # Assuming 52 weeks in a year
        for _ in range(week_difference):
            index = change_lights(index)
        save_state(index, new_week)
        week = new_week

    gc.collect()
    # Wait 1hr
    for _ in range(60 * 60 // 5):
        watchdog.feed()
        sleep(5)
