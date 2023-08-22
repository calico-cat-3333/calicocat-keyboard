print("Starting")

import board

from kb import KMKKeyboard
from kmk.keys import KC

from kmk.modules.layers import Layers
from kmk.modules.mouse_keys import MouseKeys
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.extensions.media_keys import MediaKeys

keyboard = KMKKeyboard()
rgb = RGB(pixel_pin=board.GP28, num_pixels=86, val_limit = 10, val_step = 1, animation_mode=AnimationModes.RAINBOW)

keyboard.modules.append(Layers())
keyboard.modules.append(MouseKeys())
keyboard.extensions.append(rgb)
keyboard.extensions.append(MediaKeys())

keyboard.keymap = [[
    KC.ESC,  KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,  KC.PSCR, KC.INS,  KC.DEL,
    KC.GRV,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.MINS, KC.EQL,  KC.BSPC, KC.HOME,
    KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.LBRC, KC.RBRC, KC.BSLS, KC.END,
    KC.CAPS, KC.A,    KC.S,    KC.D,    KC.F,    KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT, KC.ENT,  KC.PGUP,
    KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.RSFT, KC.UP,   KC.PGDN,
    KC.LCTL, KC.MO(1),KC.LGUI, KC.LALT, KC.SPC,  KC.SPC,  KC.RALT, KC.APP,  KC.RCTL, KC.LEFT, KC.DOWN, KC.RGHT,
    KC.MUTE, KC.VOLD, KC.VOLU,
        ],[
    KC.ESC,  KC.MPRV, KC.MSTP, KC.MNXT, KC.RGB_TOG, KC.RGB_VAI, KC.RGB_VAD,   KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,  KC.PSCR, KC.INS,  KC.DEL,
    KC.GRV,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.MINS, KC.EQL,  KC.BSPC, KC.HOME,
    KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.LBRC, KC.RBRC, KC.BSLS, KC.END,
    KC.CAPS, KC.A,    KC.S,    KC.D,    KC.F,    KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT, KC.ENT,  KC.PGUP,
    KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.RSFT, KC.UP,   KC.PGDN,
    KC.LCTL, KC.TRNS, KC.LGUI, KC.LALT, KC.SPC,  KC.SPC,  KC.RALT, KC.APP,  KC.RCTL, KC.LEFT, KC.DOWN, KC.RGHT,
    KC.MUTE, KC.BRID, KC.BRIU,
        ]]

if __name__ == '__main__':
    keyboard.debug_enabled = True
    keyboard.go()
