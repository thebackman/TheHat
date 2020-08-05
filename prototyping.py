""" be able to prototype the unicorn hat on my laptop

Using some numpy arrays and plots to mimic the LED matrix
    
"""

### EXAMPLE ###################################################################

import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import time

# -- define color ranges

# darkblue, lightblue
blues = [[0,0,255], [0,191,255]]
yellow = [[255,255,0], [255, 215,0]]
blue_yellow = [blues[0], yellow[0]]

# initiate empty numpy array to hold results
# 8 rows, 8 columns, 3 layers for RGB values
holder = np.zeros((8, 8, 3))

# iterate over the rows of the matrix
for row in range(0, 8):
    for col in range (0,8):
        print(f"--- row is {row} and col is {col} -- ")
        # check if we have even | uneven rows cols
        mod_row = row % 2
        mod_col = col % 2
        print(mod_row)
        print(mod_col)
        # if we have even rows apply color1 on entry 0, 2, 4, 6
        if mod_row == 0:
            if mod_col == 0:
                holder[row, col, 0:3] = blue_yellow[0]
                # unicorn.set_pixel(row, col, tuple(blue_yellow[0]))
            else:
                holder[row, col, 0:3] = blue_yellow[1]
        # if we have uneven rows, apply color1 on entry 1,3,5,7
        if mod_row == 1:
            if mod_col == 1:
                holder[row, col, 0:3] = blue_yellow[0]
            else:
                holder[row, col, 0:3] = blue_yellow[1]

# plot the colors of the array
io.imshow(holder)
# unicorn.show()

### FUNCTIONS #################################################################

def set_point(row, col, rgb_list, dev):
    """ turn on the unicorn or put the entry into a numpy array """
    
    # create a black matrix
    holder = np.zeros((8, 8, 3))
    
    # decide if we light up unicorn or fill the matrix
    if dev == "uni":
        unicorn.set_pixel(row, col, tuple(rgb_list))
    if dev == "screen":
        holder[row, col, 0:3] = rgb_list
        return holder

def activate_points(dev):
    if dev == "uni":
        unicorn.show()
        time.sleep(10)
        unicorn.off()
    if dev == "screen":
        io.imshow(holder)
    

        

