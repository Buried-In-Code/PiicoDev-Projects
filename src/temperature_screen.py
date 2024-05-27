import ujson
from ucollections import deque

from PiicoDev_SSD1306 import HEIGHT, create_PiicoDev_SSD1306
from PiicoDev_TMP117 import PiicoDev_TMP117

from utils import calculate_date, calculate_time, show_date, show_time


class TemperatureScreen:
    def __init__(self) -> None:
        self._temp_sensor = PiicoDev_TMP117()
        self._display = create_PiicoDev_SSD1306()
        self.last_updated, readings = self.load_state()
        self.readings = deque(readings, 7)

        self.update_display()

    @staticmethod
    def load_state() -> tuple[int, list[tuple[tuple[int, int, int, int, int, int, int], float]]]:
        try:
            with open("temperature-screen_state.json") as stream:
                data = ujson.load(stream)
                return data["last_updated"], data["readings"]
        except (OSError, ValueError) as err:
            print("Error loading state:", err)
            return (), []

    def save_state(self) -> None:
        try:
            with open("temperature-screen_state.json", "w") as stream:
                ujson.dump(
                    {"last_updated": self.last_updated, "readings": list(self.readings)}, stream
                )
        except (OSError, ValueError) as err:
            print("Error saving state:", err)

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
                module.pwrLED(True)
                print("Turning on PowerLED")
            except AttributeError:
                pass

        temperature = self._temp_sensor.readTempC()
        current_date = calculate_date()
        current_time = calculate_time()
        self.readings.append(
            (
                (
                    current_date[0],
                    current_date[1],
                    current_date[2],
                    current_date[3],
                    current_time[0],
                    current_time[1],
                    current_time[2],
                ),
                temperature,
            )
        )
        self.save_state()
        self.update_display()

        for module in (self._temp_sensor, self._display):
            try:
                module.pwrLED(False)
                print("Turning off PowerLED")
            except AttributeError:
                pass
        print("Finished update of Temperature Screen")
