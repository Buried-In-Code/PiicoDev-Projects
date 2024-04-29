from PiicoDev_RGB import PiicoDev_RGB

from utils import Bin, Day

ssid = "WIFI"
password = "PASSWORD"
timezone = "Pacific/Auckland"
rubbish_day = Day.THU
show_before = True
show_after = True
# fmt: off
modules = [
    PiicoDev_RGB(),
]
# fmt: on

rubbish = Bin(module=0, led=0, colour=[255, 0, 0])
recycling = Bin(module=0, led=1, colour=[255, 255, 0])
glass = Bin(module=0, led=2, colour=[0, 0, 255])
# fmt: off
bin_rotation = [
    (rubbish, recycling),
    (rubbish, glass),
]
# fmt: on
