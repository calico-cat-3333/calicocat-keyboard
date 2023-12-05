from kmk.keys import make_key
from kmk.extensions.RGB import AnimationModes
from kmk.handlers.stock import passthrough as handler_passthrough
from kmk.modules import Module

import supervisor

# 将电路上的rgb排列转换为更常见的排列
rgb_led_map = [
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
    for j in range(0,len(rgb_led_map)):
        for i in range(0, len(rgb_led_map[j])):
            rgb.set_hsv(
                rgb.hue + j * rgb.hue_step,
                rgb.sat,
                rgb.val,
                rgb_led_map[j][i]
            )
    rgb.increase_hue(rgb._step)

# 横向彩色流光灯效  horizontal stream animation
# 推荐 hue_step: 20  recommended hue_step: 20
def horizontal_stream(rgb):
    for j in range(0,len(rgb_led_map)):
        for i in range(0, len(rgb_led_map[j])):
            rgb.set_hsv(
                rgb.hue + i * rgb.hue_step,
                rgb.sat,
                rgb.val,
                rgb_led_map[j][i]
            )
    rgb.increase_hue(rgb._step)

# 当按下按键时改变rgb状态
# 这一部分是试验性的
value_map = None
# 当按下按键时点亮对应的led
def brightens_when_pressed(rgb):
    global value_map
    # module 会比 extension 更早加载，因此不能把 value_map 的初始化放在构造函数或 during_bootup 中
    # 因为在 rgb 模块中， num_pixels 在 during_bootup 之后才能确定
    if value_map == None:
        value_map = [0 for i in range(0,rgb.num_pixels)]
        # 附加一个虚拟灯，用于无灯的按键
        value_map.append(0)
    rgb.set_hsv_fill(rgb.hue, rgb.sat, 0)
    for i in range(0,rgb.num_pixels):
        if value_map[i] == -1:
            rgb.set_hsv(rgb.hue, rgb.sat, rgb.val, i)
        elif value_map[i] == -2:
            rgb.set_hsv(rgb.hue, rgb.sat, rgb.val, i)
            value_map[i] = rgb.val
        elif value_map[i] > 0:
            value_map[i] = value_map[i] - rgb._step
            rgb.set_hsv(rgb.hue, rgb.sat, value_map[i], i)

# 当按下按键时点亮对应的led，带有渐变色彩
def brightens_when_pressed_rainbow(rgb):
    global value_map
    # module 会比 extension 更早加载，因此不能把 value_map 的初始化放在构造函数或 during_bootup 中
    # 因为在 rgb 模块中， num_pixels 在 during_bootup 之后才能确定
    if value_map == None:
        value_map = [0 for i in range(0,rgb.num_pixels)]
        # 附加一个虚拟灯，用于无灯的按键
        value_map.append(0)
    rgb.set_hsv_fill(rgb.hue, rgb.sat, 0)
    for i in range(0,rgb.num_pixels):
        if value_map[i] == -1:
            rgb.set_hsv(rgb.hue, rgb.sat, rgb.val, i)
        elif value_map[i] == -2:
            rgb.set_hsv(rgb.hue, rgb.sat, rgb.val, i)
            value_map[i] = rgb.val
        elif value_map[i] > 0:
            value_map[i] = value_map[i] - rgb._step
            rgb.set_hsv(rgb.hue, rgb.sat, value_map[i], i)
    rgb.increase_hue(rgb._step)

# 当按下按键时熄灭对应的led
def dims_when_pressed(rgb):
    global value_map
    # module 会比 extension 更早加载，因此不能把 value_map 的初始化放在构造函数或 during_bootup 中
    # 因为在 rgb 模块中， num_pixels 在 during_bootup 之后才能确定
    if value_map == None:
        value_map = [rgb.val for i in range(0,rgb.num_pixels)]
        # 附加一个虚拟灯，用于无灯的按键
        value_map.append(0)
    rgb.set_hsv_fill(rgb.hue, rgb.sat, rgb.val)
    for i in range(0,rgb.num_pixels):
        if value_map[i] == -1:
            rgb.set_hsv(rgb.hue, rgb.sat, 0, i)
        elif value_map[i] == -2:
            rgb.set_hsv(rgb.hue, rgb.sat, 0, i)
            value_map[i] = 0
        elif value_map[i] < rgb.val:
            value_map[i] = value_map[i] + rgb._step
            rgb.set_hsv(rgb.hue, rgb.sat, value_map[i], i)

# 当按下按键时熄灭对应的led，带有渐变色彩
def dims_when_pressed_rainbow(rgb):
    global value_map
    # module 会比 extension 更早加载，因此不能把 value_map 的初始化放在构造函数或 during_bootup 中
    # 因为在 rgb 模块中， num_pixels 在 during_bootup 之后才能确定
    if value_map == None:
        value_map = [rgb.val for i in range(0,rgb.num_pixels)]
        # 附加一个虚拟灯，用于无灯的按键
        value_map.append(0)
    rgb.set_hsv_fill(rgb.hue, rgb.sat, rgb.val)
    for i in range(0,rgb.num_pixels):
        if value_map[i] == -1:
            rgb.set_hsv(rgb.hue, rgb.sat, 0, i)
        elif value_map[i] == -2:
            rgb.set_hsv(rgb.hue, rgb.sat, 0, i)
            value_map[i] = 0
        elif value_map[i] < rgb.val:
            value_map[i] = value_map[i] + rgb._step
            rgb.set_hsv(rgb.hue, rgb.sat, value_map[i], i)
    rgb.increase_hue(rgb._step)

# 上述四个RGB灯效需要的辅助模块，负责读取按下的按键
class RGBwithKeyProcerss(Module):
    def __init__(self, rgb):
        # 将rgb编号对应到按键
        self._rgb_led_map = [
            15,14,13,12,11,10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0,
            16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,
            45,44,43,42,41,40,39,38,37,36,35,34,33,32,31,
            46,47,48,49,50,51,52,53,54,55,56,57,58,59,
            73,72,71,70,69,68,67,66,65,64,63,62,61,60,
            74,75,76,77,78,79,80,81,82,83,84,85,
            86,86,86 # 这三个是虚拟灯
        ]
        self.rgb = rgb

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if not self.rgb.enable:
            return key
        if not self.rgb.animation_mode == AnimationModes.USER:
            return key
        if self.rgb.user_animation in [
            brightens_when_pressed,
            brightens_when_pressed_rainbow,
            dims_when_pressed,
            dims_when_pressed_rainbow
        ]:
            self.dims_brightens_pk(keyboard, is_pressed, int_coord)
        return key

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def deinit(self, keyboard):
        pass

    def dims_brightens_pk(self, keyboard, is_pressed, int_coord):
        global value_map
        if is_pressed:
            value_map[self._rgb_led_map[keyboard.coord_mapping.index(int_coord)]] = -1
        else:
            value_map[self._rgb_led_map[keyboard.coord_mapping.index(int_coord)]] = -2
# 试验性部分到这里


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
    user_animations_list = [
        stream,
        vertical_stream,
        horizontal_stream,
        brightens_when_pressed,
        brightens_when_pressed_rainbow,
        dims_when_pressed,
        dims_when_pressed_rainbow
    ]
    if not user_animations_list == []:
        rgb_modes_list.append(AnimationModes.USER)
        if rgb.user_animation == None:
            rgb.user_animation = user_animations_list[0]
    rgb_modes_num = len(rgb_modes_list)
    user_animations_num = len(user_animations_list)

    def rgb_modes_cycle(*args, **kwargs):
        rgb.effect_init = True
        current_rgb_mode = 0
        if rgb.animation_mode == AnimationModes.STATIC_STANDBY:
            current_rgb_mode = rgb_modes_list.index(AnimationModes.STATIC)
        else:
            current_rgb_mode = rgb_modes_list.index(rgb.animation_mode)

        if rgb.animation_mode == AnimationModes.USER:
            current_user_animation = (user_animations_list.index(rgb.user_animation) + 1) % user_animations_num
            rgb.user_animation = user_animations_list[current_user_animation]
            if not current_user_animation == 0:
                current_rgb_mode = current_rgb_mode - 1

        current_rgb_mode = (current_rgb_mode + 1) % rgb_modes_num
        rgb.animation_mode = rgb_modes_list[current_rgb_mode]

    make_key(
        names=('RGB_MODES_CYCLE', 'RGB_CYC'),
        on_press=rgb_modes_cycle,
        on_release=handler_passthrough,
    )
