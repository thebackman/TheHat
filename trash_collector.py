""" show me when I have to bring out the trash in the street """

### SETUP ######################################################################

# import ics
import os
from datetime import datetime, timedelta
import unicornhat as unicorn
import time

# folders
PROJ_FOLDER = "/home/pi/Projects/Hattie"
CAL1 = os.path.join(PROJ_FOLDER, "calendar-Leichtverpackungen.ics")
CAL2 = os.path.join(PROJ_FOLDER, "calendar-Papier.ics")

# dates
TODAY = datetime.now().date()
TOMORROW = TODAY + timedelta(days = 1)
RUN_TIME_SECS = 1800

# led matrix
unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(180)
unicorn.brightness(0.4)

# colors
blues = [[0,0,255], [0,191,255]]
yellows = [[255,255,0], [255, 215,0]]
blue_yellow = [blues[0], yellows[0]]

### FUNCTIONS ##################################################################

def parse_calendar(path):
    """ returns the start date for each event """
        
    # read each calendar line
    with open(path) as file:
        lines = file.readlines()
        
    # strip lines endings
    lines = [x.strip() for x in lines] 
    
    # extract the dates for each event
    dates = []
    for item in lines:
        # print(item)
        # extract the date from this string, it always has the same structure
        # so we dont need something fancy to do this
        if item[0:7] == "DTSTART":
            datestring = item[27:35]
            # print(datestring)
            dates.append(datetime.strptime(datestring, "%Y%m%d").date())
            
    return(dates)

def show_colors(color_scheme, seconds):
    """ show a chess board consisting of two colors """
    
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
                    unicorn.set_pixel(row, col, tuple(color_scheme[0]))
                else:
                    unicorn.set_pixel(row, col, tuple(color_scheme[1]))
            # if we have uneven rows, apply color1 on entry 1,3,5,7
            if mod_row == 1:
                if mod_col == 1:
                    unicorn.set_pixel(row, col, tuple(color_scheme[0]))
                else:
                    unicorn.set_pixel(row, col, tuple(color_scheme[1]))
    
    unicorn.show()
    time.sleep(seconds)
    unicorn.off()
        
### RUN ########################################################################

# -- read ICS file
 
# wanted to use the ICS parser from https://pypi.org/project/ics/
# but since the calendar files are malformed I will have to do it the
# dirty way

# events = ics.Calendar(CAL1)
plastic_days = parse_calendar(CAL1)
paper_days = parse_calendar(CAL2)

# -- check if tomorrow is in any of those lists

paper_tom = TOMORROW in paper_days
plast_tom = TOMORROW in plastic_days

# -- light it up

# show me that you are thinking of us
show_colors(blue_yellow, 1)
time.sleep(0.5)
show_colors(blues, 1)
time.sleep(0.5)
show_colors(yellows, 1)
time.sleep(1)

if paper_tom == True and plast_tom == True:
    print("today was a yellow and blue day")
    show_colors(blue_yellow, RUN_TIME_SECS)
elif paper_tom == True:
    print("today was a blue day")
    show_colors(blues, RUN_TIME_SECS)
elif plast_tom == True:
    print("today was a yellow day")
    show_colors(yellows, RUN_TIME_SECS)
    


