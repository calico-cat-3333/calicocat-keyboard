# calicocat-keyboard
使用YD-RP2040（RPI pico兼容开发板）作为主控的键盘，带 RGB、旋钮和小屏幕，支持热插拔，使用kmk固件

code 文件夹中是键盘的固件代码，需要配合 [kmk](http://kmkfw.io/) 使用

键盘电路图及PCB开源在 [https://oshwhub.com/calico-cat-3333/calicocat-s-keyboard-v1](https://oshwhub.com/calico-cat-3333/calicocat-s-keyboard-v1) 

pcb 文件夹中也提供文件下载，需要使用嘉立创eda打开。

case 文件夹中是外壳的dxf文件。

keyboard-layout.json 是使用 [keyboard layout editor](http://www.keyboard-layout-editor.com) 设计的键位布局

警告：此版本的固件默认超频到 150MHz, 如果您不希望在超频的情况下使用此键盘，您应该注释 `mian.py` 的第 7 行。不过这会导致额外的输入延迟等。

我目前已经使用超频版本固件约半年，未发现严重问题。

## 已知问题

在使用此键盘时，会有偶发的键盘突然不停输入最后按下的按键的情况，似乎是按键松开事件没有正确传入电脑。由于此问题发生偶然性很大，我没有找到稳定的复现方法，故暂时无法定位修复。临时的解决方案是在出现此问题时将键盘拔下再重新插入即可。

![效果图](image.jpg)