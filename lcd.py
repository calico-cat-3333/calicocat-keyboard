import board
import terminalio
import displayio
import busio
import supervisor

from adafruit_display_text import label
from adafruit_st7789 import ST7789

from kmk.extensions.lock_status import LockStatus
from kmk.extensions import Extension

bitmap = displayio.OnDiskBitmap("spritemap.bmp")
palette = bitmap.pixel_shader
palette.make_transparent(0)

displayio.release_displays()

spi = busio.SPI(clock = board.GP2, MOSI = board.GP3)
tft_cs = board.GP29
tft_dc = board.GP5
tft_rs = board.GP4

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset = tft_rs)
display = ST7789(display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53)

splash = displayio.Group()

group_lock = displayio.Group(scale=3, x=20, y=10)
tilegrid_numlock = displayio.TileGrid(bitmap, pixel_shader=palette, tile_width=16, tile_height=16, default_tile=7, x=0, y=0)
tilegrid_caplock = displayio.TileGrid(bitmap, pixel_shader=palette, tile_width=16, tile_height=16, default_tile=7, x=20, y=0)
tilegrid_scrlock = displayio.TileGrid(bitmap, pixel_shader=palette, tile_width=16, tile_height=16, default_tile=7, x=40, y=0)

group_layer = displayio.Group(scale=3, x=20, y=70)
tilegrid_layer = displayio.TileGrid(bitmap, pixel_shader=palette, tile_width=16, tile_height=16, default_tile=4, x=0, y=0)
tilegrid_cat = displayio.TileGrid(bitmap, pixel_shader=palette, width=2, tile_width=16, tile_height=16, x=30, y=0)
tilegrid_cat[0] = 8
tilegrid_cat[1] = 9


class LCDLockStatus(LockStatus):
    def update_text(self):
        if self.get_num_lock():
            tilegrid_numlock[0] = 0
        else:
            tilegrid_numlock[0] = 7
        if self.get_caps_lock():
            tilegrid_caplock[0] = 1
        else:
            tilegrid_caplock[0] = 3
        if self.get_scroll_lock():
            tilegrid_scrlock[0] = 2
        else:
            tilegrid_scrlock[0] = 7

    def after_hid_send(self, sandbox):
        super().after_hid_send(sandbox)  # Critically important. Do not forget
        if self.report_updated:
            #at = supervisor.ticks_ms()
            self.update_text()
            #print('lock status timeuse:',supervisor.ticks_ms()-at)

class LCDLayerStatus(Extension):
    def __init__(self):
        self._onscreen_layer = -1

    def update_text(self, layer):
        if layer in [0, 1, 2]:
            tilegrid_layer[0] = layer + 4
        else:
            tilegrid_layer[0] = 4

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):
        group_lock.append(tilegrid_numlock)
        group_lock.append(tilegrid_caplock)
        group_lock.append(tilegrid_scrlock)
        group_layer.append(tilegrid_layer)
        group_layer.append(tilegrid_cat)
        splash.append(group_lock)
        splash.append(group_layer)
        display.show(splash)

    def before_matrix_scan(self, sandbox):
        return

    def after_matrix_scan(self, sandbox):
        if self._onscreen_layer != sandbox.active_layers[0]:
            #at = supervisor.ticks_ms()
            self.update_text(sandbox.active_layers[0])
            self._onscreen_layer = sandbox.active_layers[0]
            #print('layer status timeuse:',supervisor.ticks_ms()-at)

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return
