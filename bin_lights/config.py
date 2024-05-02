from PiicoDev_RGB import PiicoDev_RGB
from utils import Bin, Day

ssid = "WIFI"
password = "PASSWORD"
timezone = "Pacific/Auckland"
show_lights = [Day.WED, Day.THU, Day.FRI]
modules = [
    PiicoDev_RGB(bright=10),
]
rubbish = Bin(module=0, led=0, colour=[255, 0, 0])
recycling = Bin(module=0, led=1, colour=[255, 255, 0])
glass = Bin(module=0, led=2, colour=[0, 0, 255])
bin_rotation = [
    (rubbish, recycling),
    (rubbish, glass),
]
