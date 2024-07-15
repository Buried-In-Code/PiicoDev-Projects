# Common
ssid = "WIFI"
password = "PASSWORD"
offset = +12

# Bin Lights
from PiicoDev_RGB import PiicoDev_RGB
from utils import Bin, Day

show_lights = (Day.WED, Day.THU, Day.FRI)
light_modules = [
    PiicoDev_RGB(bright=5),
]
rubbish = Bin(module=0, led=0, colour=[255, 0, 0])
recycling = Bin(module=0, led=1, colour=[255, 255, 0])
glass = Bin(module=0, led=2, colour=[0, 0, 255])
bin_rotation = [
    (rubbish, recycling),
    (rubbish, glass),
]
