import board
import displayio
import busio

# 兼容 circuitpython 8 和 circuitpython 9
try:
    from fourwire import FourWire
    print('use fourwire module on circuitpython 9')
except:
    from displayio import FourWire
    print('use displayio module on circuitpython 8')

from adafruit_st7789 import ST7789

from kmk.extensions import Extension
from kmk.keys import make_key
from kmk.handlers.stock import passthrough as handler_passthrough

displayio.release_displays()

spi = busio.SPI(clock = board.GP2, MOSI = board.GP3)
while not spi.try_lock():
    pass
spi.configure(baudrate=24000000) # Configure SPI for 24MHz
spi.unlock()

tft_cs = board.GP29
tft_dc = board.GP5
tft_rs = board.GP4

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset = tft_rs)
display = ST7789(display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53)

# LCD 扩展基础，提供多功能切换，其对象将作为参数传入LCD功能扩展类
# 本身只需要一个参数，dsiplay, 是 displayio.Display 对象
class LCD(Extension):
    def __init__(self, display):
        self.display = display
        self.group_list = []
        self.default_group = displayio.Group()
        self.group_list.append(self.default_group)

        make_key(
            names=('LCD_GROUP_NEXT', 'LCD_NXT'),
            on_press=self._lcd_group_next,
            on_release=handler_passthrough,
        )
        make_key(
            names=('LCD_GROUP_PRIV', 'LCD_PRI'),
            on_press=self._lcd_group_priv,
            on_release=handler_passthrough,
        )

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):
        self.show(self.default_group)

    def before_matrix_scan(self, sandbox):
        return

    def after_matrix_scan(self, sandbox):
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return

    def show(self, group=None):
        # displayio.Display.show() 即将被删除所以写这个函数作为替代
        if group == None:
            self.display.root_group = self.default_group
        else:
            self.display.root_group = group

    def _lcd_group_next(self, *args, **kwargs):
        group_index = self.group_list.index(self.display.root_group)
        group_index = (group_index + 1) % len(self.group_list)
        self.show(self.group_list[group_index])

    def _lcd_group_priv(self, *args, **kwargs):
        group_index = self.group_list.index(self.display.root_group)
        group_index = (group_index - 1) % len(self.group_list)
        self.show(self.group_list[group_index])

    def add_group(self):
        new_group = displayio.Group()
        self.group_list.append(new_group)
        return new_group

    # 检查当前是否在显示这个 group
    # 除了内置直接显示在 defalut_group 上的模块外，所有 LCD 功能模块都应该进行这一检查
    # 如果没有显示，那么函数将直接退出，不进行任何操作
    def group_on_showing(self, group):
        if group == self.display.root_group:
            return True
        return False
