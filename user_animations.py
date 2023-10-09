import supervisor

# old version, do not use
stream_priv = [0, 0, 0]
def old_stream(rgb):
    rgb.set_hsv(stream_priv[1], rgb.sat, rgb.val, stream_priv[0])
    stream_priv[0] += 1
    stream_priv[1] = (stream_priv[1] + rgb.hue_step) % 256

    if stream_priv[0] == rgb.num_pixels:
        rgb.show()
        stream_priv[0] = 0
        stream_priv[1] = (stream_priv[2] + 2) % 256
        stream_priv[2] = stream_priv[1]

stream_info = [0, 0] # first led color, led index
def stream(rgb):
    for i in range(20):
        led_color = (stream_info[0] + rgb.hue_step * stream_info[1]) % 256
        rgb.set_hsv(led_color, rgb.sat, rgb.val, stream_info[1])
        stream_info[1] = (stream_info[1] + 1) % rgb.num_pixels
        if stream_info[1] == 0:
            stream_info[0] = (stream_info[0] + 1) % 256
