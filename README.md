# PiicoDev Projects

![Micropython](https://img.shields.io/badge/Micropython-1.23.0-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Beta-yellowgreen?style=flat-square)

A Micropython project using a list of optional PiicoDev modules.
Each project is independent of each other so should work as long as dependencies are met.

## Projects

### Bin Lights

Visually show what bins to put out each week.

#### Components

- [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- [PiicoDev Expansion Board for Pi Pico (Optional)](https://core-electronics.com.au/piicodev-lipo-expansion-board-for-raspberry-pi-pico.html)
- [PiicoDev Cables](https://core-electronics.com.au/piicodev/cables.html)
- [PiicoDev 3x RGB LED Module](https://core-electronics.com.au/piicodev-3x-rgb-led-module.html)

#### Installation

1. Download and load the [Micropython uf2](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) onto your Pico.
2. Install [mpremote](https://pypi.org/project/mpremote/).
3. Create a lib folder: `mkdir lib`
4. Download the PiicoDev Unified library: `wget https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-Unified/main/PiicoDev_Unified.py -O lib/PiicoDev_Unified.py`
5. Download the PiicoDev 3x RGB LED library: `wget https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-RGB-LED-MicroPython-Module/main/PiicoDev_RGB.py -O lib/PiicoDev_RGB.py`
6. Copy the libraries to your device: `mpremote cp -r lib/ :`
7. Copy the src files to your device: `mpremote cp src/config.py src/bin_lights.py src/utils.py :`
8. Update the `config.py` file with your settings: `mpremote edit config.py`
9. Copy the main file device: `mpremote cp src/main.py :`

### Temperature Screen

Record the temperature, display it and send the reading to [Freyr](https://github.com/Buried-In-Code/Freyr)

#### Components

- [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- [PiicoDev Expansion Board for Pi Pico (Optional)](https://core-electronics.com.au/piicodev-lipo-expansion-board-for-raspberry-pi-pico.html)
- [PiicoDev Cables](https://core-electronics.com.au/piicodev/cables.html)
- [PiicoDev OLED Display Module](https://core-electronics.com.au/piicodev-oled-display-module-128x64-ssd1306.html)
- [PiicoDev Precision Temperature Sensor Module](https://core-electronics.com.au/piicodev-precision-temperature-sensor-tmp117.html)

### Installation

01. Download and load the [Micropython uf2](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) onto your Pico.
02. Install [mpremote](https://pypi.org/project/mpremote/).
03. Install external dependencies: `mpremote mip install urequests`
04. Create a lib folder: `mkdir lib`
05. Download the PiicoDev Unified library: `wget https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-Unified/main/PiicoDev_Unified.py -O lib/PiicoDev_Unified.py`
06. Download the PiicoDev OLED Display library: `wget https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-SSD1306-MicroPython-Module/main/PiicoDev_SSD1306.py -O lib/PiicoDev_SSD1306.py`
07. Download the PiicoDev Precision Temperature Sensor library: `wget https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-TMP117-MicroPython-Module/main/PiicoDev_TMP117.py -O lib/PiicoDev_TMP117.py`
08. Copy the libraries to your device: `mpremote cp -r lib/ :`
09. Copy the src files to your device: `mpremote cp src/config.py src/temperature_screen.py src/utils.py :`
10. Update the `config.py` file with your settings: `mpremote edit config.py`
11. Copy the main file device: `mpremote cp src/main.py :`
