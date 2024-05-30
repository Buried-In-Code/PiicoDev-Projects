import utime

from config import offset


class Bin:
    def __init__(self, module: int, led: int, colour: list[int]):
        self.module = module
        self.led = led
        self.colour = colour


class Day:
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


def get_datetime(offset: int = offset) -> tuple[int, int, int, int, int, int, int, int]:
    return utime.gmtime(utime.time() + offset * 3600)


def calculate_week_number() -> int:
    year, _, _, _, _, _, _, day_of_year = get_datetime()

    jan1_tuple = utime.mktime((year, 1, 1, 0, 0, 0, 0, 0))
    jan1_weekday = utime.localtime(jan1_tuple)[6]

    first_monday_offset = -jan1_weekday if jan1_weekday <= 3 else 7 - jan1_weekday

    return (day_of_year + first_monday_offset) // 7 + 1


def calculate_day_of_week() -> int:
    return get_datetime()[6]


def calculate_date() -> tuple[int, int, int, int]:
    year, month, day, _, _, _, day_of_week, _ = get_datetime()
    return year, month, day, day_of_week


def show_date(date: tuple[int, int, int], day_of_week: int) -> str:
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    weekday_name = weekdays[day_of_week]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_name = months[date[1] - 1]
    return f"{weekday_name}, {date[2]:02d} {month_name} {date[0]:04d}"


def calculate_time() -> tuple[int, int, int]:
    _, _, _, hour, minute, second, _, _ = get_datetime()
    return hour, minute, second


def show_time(time: tuple[int, int, int]) -> str:
    return f"{time[0]:02d}:{time[1]:02d}"
