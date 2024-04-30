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

    def __add__(self, days: int) -> "Date":
        year, month, day = self.year, self.month, self.day
        for _ in range(days):
            day += 1
            if (
                (day == 32 and month in (1, 3, 5, 7, 8, 10, 12))
                or (day == 31 and month in (4, 6, 9, 11))
                or (day == 29 and month == 2 and not self.is_leap_year())
                or (day == 30 and month == 2 and self.is_leap_year())
            ):
                day = 1
                month += 1
            if month == 13:
                month = 1
                year += 1
        return Date(year=year, month=month, day=day)

    def __sub__(self, days: int) -> "Date":
        year, month, day = self.year, self.month, self.day
        for _ in range(days):
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
                    day = 29 if self.is_leap_year() else 28
        return Date(year=year, month=month, day=day)

    @staticmethod
    def from_iso_format(date_str: str) -> "Date":
        year, month, day = map(int, date_str.split("T")[0].split("-"))
        return Date(year=year, month=month, day=day)

    def to_dict(self) -> dict:
        return {"year": self.year, "month": self.month, "day": self.day}

    def is_leap_year(self) -> bool:
        return self.year % 4 == 0 and (self.year % 100 != 0 or self.year % 400 == 0)


def zellers_congruence(year: int, month: int, day: int) -> int:
    if month < 3:
        month += 12
        year -= 1
    c = year // 100
    year = year % 100
    return (c // 4 - 2 * c + year + year // 4 + 13 * (month + 1) // 5 + day - 1) % 7


def count_mondays(start: Date, end: Date) -> int:
    monday_count = 0
    current = start
    while current <= end:
        if zellers_congruence(year=current.year, month=current.month, day=current.day) == 1:
            monday_count += 1
        current += 1
    return monday_count
