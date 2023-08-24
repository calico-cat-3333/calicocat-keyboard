import board
import terminalio
import displayio
import busio
import supervisor

from adafruit_display_text import label
from adafruit_st7789 import ST7789

from kmk.extensions.lock_status import LockStatus

displayio.release_displays()

spi = busio.SPI(clock = board.GP2, MOSI = board.GP3)
tft_cs = board.GP29
tft_dc = board.GP5
tft_rs = board.GP4

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset = tft_rs, baudrate=40000000)
display = ST7789(display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53)

splash = displayio.Group()
display.show(splash)

FONTSCALE = 2
text_area = label.Label(terminalio.FONT, text=' '*11, color=0xFFFFFF)
text_width = text_area.bounding_box[2] * FONTSCALE
text_group = displayio.Group(scale=FONTSCALE, x=20, y=30)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)


class LCDLockStatus(LockStatus):
    def update_lcd(self):
        s = ''
        if self.get_num_lock():
            s += '[1]'
        else:
            s += '[ ]'
        s += ' '
        if self.get_caps_lock():
            s += '[A]'
        else:
            s += '[a]'
        s += ' '
        if self.get_scroll_lock():
            s += '[S]'
        else:
            s += '[ ]'
        text_area.text = s

    def after_hid_send(self, sandbox):
        super().after_hid_send(sandbox)  # Critically important. Do not forget
        if self.report_updated:
            self.update_lcd()
