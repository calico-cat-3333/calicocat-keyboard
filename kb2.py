import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.scanners.encoder import RotaryioEncoder
from kmk.scanners.digitalio import MatrixScanner


class KMKKeyboard(_KMKKeyboard):
    extensions = []

    row_pins = [board.GP27, board.GP26, board.GP22, board.GP21, board.GP20, board.GP19, board.GP18, board.GP17, board.GP16]
    col_pins = [board.GP15, board.GP14, board.GP13, board.GP12, board.GP11, board.GP10, board.GP9, board.GP8, board.GP7, board.GP6]
    diode_orientation = DiodeOrientation.ROW2COL

    coord_mapping = [
         0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 60, 61, 62, 63, 64, 65,
        10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 66, 67, 68, 69, 79,
        20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 70, 71, 72, 73, 74,
        30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 75, 76, 77, 78,
        40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 80, 81, 82, 83,
        50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 84, 85,
        86, 90, 91  # this three key for rotaryioencoder
        ]

    def __init__(self):
        self.matrix = [
            MatrixScanner(
                cols=self.col_pins,
                rows=self.row_pins,
                diode_orientation=self.diode_orientation,
                ),
            RotaryioEncoder(
                pin_a=board.GP1,
                pin_b=board.GP0
                ),
            ]
