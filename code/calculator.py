import board
import terminalio
import displayio
import supervisor
from math import *
# bitmap_label 不工作，因为这将导致 pystack exhausted 堆栈溢出。
# from adafruit_display_text import bitmap_label as label
from adafruit_display_text import label

from kmk.modules import Module

from gettime import get_time

_char_map = [r"abcdefghijklmnopqrstuvwxyz1234567890 -=[]\;'`,./",
             r'ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*() _+{}|:"~<>?']

class LCDCalculator(Module):
    def __init__(self, lcd, history_length = 8, cursor_style = '|', decimal_places = 5):
        self.lcd = lcd
        self.font = terminalio.FONT
        self.color = 0xffffff
        self.expr = ''
        self.expr_history = ['']
        self.expr_history_length = history_length + 1 # 0 被用于缓存查看历史时的当前输入
        self.expr_history_showing = 0
        self.ans = ''
        self.decimal_places = decimal_places # 最大保留小数位数，使用 round 函数处理，circuitpython 的小数精度十分有限
        self.cursor_pos = 0
        self.cursor_style = cursor_style
        self.unreleased_keys = set() # 退出时未松开的按键
        self.unreleased_modkeys = set() # 退出时未松开的修饰键
        self.update_display_list = [True, True] # expr, ans
        self.shift_pressed = False # 是否按下 shift

    def during_bootup(self, keyboard):
        self.group = self.lcd.add_group()
        self.expr_label = label.Label(self.font, text=' '*20, color=self.color, scale=2, x=0, y=10, anchor_point=(0.0, 0.0))
        self.ans_label = label.Label(self.font, text=' '*40, color=self.color, scale=2, x=0, y=40, anchor_point=(0.0, 0.0))
        self.hint_label = label.Label(self.font, text='Experimental\nSimple Calculator', color=self.color, x=5, y=100, anchor_point=(0.0, 0.0))
        self.expr_label.text = '|'
        self.group.append(self.expr_label)
        self.group.append(self.ans_label)
        self.group.append(self.hint_label)
        return

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    #@get_time
    def process_key(self, keyboard, key, is_pressed, int_coord):
        #print('------------->key event:',key,is_pressed,int_coord)
        if not self.lcd.group_on_showing(self.group):
            # 如果退出时没有松开某个按键，那么当发生按键释放事件时仍然拦截一次
            if hasattr(key, 'FAKE_CODE'):
                # 是修饰键
                #print('is mod key')
                if len(self.unreleased_modkeys) != 0 and is_pressed == False and key.code in self.unreleased_modkeys:
                    self.modkey_release(key.code)
                    self.unreleased_modkeys.discard(key.code)
                    #print('in unreleased_modkeys,',key.code)
                    return
                #print('send key event')
                return key

            # 是常规按键
            #print('is input key')
            if len(self.unreleased_keys) != 0 and is_pressed == False and key.code in self.unreleased_keys:
                self.unreleased_keys.discard(key.code)
                #print('in unreleased_keys,',key.code)
                return
            #print('send key event')
            return key

        if hasattr(key, 'FAKE_CODE'):
            # 是修饰键
            #print('is mod key')
            if is_pressed:
                #print('mod key pressed:',key.code)
                self.modkey_press(key.code)
                self.unreleased_modkeys.add(key.code)
                # 修饰键按下是不需要刷新显示的
                #print('out')
                return
            # 防止进入该功能时有按键未松开
            if key.code in self.unreleased_modkeys:
                self.modkey_release(key.code)
                self.unreleased_modkeys.discard(key.code)
                #print('mod key in unreleased_modkeys release')
                return
            #print('mod key released:',key.code)
            return key

        # 是常规按键
        if not (key.code >= 4 and key.code <= 82):
            # 排除非有效按键
            #print('not input key')
            return key
        if is_pressed:
            #print('key pressed:',key.code)
            self.key_operate(key.code)
            self.update_display()
            self.unreleased_keys.add(key.code)
            #print('out')
            return
        if key.code in self.unreleased_keys:
            self.unreleased_keys.discard(key.code)
            #print('key in unreleased_keys released:',key.code)
            return
        #print('key released:',key.code)
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

    def key_operate(self, keycode):
        #print('key operate:',keycode)
        if (keycode >=4 and keycode <= 39):
            self.char_insert_key(keycode - 4)
        elif keycode >= 44 and keycode <= 49:
            self.char_insert_key(keycode - 8) # keycode - 44 + 36
        elif keycode >= 51 and keycode <= 56:
            self.char_insert_key(keycode - 9) # keycode - 51 + 42
        elif keycode == 42: # Backspace
            self.check_clear_display()
            if self.cursor_pos > 0:
                self.expr = self.expr[:self.cursor_pos - 1] + self.expr[self.cursor_pos:]
                self.cursor_pos = self.cursor_pos - 1
                self.update_display_list[0] = True
        elif keycode == 76: # Delet
            self.check_clear_display()
            if self.cursor_pos < len(self.expr):
                self.expr = self.expr[:self.cursor_pos] + self.expr[self.cursor_pos + 1:]
                self.update_display_list[0] = True
        elif keycode == 40: # Enter
            self.do_calc()
        elif keycode == 80: # Left
            if self.cursor_pos > 0:
                self.cursor_pos = self.cursor_pos - 1
                self.update_display_list[0] = True
        elif keycode == 79: # Right
            if self.cursor_pos < len(self.expr):
                self.cursor_pos = self.cursor_pos + 1
                self.update_display_list[0] = True
        elif keycode == 74: # Home
            self.cursor_pos = 0
            self.update_display_list[0] = True
        elif keycode == 77: # End
            self.cursor_pos = len(self.expr)
            self.update_display_list[0] = True
        elif keycode == 82: # Up
            if self.expr_history_showing < len(self.expr_history) - 1:
                if self.expr_history_showing == 0:
                    self.expr_history[0] = self.expr
                self.expr_history_showing = self.expr_history_showing + 1
                self.expr = self.expr_history[self.expr_history_showing]
                self.cursor_pos = len(self.expr)
                self.ans = ''
                self.update_display_list = [True, True]
        elif keycode == 81: # Down
            if self.expr_history_showing > 0:
                self.expr_history_showing = self.expr_history_showing - 1
                self.expr = self.expr_history[self.expr_history_showing]
                self.cursor_pos = len(self.expr)
                if self.expr_history_showing == 0:
                    self.expr_history[0] = ''
                self.ans = ''
                self.update_display_list = [True, True]
        #print('key operate end:',keycode)

    def char_insert_key(self, char):
        #print('start char insert:',char)
        self.check_clear_display()
        self.expr = self.expr[:self.cursor_pos] + _char_map[self.shift_pressed][char] + self.expr[self.cursor_pos:]
        self.cursor_pos = self.cursor_pos + 1
        self.update_display_list[0] = True
        #print('char insert end')

    def modkey_press(self, modcode):
        #print('modkey start',modcode)
        if modcode == 0x02 or modcode == 0x20:
            self.shift_pressed = True
        #print('modkey end')

    def modkey_release(self, modcode):
        #print('modkey release start',modcode)
        if modcode == 0x02 and (not 0x20 in self.unreleased_modkeys):
            self.shift_pressed = False
        elif modcode == 0x20 and (not 0x02 in self.unreleased_modkeys):
            self.shift_pressed = False
        #print('modkey release end')

    def check_clear_display(self):
        if len(self.ans) != 0:
            # clear
            if self.ans == 'Error':
                self.ans = ''
                self.expr_history_showing = 0
                self.update_display_list[1] = True
            else:
                self.clear_dispaly()

    def clear_dispaly(self):
        self.ans = ''
        self.expr = ''
        self.cursor_pos = 0
        self.update_display_list = [True, True]
        self.expr_history_showing = 0

    def update_display(self):
        #print('update_display start')
        #print(self.ans)
        # 更新算式显示
        disp_expr = ''
        expr_len = len(self.expr)
        ans_len = len(self.ans)
        if self.update_display_list[0]:
            self.update_display_list[0] = False
            if self.cursor_pos <= 10:
                # 光标在前10位时
                disp_expr = self.expr[:self.cursor_pos] + self.cursor_style
                if expr_len <= 19:
                    disp_expr = disp_expr + self.expr[self.cursor_pos:]
                else:
                    disp_expr = disp_expr + self.expr[self.cursor_pos:17] + '..'
            elif expr_len - self.cursor_pos <= 9:
                # 光标在后9位时
                disp_expr = self.cursor_style + self.expr[self.cursor_pos:]
                if expr_len <= 19:
                    disp_expr = self.expr[:self.cursor_pos] + disp_expr
                else:
                    disp_expr = '..' + self.expr[expr_len - 17:self.cursor_pos] + disp_expr
            else:
                # 光标在中间时
                disp_expr = '..' + self.expr[self.cursor_pos - 8:self.cursor_pos] + self.cursor_style + self.expr[self.cursor_pos:self.cursor_pos + 7] + '..'
            self.expr_label.text = disp_expr

        if self.update_display_list[1]:
            self.update_display_list[1] = False
            if ans_len > 20:
                self.ans_label.scale = 1
            else:
                self.ans_label.scale = 2
            self.ans_label.text = self.ans
        #print('update_display end')

    def do_calc(self):
        #print('do calc start')
        #print(self.expr)
        try:
            ans = eval(self.expr)
            if type(ans) == int or type(ans) == bool:
                self.ans = str(ans)
            elif type(ans) == float:
                self.ans = str(round(ans, self.decimal_places))
            else:
                self.ans = 'Error'
            if len(self.ans) > 38:
                self.ans = 'Output Limit Exceed'
        except Exception as e:
            self.ans = 'Error'
        #print(self.ans)
        self.update_display_list[1] = True
        self.expr_history.insert(1, self.expr)
        self.expr_history_showing = 1
        self.expr_history[0] = ''
        if len(self.expr_history) > self.expr_history_length:
            self.expr_history.pop()
        #print('do calc end')
