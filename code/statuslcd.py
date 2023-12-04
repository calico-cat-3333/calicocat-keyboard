import board
import displayio
import supervisor

from kmk.extensions.lock_status import LockStatus
from kmk.extensions import Extension

bitmap = displayio.OnDiskBitmap("spritemap.bmp")
palette = bitmap.pixel_shader
palette.make_transparent(0)

class LCDLockStatus(LockStatus):
    def __init__(self, lcd):
        super().__init__()
        self.lcd = lcd

    def during_bootup(self, sandbox):
        super().during_bootup(sandbox)

        self.group_lock = displayio.Group(scale=3, x=20, y=10)
        self.tilegrid_numlock = displayio.TileGrid(bitmap, pixel_shader=palette,
                                              tile_width=16, tile_height=16, default_tile=7, x=0, y=0)
        self.tilegrid_caplock = displayio.TileGrid(bitmap, pixel_shader=palette,
                                              tile_width=16, tile_height=16, default_tile=3, x=20, y=0)
        self.tilegrid_scrlock = displayio.TileGrid(bitmap, pixel_shader=palette,
                                              tile_width=16, tile_height=16, default_tile=11, x=40, y=0)

        self.group_lock.append(self.tilegrid_numlock)
        self.group_lock.append(self.tilegrid_caplock)
        self.group_lock.append(self.tilegrid_scrlock)
        self.lcd.default_group.append(self.group_lock)

    def update_text(self):
        if self.get_num_lock():
            self.tilegrid_numlock[0] = 0
        else:
            self.tilegrid_numlock[0] = 7
        if self.get_caps_lock():
            self.tilegrid_caplock[0] = 1
        else:
            self.tilegrid_caplock[0] = 3
        if self.get_scroll_lock():
            self.tilegrid_scrlock[0] = 2
        else:
            self.tilegrid_scrlock[0] = 11

    def after_hid_send(self, sandbox):
        super().after_hid_send(sandbox)  # Critically important. Do not forget
        if self.report_updated:
            #at = supervisor.ticks_ms()
            self.update_text()
            #print('lock status timeuse:',supervisor.ticks_ms()-at)

class LCDLayerStatus(Extension):
    def __init__(self, lcd):
        self._onscreen_layer = -1
        self.lcd = lcd

    def update_text(self, layer):
        if layer in [0, 1, 2]:
            self.tilegrid_layer[0] = layer + 4
        else:
            self.tilegrid_layer[0] = 4

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):
        self.group_layer = displayio.Group(scale=3, x=20, y=70)
        self.tilegrid_layer = displayio.TileGrid(bitmap, pixel_shader=palette,
                                                 tile_width=16, tile_height=16, default_tile=4, x=0, y=0)
        self.tilegrid_cat = displayio.TileGrid(bitmap, pixel_shader=palette,
                                               width=2, tile_width=16, tile_height=16, x=30, y=0)
        self.tilegrid_cat[0] = 8
        self.tilegrid_cat[1] = 9
        self.group_layer.append(self.tilegrid_layer)
        self.group_layer.append(self.tilegrid_cat)
        self.lcd.default_group.append(self.group_layer)

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
