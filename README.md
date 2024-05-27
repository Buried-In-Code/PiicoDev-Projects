# PiicoDev Projects

![Micropython](https://img.shields.io/badge/Micropython-1.23.0-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Beta-yellowgreen?style=flat-square)

A Micropython project using a list of optional PiicoDev modules.
Each project is independent of each other so should work as long as dependencies are met.

## Components

- [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- [PiicoDev Expansion Board for Pi Pico (Optional)](https://core-electronics.com.au/piicodev-lipo-expansion-board-for-raspberry-pi-pico.html)
- [PiicoDev Cables](https://core-electronics.com.au/piicodev/cables.html)

### Bin Lights

- [PiicoDev 3x RGB LED Module](https://core-electronics.com.au/piicodev-3x-rgb-led-module.html)

### Temperature Screen

- [PiicoDev OLED Display Module](https://core-electronics.com.au/piicodev-oled-display-module-128x64-ssd1306.html)
- [PiicoDev Precision Temperature Sensor Module](https://core-electronics.com.au/piicodev-precision-temperature-sensor-tmp117.html)

## Installation

1. Download and load the [Micropython uf2](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) onto your Pico.
2. Install [mpremote](https://pypi.org/project/mpremote/).
3. Create a libs folder: `mkdir lib && cd lib`
4. Download necessary PiicoDev libraries: `wget <PiicoDev Library>`
5. Copy PiicoDev libraries to your device: `mpremote cp -r lib/ :`
6. Update `src/config.py` with your settings: `nano src/config.py`
7. Copy the src files to your device: `mpremote cp <src file> :`

### Bin Lights

Needed PiicoDev Libraries:

- [PiicoDev Unified](https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-Unified/main/PiicoDev_Unified.py)
- [PiicoDev 3x RGB LED](https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-RGB-LED-MicroPython-Module/main/PiicoDev_RGB.py)

Needed src files:

- [src/config.py](./src/config.py)
- [src/utils.py](./src/utils.py)
- [src/bin_lights.py](./src/bin_lights.py)
- [src/main.py](./src/main.py)

### Temperature Screen

Needed PiicoDev Libraries:

- [PiicoDev Unified](https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-Unified/main/PiicoDev_Unified.py)
- [PiicoDev Precision Temperature Sensor](https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-TMP117-MicroPython-Module/main/PiicoDev_TMP117.py)
- [PiicoDev OLED Display](https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-SSD1306-MicroPython-Module/main/PiicoDev_SSD1306.py)

Needed src files:

- [src/config.py](./src/config.py)
- [src/utils.py](./src/utils.py)
- [src/temperature_screen.py](./src/temperature_screen.py)
- [src/main.py](./src/main.py)
