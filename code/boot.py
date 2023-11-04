import board

from kmk.bootcfg import bootcfg

# 目前 boot_device 似乎不正常工作
# 个人测试结果为只有关闭 nkro 并把 boot_device 设置为 0 才能操作 grub

bootcfg(
    # required:
    sense = board.GP27,
    # optional:
    source = board.GP15,
    boot_device = 0,
    cdc = False,
    midi = False,
    nkro = False,
    storage = False,
)
