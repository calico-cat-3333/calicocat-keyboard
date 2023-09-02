import board

from kmk.bootcfg import bootcfg

bootcfg(
    # required:
    sense = board.GP27,
    # optional:
    source = board.GP15,
    boot_device = 1,
    cdc = False,
    midi = False,
    nkro = True,
    storage = False,
)
