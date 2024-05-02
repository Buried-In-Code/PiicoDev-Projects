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


def connect_to_wifi() -> str:
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    return ip


def load_state() -> tuple[tuple[int, int, int], int]:
    try:
        with open("state.json") as stream:
            data = ujson.load(stream)
            return data["last_updated"], data["index"]
    except OSError as err:
        print("Error loading state:", err)
        return None, 0


def save_state(last_updated: tuple[int, int, int], index: int) -> None:
    try:
        with open("state.json", "w") as stream:
            ujson.dump({"last_updated": last_updated, "index": index}, stream)
    except OSError as err:
        print("Error saving state:", err)


def get_current_date() -> tuple[tuple[int, int, int], Day]:
    try:
        response = urequests.get(f"http://worldtimeapi.org/api/timezone/{timezone}")
        data = response.json()
        return map(int, data["datetime"].split("T")[0].split("-")), Day(value=data["day_of_week"])
    except Exception as err:  # noqa: BLE001
        print("Error fetching current date:", err)
        return None, None


def zellers_congruence(year: int, month: int, day: int) -> int:
    if month < 3:
        month += 12
        year -= 1
    c = year // 100
    year = year % 100
    return (c // 4 - 2 * c + year + year // 4 + 13 * (month + 1) // 5 + day - 1) % 7


def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def next_day(year: int, month: int, day: int) -> tuple[int, int, int]:
    day += 1
    if (
        (day == 32 and month in (1, 3, 5, 7, 8, 10, 12))
        or (day == 31 and month in (4, 6, 9, 11))
        or (day == 29 and month == 2 and not is_leap_year(year=year))
        or (day == 30 and month == 2 and is_leap_year(year=year))
    ):
        day = 1
        month += 1
    if month == 13:
        month = 1
        year += 1
    return year, month, day


def count_mondays(start_date: tuple[int, int, int], end_date: tuple[int, int, int]) -> int:
    monday_count = 0
    current = start_date
    while current <= end_date:
        if zellers_congruence(*current) == 1:
            monday_count += 1
        current = next_day(*current)
    return monday_count


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
last_updated, index = load_state()
while True:
    for module in modules:
        module.pwrLED(True)

    current_date, day_of_week = get_current_date()
    if current_date is not None:
        if last_updated is not None and current_date != last_updated:
            for _ in range(count_mondays(start_date=last_updated, end_date=current_date)):
                index = (index + 1) % len(bin_rotation)
        last_updated = current_date
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
