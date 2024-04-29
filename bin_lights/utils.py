from enum import IntEnum


class Bin:
    def __init__(self, module: int, led: int, colour: list[int]):
        self.module = module
        self.led = led
        self.colour = colour


class Day(IntEnum):
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6
    SUN = 7

    def __add__(self, other) -> "Day":  # noqa: ANN001
        if not isinstance(other, int):
            raise NotImplementedError
        result = (self.value + other - 1) % 7 + 1
        return Day(result)

    def __sub__(self, other) -> "Day":  # noqa: ANN001
        if not isinstance(other, int):
            raise NotImplementedError
        result = (self.value - other - 1) % 7 + 1
        return Day(result)


class Date:
    def __init__(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day

    def __lt__(self, other) -> int:  # noqa: ANN001
        if not isinstance(other, type(self)):
            raise NotImplementedError
        return (self.year, self.month, self.day) < (other.year, other.month, other.day)

    def __eq__(self, other) -> bool:  # noqa: ANN001
        if not isinstance(other, type(self)):
            raise NotImplementedError
        return (self.year, self.month, self.day) == (other.year, other.month, other.day)

    def __hash__(self) -> int:
        return hash((type(self), self.year, self.month, self.day))

    @staticmethod
    def from_iso_format(date_str: str) -> "Date":
        year, month, day = map(int, date_str.split("T")[0].split("-"))
        return Date(year=year, month=month, day=day)

    def to_dict(self) -> dict:
        return {"year": self.year, "month": self.month, "day": self.day}


def zellers_congruence(year: int, month: int, day: int) -> int:
    if month < 3:
        month += 12
        year -= 1
    c = year // 100
    year = year % 100
    return (c // 4 - 2 * c + year + year // 4 + 13 * (month + 1) // 5 + day - 1) % 7


def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def next_day(date: Date) -> Date:
    year, month, day = date.year, date.month, date.day

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
    return Date(year=year, month=month, day=day)


def previous_day(date: Date) -> Date:
    year, month, day = date.year, date.month, date.day

    day -= 1
    if day == 0:
        month -= 1
        if month == 0:
            month = 12
            year -= 1
        if month in (1, 3, 5, 7, 8, 10, 12):
            day = 31
        elif month in (4, 6, 9, 11):
            day = 30
        elif month == 2:
            day = 29 if is_leap_year(year=year) else 28

    return Date(year=year, month=month, day=day)


def count_mondays(start: Date, end: Date) -> int:
    monday_count = 0
    current = start
    while current <= end:
        if zellers_congruence(year=current.year, month=current.month, day=current.day) == 1:
            monday_count += 1
        current = next_day(date=current)
    return monday_count
