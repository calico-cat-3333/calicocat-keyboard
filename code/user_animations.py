from kmk.keys import make_key
from kmk.extensions.RGB import AnimationModes
from kmk.handlers.stock import passthrough as handler_passthrough

import supervisor

# animations
stream_info = [0, 0] # first led color, led index
def stream(rgb):
    for i in range(20):
        led_color = (stream_info[0] + rgb.hue_step * stream_info[1]) % 256
        rgb.set_hsv(led_color, rgb.sat, rgb.val, stream_info[1])
        stream_info[1] = (stream_info[1] + 1) % rgb.num_pixels
        if stream_info[1] == 0:
            stream_info[0] = (stream_info[0] + 1) % 256

# 添加 RGB_MODES_CYCLE / RGB_CYC 按键，暂时放这
# add RGB_MODES_CYCLE / RGB_CYC key
def init_rgb_modes_cycle_key(rgb):
    rgb_modes_list = [
        AnimationModes.STATIC,
        AnimationModes.BREATHING,
        AnimationModes.RAINBOW,
        AnimationModes.BREATHING_RAINBOW,
        AnimationModes.KNIGHT,
        AnimationModes.SWIRL,
        AnimationModes.USER
    ]
    rgb_modes_num = len(rgb_modes_list)
    def rgb_modes_cycle(*args, **kwargs):
        rgb.effect_init = True
        rgb_mode_index = 0
        if rgb.animation_mode == AnimationModes.STATIC_STANDBY:
            rgb_mode_index = 0
        else:
            rgb_mode_index = rgb_modes_list.index(rgb.animation_mode)
        rgb_mode_index = (rgb_mode_index + 1) % rgb_modes_num
        rgb.animation_mode = rgb_modes_list[rgb_mode_index]
    make_key(
        names=('RGB_MODES_CYCLE', 'RGB_CYC'),
        on_press=rgb_modes_cycle,
        on_release=handler_passthrough,
    )
