import urequests

from config import timezone


class Day:
    SUN = 0
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6


def get_current_date() -> tuple[int, int]:
    try:
        response = urequests.get(f"http://worldtimeapi.org/api/timezone/{timezone}")
        data = response.json()
        return data["week_number"], data["day_of_week"]
    except Exception as err:  # noqa: BLE001
        print("Error fetching current date:", err)
        return None, None


def get_current_datetime() -> tuple[int, int, int, int, int, int]:
    try:
        response = urequests.get(f"http://worldtimeapi.org/api/timezone/{timezone}")
        data = response.json()
        date = map(int, data.split("T")[0].split("-"))
        time = map(int, data.split("T")[1].split(".")[0].split(":"))
        return *date, *time
    except Exception as err:  # noqa: BLE001
        print("Error fetching current date:", err)
        return None, None, None, None, None, None
