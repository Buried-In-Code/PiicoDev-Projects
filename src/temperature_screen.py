import ujson
from ucollections import deque

import urequests
from PiicoDev_SSD1306 import HEIGHT, create_PiicoDev_SSD1306
from PiicoDev_TMP117 import PiicoDev_TMP117

from config import base_url, device_name
from utils import get_datetime, show_date, show_time

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": f"Freyr-Device/2.0/{device_name}",
}


class TemperatureScreen:
    def __init__(self) -> None:
        self._temp_sensor = PiicoDev_TMP117()
        self._display = create_PiicoDev_SSD1306()
        readings, self.device_id = self.load_state()
        self.readings = deque(readings, 7)

    @staticmethod
    def load_state() -> tuple[list[tuple[tuple[int, int, int, int, int, int, int], float]], int]:
        try:
            with open("temperature-screen_state.json") as stream:
                data = ujson.load(stream)
                return data["readings"], data["device_id"]
        except OSError as err:
            print("Error loading state:", err)
            return [], None

    def save_state(self) -> None:
        try:
            with open("temperature-screen_state.json", "w") as stream:
                ujson.dump({"readings": list(self.readings), "device_id": self.device_id}, stream)
        except OSError as err:
            print("Error saving state:", err)

    def create_device(self) -> int:
        body = {"name": device_name}
        response = urequests.post(url=f"{base_url}/api/devices", json=body, headers=headers)
        if response.status_code != 201:
            raise OSError(f"Failed to connect: {response.text}")
        data = response.json()
        return data["id"]

    def send_measurement(
        self, datetime: str, temperature: float = None, humidity: float = None
    ) -> None:
        body = {"timestamp": datetime, "temperature": temperature, "humidity": humidity}
        response = urequests.post(
            url=f"{base_url}/api/devices/{self.device_id}/readings", json=body, headers=headers
        )
        if response.status_code != 201:
            raise OSError(f"Failed to connect: {response.text}")

    def update_display(self) -> None:
        self._display.fill(0)
        previous_date = None
        index = 0
        for datetime, temperature in reversed(list(self.readings)):
            date = datetime[0], datetime[1], datetime[2]
            time = datetime[4], datetime[5], datetime[6]
            if previous_date != date:
                self._display.text(show_date(date=date, day_of_week=datetime[3]), 0, index, 1)
                index += 9
                if index + 8 > HEIGHT:
                    break
            previous_date = date
            self._display.text(f" {show_time(time=time)} - {temperature:0.2f}", 0, index, 1)
            index += 9
            if index + 8 > HEIGHT:
                break
        self._display.show()

    def update(self) -> None:
        print("Starting update of Temperature Screen")
        for module in (self._temp_sensor, self._display):
            try:
                print("Turning on PowerLED")
                module.pwrLED(True)
            except AttributeError:
                pass

        if not self.device_id:
            self.device_id = self.create_device()

        temperature = self._temp_sensor.readTempC()
        year, month, day, hour, minute, second, day_of_week, _ = get_datetime()
        self.readings.append(((year, month, day, day_of_week, hour, minute, second), temperature))
        self.save_state()
        datetime = f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}"
        self.send_measurement(datetime=datetime, temperature=temperature)
        self.update_display()

        for module in (self._temp_sensor, self._display):
            try:
                print("Turning off PowerLED")
                module.pwrLED(False)
            except AttributeError:
                pass
        print("Finished update of Temperature Screen")
