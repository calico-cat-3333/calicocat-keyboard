import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.scanners.encoder import RotaryioEncoder
from kmk.scanners.keypad import MatrixScanner


class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        super().__init__()

        self.col_pins = [board.GP27, board.GP26, board.GP22, board.GP21, board.GP20, board.GP19, board.GP18, board.GP17, board.GP16]
        self.row_pins = [board.GP15, board.GP14, board.GP13, board.GP12, board.GP11, board.GP10, board.GP9, board.GP8, board.GP7, board.GP6]
        self.diode_orientation = DiodeOrientation.COL2ROW

        self.coord_mapping = [
            0,  9, 18, 27, 36, 45, 54, 63, 72, 81,  6, 15, 24, 33, 42, 51,
            1, 10, 19, 28, 37, 46, 55, 64, 73, 82, 60, 69, 78, 87, 88,
            2, 11, 20, 29, 38, 47, 56, 65, 74, 83,  7, 16, 25, 34, 43,
            3, 12, 21, 30, 39, 48, 57, 66, 75, 84, 52, 61, 70, 79,
            4, 13, 22, 31, 40, 49, 58, 67, 76, 85,  8, 17, 26, 35,
            5, 14, 23, 32, 41, 50, 59, 68, 77, 86, 44, 53,
            62, 90, 91  # this three key for rotaryioencoder
            ]

        self.matrix = [
             MatrixScanner(
                column_pins=self.col_pins,
                row_pins=self.row_pins,
                columns_to_anodes=self.diode_orientation
                ),
            RotaryioEncoder(
                pin_a=board.GP1,
                pin_b=board.GP0
                ),
            ]
