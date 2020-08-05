""" show me when I have to bring out the trash in the street """

### SETUP ######################################################################

# import ics
import os
from datetime import datetime # timedelta

PROJ_FOLDER = "/home/pi/Projects/Hattie"
CAL1 = os.path.join(PROJ_FOLDER, "calendar-Leichtverpackungen.ics")
CAL2 = os.path.join(PROJ_FOLDER, "calendar-Papier.ics")
TODAY = datetime.now().date()

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

def blue_day():
    pass

def yellow_day():
    pass

def blue_yellow_day():
    pass
        
### RUN ME #####################################################################

# -- read ICS file
 
# wanted to use the ICS parser from https://pypi.org/project/ics/
# but since the calendar files are malformed I will have to do it the
# dirty way

# events = ics.Calendar(CAL1)
plastic_days = parse_calendar(CAL1)
paper_days = parse_calendar(CAL2)

# -- check if today is in any of those lists

paper_today = TODAY in paper_days
plast_today = TODAY in plastic_days

# -- light it up

if paper_today == True and plast_today == True:
    print("today was a yellow and blue day")
    blue_yellow_day()
elif paper_today == True:
    print("today was a blue day")
    blue_day()
elif plast_today == True:
    print("today was a yellow day")
    yellow_day()
    


