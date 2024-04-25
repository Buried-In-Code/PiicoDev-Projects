from PiicoDev_RGB import PiicoDev_RGB

from bin import Bin

ssid = "WIFI"
password = "PASSWORD"
timezone = "Pacific/Auckland"
# fmt: off
modules = [
    PiicoDev_RGB()
]
# fmt: on

rubbish = Bin(module_index=0, light_index=0, colour=[255, 0, 0])
recycling = Bin(module_index=0, light_index=1, colour=[255, 255, 0])
glass = Bin(module_index=0, light_index=2, colour=[0, 0, 255])
# fmt: off
weekly_options = [
    (rubbish, recycling),
    (rubbish, glass)
]
# fmt: on
