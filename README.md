# Bin Lights

![Micropython](https://img.shields.io/badge/Micropython-1.22.2-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Beta-yellowgreen?style=flat-square)

A micropython project to visually show what bins to put out each week.

## Components

- [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- [PiicoDev 3x RGB LED Module](https://core-electronics.com.au/piicodev-3x-rgb-led-module.html)
- [PiicoDev Cable](https://core-electronics.com.au/piicodev/cables.html)
- [PiicoDev Expansion Board for Pi Pico (Optional)](https://core-electronics.com.au/piicodev-lipo-expansion-board-for-raspberry-pi-pico.html)

## Installation

1. Download and load the [Micropython uf2](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) onto your Pico.
2. Install [mpremote](https://pypi.org/project/mpremote/).
3. Copy PiicoDev libraries:
    - mpremote cp [PiicoDev_Unified.py](https://github.com/CoreElectronics/CE-PiicoDev-Unified) :
    - mpremote cp [PiicoDev_RGB.py](https://github.com/CoreElectronics/CE-PiicoDev-RGB-LED-MicroPython-Module) :
4. Install external dependencies:
    - `mpremote mip install urequests`
5. Copy the config file to your device: `mpremote cp bin_lights/config.py :`
6. Update the `config.py` file with your settings: `mpremote edit config.py`
7. Copy the utils file to your device: `mpremote cp bin_lights/utils.py :`
8. Copy the main file to your device: `mpremote cp bin_lights/main.py :`
