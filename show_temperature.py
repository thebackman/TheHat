""" show the temperature for the last 8 days """

# CRON

# 1 22 * * * python3 /home/pi/Projects/Hattie/show_temperature.py

# -- setup

# libs
import os
import sqlite3
from datetime import datetime, timedelta
import time
import unicornhat as unicorn
import pandas as pd

# led matrix
unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(180)
unicorn.brightness(0.4)
WIDTH, HEIGHT = unicorn.get_shape()

# paths
PROJ_FOLDER = "/home/pi/Projects/Hattie"
AIR_DB = os.path.join("/home/pi/Projects/GatherSensorData", "air.db")

# -- prepare dates

TODAY = datetime.now().date()
YESTERDAY = TODAY - timedelta(days = 1)
DAYS_AGO = TODAY - timedelta(days = 8)

# -- colors

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

def prepare_full_data():
    """ construct a 'full' data set so that we can identify missing data """
    
    # create a data frame with all days between yesterday and 8 days back
    start = DAYS_AGO
    step = timedelta(days=1)
    daylist = []
    while start <= YESTERDAY:
        daylist.append(start)
        start += step
    df_days = pd.DataFrame({"datecol": daylist})
    df_days["key"] = 1
    df_days["datecol"] = df_days["datecol"].astype(str)
    
    # create a data frame with all the avaliable time slots
    slots = []
    for slot in range(0, 24, 3):
        slots.append(f"slot{slot}_{slot + 3}")
    df_slots = pd.DataFrame({"timeslot":slots})
    df_slots["key"] = 1
    
    # combine this data set to construct a df with 64 rows for all combinations    
    df_all_combos = df_days.merge(df_slots, how = "outer")
    df_all_combos.drop(columns = "key", inplace = True)
    
    return df_all_combos
    

def get_data():
    """ get the data from sqlite """
           
    # generate query - yes I know, SQL injection but its not exposed
    query = f"""
    with prepared as (
    	select
    		date(time) as datecol,
    		time(time) as timecol,
    		*
        from air_measures_10min
        where datecol between '{DAYS_AGO}' and '{YESTERDAY}'),
    	slotted as (
        select
        case
        	when timecol between '00:00:00' and '03:00:00' then 'slot0_3'
            when timecol between '03:00:00' and '06:00:00' then 'slot3_6'
            when timecol between '06:00:00' and '09:00:00' then 'slot6_9'
            when timecol between '09:00:00' and '12:00:00' then 'slot9_12'
            when timecol between '12:00:00' and '15:00:00' then 'slot12_15'
            when timecol between '15:00:00' and '18:00:00' then 'slot15_18'
            when timecol between '18:00:00' and '21:00:00' then 'slot18_21'
            when timecol between '21:00:00' and '24:00:00' then 'slot21_24'
        end as timeslot,
        *
        from prepared)
    select
        datecol,
        timeslot,
        count(*) as n_obs,
    	avg(temp) as mean_temp,
    	min(time) as min_time,
    	max(time) as max_time
    from slotted
    group by datecol, timeslot
    order by datecol, min_time ;
    """
    
    # get the data
    conn = sqlite3.connect(AIR_DB)
    
    # get the data 
    rows = pd.read_sql_query(query, con = conn)
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
    elif tempval > 20 and tempval <= 23:
        return colorscheme[4]
    elif tempval > 23 and tempval <= 26:
        return colorscheme[3]
    elif tempval > 26 and tempval <= 30:
        return colorscheme[2]
    elif tempval > 30 and tempval <= 35:
        return colorscheme[1]
    elif tempval > 35 and tempval <= 55:
        return colorscheme[0]
    else:
        return (0,0,0)
        
def show_color_scheme(colorscheme):
    """ shows the color scheme """
    
    for col in range(0, 8):
        for row in range(0, 8):
            unicorn.set_pixel(col, row, colorscheme[col])

def turn_on_pixels(seconds):
    """ show the data """
    
    counter = 0
    # loop from the bottom rows of the hat and go columnswise ---> ^ ---> etc
    for row in reversed(range(0, 8)):
        for col in range(0,8):
            print(f"row is: {row}, col is: {col}")
            # extract temperature and convert to float
            tempus = df_show.loc[counter, "mean_temp"]
            tempus = float(tempus)
            print(f"temperature is {tempus}")
            # get the color value that should be displayed
            color = temp_to_rgb(tempus, rocket)
            print(f"color is {color}")
            # turn on pixels
            unicorn.set_pixel(col, row, color)
            time.sleep(0.05)
            unicorn.show()
            # add to counter
            print(f"counter is {counter}")
            counter = counter + 1
    # let it shine
    time.sleep(seconds)
    unicorn.off()
           
# -- start execution

# get the data from sqlite as pandas df
df_data = get_data()

# get the full data
df_all = prepare_full_data()

# merge actual data with full data to get a df that has explicit missings
df_show = pd.merge(df_all,
                   df_data,
                   left_on = ['datecol','timeslot'],
                   right_on = ['datecol', 'timeslot'],
                   how = "outer",
                   indicator = True)

# replace all missing values with something unresonable
df_show = df_show.fillna(value = {"n_obs": 0, "mean_temp": 99999})

# activate the pixels
turn_on_pixels(20)
