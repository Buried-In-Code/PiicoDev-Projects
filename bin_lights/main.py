import gc
import ujson
from machine import WDT
from network import STA_IF, WLAN
from utime import sleep

import urequests

from config import bin_rotation, modules, password, rubbish_day, show_after, show_before, ssid
from utils import Date, Day, count_mondays

wlan = WLAN(STA_IF)
watchdog = WDT(timeout=8000)  # 8 Seconds


def connect_to_wifi() -> str:
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    return ip


def load_state() -> tuple[int, Date]:
    try:
        with open("state.json") as stream:
            data = ujson.load(stream)
            return data["index"], Date(**data["date"])
    except OSError as err:
        print("Error loading state:", err)
        return 0, None


def save_state(index: int, date: Date) -> None:
    try:
        with open("state.json", "w") as stream:
            ujson.dump({"index": index, "date": date.to_dict()}, stream)
    except OSError as err:
        print("Error saving state:", err)


def get_current_date() -> tuple[Date, Day]:
    try:
        response = urequests.get("http://worldtimeapi.org/api/ip")
        data = response.json()
        return Date.from_iso_format(data["datetime"]), Day(data["day_of_week"])
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


ip = connect_to_wifi()
index, date = load_state()
while True:
    for module in modules:
        module.pwrLED(True)

    current_date, day_of_week = get_current_date()
    if current_date and (not date or current_date != date):
        if (
            (show_before and day_of_week - rubbish_day == 1)
            or (rubbish_day == day_of_week)
            or (show_after and rubbish_day - day_of_week == 1)
        ):
            enable_lights(index=index)
        else:
            disable_lights()
        if date:
            for _ in count_mondays(start=date, end=current_date):
                index = (index + 1) % len(bin_rotation)
        date = current_date
        save_state(index=index, date=date)

    for module in modules:
        module.pwrLED(False)

    gc.collect()
    # Wait 1hr
    for _ in range(60 * 60 // 5):
        watchdog.feed()
        sleep(5)
