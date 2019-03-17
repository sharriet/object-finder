from object_finder import *

# example 1: capture image from live video stream
# change src, T_bw and T_p to suit your setup
trigger_capture(src=1, T_bw=60, T_p=50)

# example 2: load image from url
#trigger_capture(url="img/test.png", T_bw=60, T_p=50)
