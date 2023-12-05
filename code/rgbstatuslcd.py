import board
import terminalio
import displayio
import supervisor
from adafruit_display_text import label

from kmk.extensions import Extension
from kmk.extensions.RGB import AnimationModes

import user_animations
from gettime import get_time

# 部分灯效的hue值经常改变，导致屏幕刷新过于频繁占用很多时间，并导致操作延迟
# 此列表中的灯效不会经常改变的hue
hue_whitelist = [
    AnimationModes.STATIC,
    AnimationModes.STATIC_STANDBY,
    AnimationModes.BREATHING,
    AnimationModes.KNIGHT
]
# 用户自定义灯效中不会经常改变hue的灯效列表
hue_whitelist_user = [
    user_animations.brightens_when_pressed,
    user_animations.dims_when_pressed
]

class LCDRGBStatus(Extension):
    def __init__(self, lcd, rgb):
        self.lcd = lcd
        self.rgb = rgb
        self.font = terminalio.FONT
        self.color = 0xffffff
        self.info = [True, -1, -1, -1, -1, -1, None, None]

    #@get_time
    def update_text(self):
        if not bool(self.rgb.enable) == self.info[0]:
            if self.rgb.enable:
                self.rgb_enable_text.text = 'RGB ON'
            else:
                self.rgb_enable_text.text = 'RGB OFF'
            self.info[0] = bool(self.rgb.enable)
            print(self.info,self.rgb.enable)

        if not self.rgb.hue == self.info[1]:
            if self.rgb.animation_mode in hue_whitelist:
                self.rgb_hue_text.text = 'Hue: '+str(self.rgb.hue)
                self.info[1] = self.rgb.hue
                self.info[7] = None
            elif self.rgb.animation_mode == AnimationModes.USER:
                if self.rgb.user_animation in hue_whitelist_user:
                    self.rgb_hue_text.text = 'Hue: '+str(self.rgb.hue)
                    self.info[1] = self.rgb.hue
                elif not self.info[7] == self.rgb.user_animation:
                    self.rgb_hue_text.text = 'Hue: ---'
                    self.info[1] = -1
                    self.info[7] = self.rgb.user_animation
            elif not self.info[7] == self.rgb.animation_mode:
                self.rgb_hue_text.text = 'Hue: ---'
                self.info[1] = -1
                self.info[7] = self.rgb.animation_mode

        if not self.rgb.sat == self.info[2]:
            self.rgb_sat_text.text = 'Sat: '+str(self.rgb.sat)
            self.info[2] = self.rgb.sat

        if not self.rgb.val == self.info[3]:
            self.rgb_val_text.text = 'Val: '+str(self.rgb.val)
            self.info[3] = self.rgb.val

        if not self.rgb.animation_speed == self.info[4]:
            self.rgb_speed_text.text = 'Speed: '+str(self.rgb.animation_speed)
            self.info[4] = self.rgb.animation_speed

        if not (self.rgb.animation_mode == self.info[5] and self.rgb.user_animation == self.info[6]):
            self.info[5] = self.rgb.animation_mode
            self.info[6] = self.rgb.user_animation
            self.animation_text.scale = 2
            if self.rgb.animation_mode == AnimationModes.STATIC:
                self.animation_text.text = 'STATIC'
            elif self.rgb.animation_mode == AnimationModes.STATIC_STANDBY:
                self.animation_text.text = 'STATIC'
            elif self.rgb.animation_mode == AnimationModes.BREATHING:
                self.animation_text.text = 'BREATHING'
            elif self.rgb.animation_mode == AnimationModes.RAINBOW:
                self.animation_text.text = 'RAINBOW'
            elif self.rgb.animation_mode == AnimationModes.BREATHING_RAINBOW:
                self.animation_text.text = 'BREATHING_RAINBOW'
            elif self.rgb.animation_mode == AnimationModes.KNIGHT:
                self.animation_text.text = 'KNIGHT'
            elif self.rgb.animation_mode == AnimationModes.SWIRL:
                self.animation_text.text = 'SWIRL'
            elif self.rgb.animation_mode == AnimationModes.USER:
                animation_name = str(self.rgb.user_animation).split(' ')[1]
                if len(animation_name) > 18:
                    self.animation_text.scale = 1
                self.animation_text.text = animation_name

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):
        self.group = self.lcd.add_group()
        self.rgb_enable_text = label.Label(self.font, text='RGB ON ', color=self.color, scale=2, x=10, y=10, anchor_point=(0.0, 0.0))
        self.rgb_hue_text = label.Label(self.font, text='Hue:    ', color=self.color, scale=2, x=10, y=32, anchor_point=(0.0, 0.0))
        self.rgb_sat_text = label.Label(self.font, text='Sat:    ', color=self.color, scale=2, x=10, y=54, anchor_point=(0.0, 0.0))
        self.rgb_val_text = label.Label(self.font, text='Val:    ', color=self.color, scale=2, x=10, y=76, anchor_point=(0.0, 0.0))
        self.rgb_speed_text = label.Label(self.font, text='Speed:    ', color=self.color, scale=2, x=10, y=98, anchor_point=(0.0, 0.0))
        self.animation_text = label.Label(self.font, text=' '*36, color=self.color, scale=2, x=10, y=120, anchor_point=(0.0, 0.0))

        self.group.append(self.rgb_enable_text)
        self.group.append(self.rgb_hue_text)
        self.group.append(self.rgb_sat_text)
        self.group.append(self.rgb_val_text)
        self.group.append(self.rgb_speed_text)
        self.group.append(self.animation_text)

    def before_matrix_scan(self, sandbox):
        return

    def after_matrix_scan(self, sandbox):
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        if self.lcd.group_on_showing(self.group):
            self.update_text()

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return
