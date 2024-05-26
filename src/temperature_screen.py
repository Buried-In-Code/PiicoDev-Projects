import ujson
from collections import deque

from PiicoDev_SSD1306 import HEIGHT, WIDTH, create_PiicoDev_SSD1306
from PiicoDev_TMP117 import PiicoDev_TMP117

from utils import get_current_datetime


class TempDisplay:
    def __init__(self) -> None:
        self._temp_sensor = PiicoDev_TMP117()
        self._display = create_PiicoDev_SSD1306()
        self._graph = self._display.graph2D(minvalue=-10, maxvalue=40, height=HEIGHT - 18)
        self.readings = deque(maxlen=WIDTH / 4)
        self.last_updated, readings = self.load_state()
        self.readings.extend(readings)
        for datetime, reading in self.readings:
            self.update_display(datetime=datetime, temperature=reading)

    @staticmethod
    def load_state() -> tuple[int, list[tuple[tuple[int, int, int, int, int, int], float]]]:
        try:
            with open("temp-display_state.json") as stream:
                data = ujson.load(stream)
                return data["last_updated"], data["readings"]
        except OSError as err:
            print("Error loading state:", err)
            return None, []

    def save_state(self) -> None:
        try:
            with open("temp-display_state.json", "w") as stream:
                ujson.dump({"last_updated": self.last_updated, "readings": self.readings}, stream)
        except OSError as err:
            print("Error saving state:", err)

    def update_display(
        self, datetime: tuple[int, int, int, int, int, int], temperature: float
    ) -> None:
        self._display.fill(0)
        self._display.text(self.show_date(datetime=datetime), 0, 0, 1)
        self._display.text(self.show_time(datetime=datetime), 0, 9, 1)
        self._display.updateGraph2D(self._graph, temperature)
        self._display.hline(0, (HEIGHT - 18) / 5 * 4, WIDTH, 1)
        self._display.show()

    def update(self) -> None:
        for module in (self._temp_sensor, self._display):
            module.pwrLED(True)

        temperature = self._temp_sensor.readTempC()
        current_date = get_current_datetime()
        self.readings.append((current_date, temperature))
        self.save_state()
        self.update_display(datetime=current_date, temperature=temperature)

        for module in (self._temp_sensor, self._display):
            module.pwrLED(False)
