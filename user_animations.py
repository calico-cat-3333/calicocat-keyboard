import supervisor

stream_priv = [0, 0, 0]
def stream(rgb):
    rgb.disable_auto_write = True

    rgb.set_hsv(stream_priv[1], rgb.sat, rgb.val, stream_priv[0])
    stream_priv[0] += 1
    stream_priv[1] = (stream_priv[1] + rgb.hue_step) % 256

    if stream_priv[0] == rgb.num_pixels:
        rgb.show()
        stream_priv[0] = 0
        stream_priv[1] = (stream_priv[2] + rgb.hue_step) % 256
        stream_priv[2] = stream_priv[1]
