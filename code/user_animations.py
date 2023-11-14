from kmk.keys import make_key
from kmk.extensions.RGB import AnimationModes
from kmk.handlers.stock import passthrough as handler_passthrough

import supervisor

# 将电路上的rgb排列转换为更常见的排列
rgb_index = [
    [15,14,13,12,11,10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
    [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    [45,44,43,42,41,40,39,38,37,36,35,34,33,32,31],
    [46,47,48,49,50,51,52,53,54,55,56,57,58,59],
    [73,72,71,70,69,68,67,66,65,64,63,62,61,60],
    [74,75,76,77,78,79,80,81,82,83,84,85]
]

# animations
# 彩色流光灯效  stream animation
def stream(rgb):
    for i in range(rgb.num_pixels):
        rgb.set_hsv((rgb.hue + rgb.hue_step * i) % 256, rgb.sat, rgb.val, i)
    rgb.increase_hue(rgb._step)

# 纵向彩色流光灯效  vertical stream animation
def vertical_stream(rgb):
    for j in range(0,len(rgb_index)):
        for i in range(0, len(rgb_index[j])):
            rgb.set_hsv(
                rgb.hue + j * rgb.hue_step,
                rgb.sat,
                rgb.val,
                rgb_index[j][i]
            )
    rgb.increase_hue(rgb._step)

# 横向彩色流光灯效  horizontal stream animation
# 推荐 hue_step: 20  recommended hue_step: 20
def horizontal_stream(rgb):
    for j in range(0,len(rgb_index)):
        for i in range(0, len(rgb_index[j])):
            rgb.set_hsv(
                rgb.hue + i * rgb.hue_step,
                rgb.sat,
                rgb.val,
                rgb_index[j][i]
            )
    rgb.increase_hue(rgb._step)



# 添加 RGB_MODES_CYCLE / RGB_CYC 按键，暂时放这
# add RGB_MODES_CYCLE / RGB_CYC key
def init_rgb_modes_cycle_key(rgb):
    rgb_modes_list = [
        AnimationModes.STATIC,
        AnimationModes.BREATHING,
        AnimationModes.RAINBOW,
        AnimationModes.BREATHING_RAINBOW,
        AnimationModes.KNIGHT,
        AnimationModes.SWIRL
    ]
    user_animation_list = [
        stream,
        vertical_stream,
        horizontal_stream
    ]
    if not user_animation_list == []:
        rgb_modes_list.append(AnimationModes.USER)
        if rgb.user_animation == None:
            rgb.user_animation = user_animation_list[0]
    rgb_modes_num = len(rgb_modes_list)
    user_animation_num = len(user_animation_list)

    def rgb_modes_cycle(*args, **kwargs):
        rgb.effect_init = True
        rgb_mode_index = 0
        if rgb.animation_mode == AnimationModes.STATIC_STANDBY:
            rgb_mode_index = rgb_modes_list.index(AnimationModes.STATIC)
        else:
            rgb_mode_index = rgb_modes_list.index(rgb.animation_mode)

        if rgb.animation_mode == AnimationModes.USER:
            user_animation_index = (user_animation_list.index(rgb.user_animation) + 1) % user_animation_num
            rgb.user_animation = user_animation_list[user_animation_index]
            if not user_animation_index == 0:
                rgb_mode_index = rgb_mode_index - 1

        rgb_mode_index = (rgb_mode_index + 1) % rgb_modes_num
        rgb.animation_mode = rgb_modes_list[rgb_mode_index]

    make_key(
        names=('RGB_MODES_CYCLE', 'RGB_CYC'),
        on_press=rgb_modes_cycle,
        on_release=handler_passthrough,
    )
