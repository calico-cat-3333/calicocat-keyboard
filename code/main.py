print("Starting")

import microcontroller
# 超频到 150Mhz 或者也可以超频到 180Mhz
# 网上一些人声称可以超频到 250Mhz 但是我比较保守，暂时只打算超频到 150Mhz
# 警告：超频可能导致树莓派 pico 损坏，请注意小心
microcontroller.cpu.frequency = 150000000
# microcontroller.cpu.frequency = 180000000

import board
import os

from kb import KMKKeyboard
from kmk.keys import KC

from kmk.modules.layers import Layers
from kmk.modules.mouse_keys import MouseKeys
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.extensions.media_keys import MediaKeys

import user_animations
from lcd import LCD, display
from statuslcd import LCDLayerStatus, LCDLockStatus
from rgbstatuslcd import LCDRGBStatus
from calculator import LCDCalculator

keyboard = KMKKeyboard()

lcdscr = LCD(display)

# circuitpython 9 上需要进一步降低 refresh_rate
refresh_rate = 30
if os.uname().release[0] == '9':
    refresh_rate = 15

rgb = RGB(
    pixel_pin=board.GP28,
    num_pixels=86,
    val_limit=30,
    val_default=20,
    val_step=1,
    animation_speed=4,
    animation_mode=AnimationModes.USER,
    user_animation=user_animations.stream,
    refresh_rate=30
)
rgbkp = user_animations.RGBwithKeyProcerss(rgb)
# 添加 RGB_MODES_CYCLE / RGB_CYC 按键
# add RGB_MODES_CYCLE / RGB_CYC key
user_animations.init_rgb_modes_cycle_key(rgb)

keyboard.modules.append(Layers())
keyboard.modules.append(MouseKeys())
keyboard.modules.append(rgbkp)
keyboard.modules.append(LCDCalculator(lcdscr))
keyboard.extensions.append(rgb)
keyboard.extensions.append(lcdscr)
keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(LCDLockStatus(lcdscr))
keyboard.extensions.append(LCDLayerStatus(lcdscr))
keyboard.extensions.append(LCDRGBStatus(lcdscr, rgb))

keyboard.keymap = [[
    KC.ESC,  KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,  KC.PSCR, KC.INS,  KC.DEL,
    KC.GRV,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.MINS, KC.EQL,  KC.BSPC, KC.HOME,
    KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.LBRC, KC.RBRC, KC.BSLS, KC.END,
    KC.CAPS, KC.A,    KC.S,    KC.D,    KC.F,    KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT, KC.ENT,  KC.PGUP,
    KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.RSFT, KC.UP,   KC.PGDN,
    KC.LCTL, KC.MO(1),KC.LGUI, KC.LALT, KC.SPC,  KC.SPC,  KC.RALT, KC.APP,  KC.RCTL, KC.LEFT, KC.DOWN, KC.RGHT,
    KC.MUTE, KC.VOLU, KC.VOLD,
        ],[
    KC.ESC,  KC.MPRV,    KC.MPLY,    KC.MNXT, KC.RGB_TOG, KC.RGB_VAI, KC.RGB_VAD, KC.RGB_HUI, KC.RGB_HUD, KC.RGB_SAI, KC.RGB_SAD, KC.RGB_ANI,  KC.RGB_AND, KC.NLCK, KC.SLCK, KC.DEL,
    KC.GRV,  KC.RGB_RST, KC.RGB_CYC, KC.N3,   KC.N4,      KC.N5,      KC.N6,      KC.N7,      KC.N8,      KC.N9,      KC.N0,      KC.MINS,     KC.EQL,     KC.BSPC, KC.HOME,
    KC.TAB,  KC.Q,       KC.W,       KC.E,    KC.R,       KC.T,       KC.Y,       KC.U,       KC.I,       KC.O,       KC.P,       KC.LBRC,     KC.RBRC,    KC.BSLS, KC.END,
    KC.CAPS, KC.A,       KC.S,       KC.D,    KC.F,       KC.G,       KC.H,       KC.J,       KC.K,       KC.L,       KC.SCLN,    KC.QUOT,     KC.ENT,     KC.PGUP,
    KC.LSFT, KC.Z,       KC.X,       KC.C,    KC.V,       KC.B,       KC.N,       KC.M,       KC.COMM,    KC.DOT,     KC.SLSH,    KC.RSFT,     KC.UP,      KC.PGDN,
    KC.LCTL, KC.TRNS,    KC.LGUI,    KC.LALT, KC.TG(2),   KC.SPC,     KC.RALT,    KC.APP,     KC.RCTL,    KC.LCD_PRI, KC.DOWN,    KC.LCD_NXT,
    KC.MUTE, KC.BRIU,    KC.BRID,
        ],[
    KC.ESC,  KC.F1,    KC.F2,    KC.F3,    KC.F4,   KC.F5,   KC.F6,   KC.F7,     KC.F8,     KC.F9,     KC.F10,    KC.F11,  KC.F12,  KC.PSCR, KC.INS,  KC.DEL,
    KC.GRV,  KC.N1,    KC.N2,    KC.N3,    KC.N4,   KC.N5,   KC.N6,   KC.N7,     KC.N8,     KC.N9,     KC.N0,     KC.MINS, KC.EQL,  KC.BSPC, KC.HOME,
    KC.TAB,  KC.NONE,  KC.MS_UP, KC.NONE,  KC.NONE, KC.NONE, KC.NONE, KC.NONE,   KC.MW_UP,  KC.NONE,   KC.NONE,   KC.LBRC, KC.RBRC, KC.BSLS, KC.END,
    KC.CAPS, KC.MS_LT, KC.MS_DN, KC.MS_RT, KC.NONE, KC.NONE, KC.NONE, KC.MB_LMB, KC.MW_DN,  KC.MB_RMB, KC.MB_MMB, KC.NONE, KC.ENT,  KC.PGUP,
    KC.LSFT, KC.NONE,  KC.NONE,  KC.NONE,  KC.NONE, KC.NONE, KC.NONE, KC.NONE,   KC.NONE,   KC.NONE,   KC.NONE,   KC.RSFT, KC.UP,   KC.PGDN,
    KC.LCTL, KC.TRNS,  KC.LGUI,  KC.LALT,  KC.TRNS, KC.SPC,  KC.RALT, KC.APP,    KC.RCTL,   KC.LEFT,   KC.DOWN,   KC.RGHT,
    KC.MUTE, KC.VOLU, KC.VOLD,
        ]]

if __name__ == '__main__':
    #keyboard.debug_enabled = True
    keyboard.go()
