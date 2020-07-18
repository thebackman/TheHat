""" show the temperature for the last 8 days """

# -- setup

# libs
import os
import sqlite3
from datetime import datetime, timedelta
import time
import unicornhat as unicorn

# led matrix
unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(180)
unicorn.brightness(0.4)
WIDTH, HEIGHT = unicorn.get_shape()

# paths
PROJ_FOLDER = "/home/pi/Projects/Hattie"
AIR_DB = os.path.join("/home/pi/Projects/GatherSensorData", "air.db")

# calculate dates
NOW = datetime.now().date()
YESTERDAY = NOW - timedelta(days = 1)
DAYS_AGO = NOW - timedelta(days = 8)

# color matrix, first entry warmest, last entry coldest
rocket = [(255, 50, 50),
          (255, 101, 50),
          (255, 178, 50),
          (229, 255, 50),
          (127, 255, 50),
          (50, 255, 132),
          (50, 129, 255),
          (50, 64, 255)]

# -- functions

def get_data():
    """ get the data from sqlite """
           
    # generate query - yes I know, SQL injection but its not exposed
    query = f"""
    with inbetween as (
        select date(time) as datecol, *
        from air_measures_10min
    	where datecol between '{DAYS_AGO}' and '{YESTERDAY}'),
    morebetween as (
    	select ntile(8) OVER(partition by datecol order by key) as the_holy_eight, *
    	from inbetween),
    lastbetween as (
    	select datecol, the_holy_eight, avg(temp) as mean_temp, min(time), max(time)
    	from morebetween
    	group by datecol, the_holy_eight)
    select * from lastbetween ;
    """
    
    # get the data
    conn = sqlite3.connect(AIR_DB)
    cur = conn.cursor()    
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows
    
def temp_to_rgb(tempval, colorscheme):
    """ input temperature, get back an rgb value """
    
    if tempval >= 0 and tempval <= 15:
        return colorscheme[7]
    elif tempval > 15 and tempval <= 18:
        return colorscheme[6]
    elif tempval > 18 and tempval <= 20:
        return colorscheme[5]
    elif tempval > 20 and tempval <= 22:
        return colorscheme[4]
    elif tempval > 22 and tempval <= 26:
        return colorscheme[3]
    elif tempval > 26 and tempval <= 30:
        return colorscheme[2]
    elif tempval > 30 and tempval <= 35:
        return colorscheme[1]
    elif tempval > 35:
        return colorscheme[0]
    else:
        return (0,0,0)
        
def show_color_scheme(colorscheme):
    """ shows the color scheme """
    
    for col in range(0, 8):
        for row in range(0, 8):
            unicorn.set_pixel(col, row, colorscheme[col])

def light_up_error():
    """ in case data is 'corrupt' just light it up to show that """
    
    for col in range(0, 8):
        for row in range(0, 8):
            unicorn.set_pixel(col, row, (125, 50, 255))
    
def turn_on_pixels(reslist):
    """ 
    show the data, the list that is returned from the query contains the data
    starting from the earliest date and the earlist time, so that means we must
    fill the unicorn from the last row, in column order """
    
    listlength = len(reslist)
    
    list_counter = 0
    for row in reversed(range(0, 8)):
        for col in range(0,8):
            print(f"row is: {row}, col is: {col}")
            # fill unicorn
            print(reslist[list_counter])
            pixel_temp = reslist[list_counter][2]
            print(pixel_temp)
            # light up the unicorn
            unicorn.set_pixel(col, row, temp_to_rgb(pixel_temp, rocket))
            # add to counter
            print(f"list counter is {list_counter}")
            list_counter = list_counter + 1
            # break out of loop once the list is full
            if list_counter == listlength:
                return

def activate_pixels(seconds):
    unicorn.show()
    time.sleep(seconds)
    unicorn.off()

# -- start execution

if __name__ == "__main__":
    results = get_data()
    show_color_scheme(rocket)
    activate_pixels(2)
    time.sleep(1)
    # right now, unless we have recordings that gives us eight slots per day,
    # do not show
    # TODO: rewrite query to generate results based on pre def time slots
    if len(results) != 60:
        print("data has not been properly recorded")
        light_up_error()
        activate_pixels(10)
    else:
        turn_on_pixels(results)
        activate_pixels(10)
    