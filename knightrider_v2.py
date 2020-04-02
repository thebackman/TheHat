""" """


# -- setup


import time
from datetime import datetime
import unicornhat as unicorn

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(180)
unicorn.brightness(0.4)
WIDTH, HEIGHT = unicorn.get_shape()


# -- globals


# define a list of reds to use to light up the pixels
# this can be tinkered with to produce something that looks better
color_range = [(255,78,78),
               (255,39,39),
               (216,0,0),
               (118,0,0),
               (118,0,0),
               (216,0,0),
               (255,39,39),
               (255,78,78)]


# -- functions



def light_up_row(palette, start_value):
    """ lights up all the rows on the hat:
    
        loops over the columns on the hat, if this is in the
        allowed range (0 -> 7) light up those pixels using the palette
        provided.
        
        The inner loop just applies the coloring to all rows of the hat
    """
    # set starting position of the palette
    pal_pos = 0
    # loop from start value to end value (8 positions)
    for col in range(start_value, start_value + 8, 1):
        # if the value is not outside the hat range, light up this pixel
        if col >= 0 and col <= 7:
            print(f"lighting up column {col} with {palette[pal_pos]}")
            # color all pixels
            for row in range(2,6):
                unicorn.set_pixel(col, row, palette[pal_pos])
        # for each loop iteration, update display
        unicorn.show()
        pal_pos = pal_pos + 1
    time.sleep(0.03)
    unicorn.off()
    print("-----------------------------------------------")


def offset_looper():
    """ constructs ranges and feeds it to light_up_row """
    for i in range(-8, 8, 1):
        print("moving right -->")
        print(f"position is {i}")
        light_up_row(palette = color_range, start_value = i)
    print("---- changing direction ----")
    for p in range(8, -8, -1):
        print("moving left -->")
        print(f"position is {p}")
        light_up_row(palette = color_range, start_value = p)


def knight_rider(seconds):
    """ runs the entire process for xx seconds """
    t_end = time.time() + seconds
    while time.time() < t_end:
        offset_looper()
    unicorn.off()


# -- run


knight_rider(8)

