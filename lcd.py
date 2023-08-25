import board
import terminalio
import displayio
import busio
import supervisor

from adafruit_display_text import label
from adafruit_st7789 import ST7789

from kmk.extensions.lock_status import LockStatus
from kmk.extensions import Extension

displayio.release_displays()

spi = busio.SPI(clock = board.GP2, MOSI = board.GP3)
tft_cs = board.GP29
tft_dc = board.GP5
tft_rs = board.GP4

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset = tft_rs)
display = ST7789(display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53)

splash = displayio.Group()
display.show(splash)

text_lock = label.Label(terminalio.FONT, text=' '*11, color=0xFFFFFF, scale=3, x=20, y=30, anchor_point=(0.0, 0.0))
text_layer = label.Label(terminalio.FONT, text=' '*11, color=0xFFFFFF, scale=3, x=20, y=70, anchor_point=(0.0, 0.0))
text_layer.text = 'Starting...'

splash.append(text_lock)
splash.append(text_layer)



class LCDLockStatus(LockStatus):
    def update_text(self):
        at = supervisor.ticks_ms()
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
        text_lock.text = s
        print('lock status timeuse:',supervisor.ticks_ms()-at)

    def after_hid_send(self, sandbox):
        super().after_hid_send(sandbox)  # Critically important. Do not forget
        if self.report_updated:
            self.update_text()

class LCDLayerStatus(Extension):
    def __init__(self, prompt='Layer: ', layer_names=None):
        self._onscreen_layer = -1
        self.prompt = prompt
        self.layer_names = layer_names

    def update_text(self, layer):
        s = self.prompt
        if self.layer_names == None:
            s += str(layer)
        else:
            s += self.layer_names[layer]
        text_layer.text = s

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):
        return

    def before_matrix_scan(self, sandbox):
        return

    def after_matrix_scan(self, sandbox):
        if self._onscreen_layer != sandbox.active_layers[0]:
            at = supervisor.ticks_ms()
            self.update_text(sandbox.active_layers[0])
            self._onscreen_layer = sandbox.active_layers[0]
            print('layer status timeuse:',supervisor.ticks_ms()-at)

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return
