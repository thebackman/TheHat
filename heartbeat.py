""" show a beating heart """

# -- setup

import time
import unicornhat as unicorn
import numpy as np
import sys

STANDARD_BRIGHTNESS = 0.5

# generate brightness values
vals_raw = np.arange(0.4, 1, 0.01)
vals = vals_raw.tolist()
vals_rev = np.flip(vals_raw).tolist()

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(180)
unicorn.brightness(STANDARD_BRIGHTNESS)
WIDTH, HEIGHT = unicorn.get_shape()

# get the number of beats
beats = int(sys.argv[1]) + 1
# get the palette to use
palette = sys.argv[2]

# -- functions

def heart():
    """ draw a heart """ 

    if palette == "reds":
        color1 = (190,0,0)
        color2 = (255,0,0)
    if palette == "greens":
        color1 = (45,175,20)
        color2 = (42, 255, 0)

    # define the positions for the heart
    pos = [
        [1,2,5,6],
        [0,1,2,3,4,5,6,7],
        [0,1,2,3,4,5,6,7],
        [0,1,2,3,4,5,6,7],
        [1,2,3,4,5,6],
        [2,3,4,5],
        [3,4]
        ]
    
    row = 0
    # loop over each row in the heart
    for r in pos:
        # light up each of the columns
        for c in r:
            if (row in [1,2]) and (c in [2,3]):
                unicorn.set_pixel(c, row, color2)
            else:
                unicorn.set_pixel(c, row, color1)
        row = row + 1

def fade(pausetime, direction):
    """ loop over the values and increase brightness """
    if direction == "in":
        v = vals
    elif direction == "out":
        v = vals_rev
    for val in v:
        unicorn.brightness(val)
        heart()
        unicorn.show()
        time.sleep(pausetime)
    unicorn.off()

# -- light it up

for i in range(1, beats):
    fade(0.005, "in")
    fade(0.001, "out")
    time.sleep(0.6)






