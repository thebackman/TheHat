""" some intro code for the hat 

    # x-coord, y-coord, r,g,b value

"""


# -- libs


import time
from datetime import datetime
import unicornhat as unicorn


# -- Set layout and some GLOBALS


unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(180)
unicorn.brightness(0.4)
WIDTH, HEIGHT = unicorn.get_shape()
print(f"WIDTH is {WIDTH}")
print(f"HEIGHT is {HEIGHT}")


# -- color tuple
    
col_tuple = (139,0,0)


# -- functions

def go_right(wait_in_seconds):
    for col in range(0, WIDTH):
        for row in range(0, HEIGHT):
            # get a feeling for how long one iteration takes
            # about 1 milliseconds, or not even that
            # now = datetime.now()
            # print(now)
            # light up the entire column
            unicorn.set_pixel(col, row, col_tuple)
        unicorn.show()
        # wait 0.1 second
        time.sleep(wait_in_seconds)
        # turn off the pixels
        unicorn.off()
    #time.sleep(wait_in_seconds)
    #unicorn.off()

def go_left(wait_in_seconds):
    for col in range(WIDTH -1, -1, -1):
        for row in range(0, HEIGHT):
            # light up the entire column
            unicorn.set_pixel(col, row, col_tuple)
        unicorn.show()
        # wait 0.1 second
        time.sleep(wait_in_seconds)
        # turn off the pixels
        unicorn.off()
    #time.sleep(wait_in_seconds)
    #unicorn.off()

def knight_rider(seconds):
    # Run for xx seconds
    t_end = time.time() + seconds
    while time.time() < t_end:
        go_right(0.08)
        go_left(0.08)    
    # kill all pixels
    unicorn.off()


# -- run

knight_rider(10)

    


