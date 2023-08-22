from kmk.extensions.RGB import RGB as _RGB
from kmk.extensions.RGB import AnimationModes

import supervisor

class RGB(_RGB):
    flow_priv = [0, 0, 0]
    def user_animation_stream(self,sus):
        self.disable_auto_write = True
        #self.off()

        for i in range(3):
            self.set_hsv(self.flow_priv[1], self.sat, self.val, self.flow_priv[0])
            self.flow_priv[0] += 1
            self.flow_priv[1] = (self.flow_priv[1] + self.hue_step) % 256
            if self.flow_priv[0] == self.num_pixels:
                #self.disable_auto_write = False
                self.show()
                self.flow_priv[0] = 0
                self.flow_priv[1] = (self.flow_priv[2] + self.hue_step) % 256
                self.flow_priv[2] = self.flow_priv[1]
