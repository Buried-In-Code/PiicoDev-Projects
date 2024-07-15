import ntptime
import utime
from utime import sleep

from config import offset


class Clock:
    def __init__(self) -> None:
        while True:
            try:
                ntptime.settime()
                break
            except OSError as err:
                print("Failed to set time:", err)
            sleep(1)

    def get_datetime(self) -> tuple[int, int, int, int, int, int, int, int]:
        return utime.gmtime(utime.time() + offset * 3600)

    def calculate_days(self) -> tuple[int, int]:
        year, _, _, _, _, _, day_of_week, day_of_year = self.get_datetime()

        jan1_tuple = utime.mktime((year, 1, 1, 0, 0, 0, 0, 0))
        jan1_weekday = utime.localtime(jan1_tuple)[6]

        first_monday_offset = -jan1_weekday if jan1_weekday <= 3 else 7 - jan1_weekday

        return day_of_week, (day_of_year + first_monday_offset) // 7 + 1

    def date_str(self) -> str:
        year, month, day, _, _, _, day_of_week, _ = self.get_datetime()
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        weekday_name = weekdays[day_of_week]
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        month_name = months[month - 1]
        return f"{weekday_name}, {day:02d} {month_name} {year:04d}"

    def time_str(self) -> str:
        _, _, _, hour, minute, second, _, _ = self.get_datetime()
        return f"{hour:02d}:{minute:02d}:{second:02d}"
