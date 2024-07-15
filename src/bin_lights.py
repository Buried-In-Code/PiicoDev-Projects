import ujson

from clock import Clock
from config import bin_rotation, light_modules, show_lights
from utils import Bin


class BinLights:
    def __init__(self, clock: Clock) -> None:
        self._clock = clock
        self._modules = light_modules
        self._bin_rotation = bin_rotation
        self._show_lights = show_lights
        self.last_updated, self.index = self.load_state()

    @staticmethod
    def load_state() -> tuple[int, int]:
        try:
            with open("bin-lights_state.json") as stream:
                data = ujson.load(stream)
                return data["last_updated"], data["index"]
        except OSError as err:
            print("Error loading state:", err)
            return None, 0

    def save_state(self) -> None:
        try:
            with open("bin-lights_state.json", "w") as stream:
                ujson.dump({"last_updated": self.last_updated, "index": self.index}, stream)
        except OSError as err:
            print("Error saving state:", err)

    def update(self) -> None:
        print("Starting update of Bin Lights")
        for module in self._modules:
            print("Turning on PowerLED")
            module.pwrLED(True)

        day_of_week, week_number = self._clock.calculate_days()
        if week_number is not None:
            if self.last_updated is not None and week_number != self.last_updated:
                self.index = 1 - self.index
            self.last_updated = week_number
            self.save_state()
        if day_of_week is not None:
            if day_of_week in self._show_lights:
                self.enable_lights(bins=self._bin_rotation[self.index])
            else:
                self.disable_lights()

        for module in self._modules:
            print("Turning off PowerLED")
            module.pwrLED(False)
        print("Finished update of Bin Lights")

    def enable_lights(self, bins: list[Bin]) -> None:
        self.disable_lights()
        for bin in bins:  # noqa: A001
            self._modules[bin.module].setPixel(bin.led, bin.colour)
        for module in self._modules:
            module.show()

    def disable_lights(self) -> None:
        for module in self._modules:
            module.clear()
            module.show()
