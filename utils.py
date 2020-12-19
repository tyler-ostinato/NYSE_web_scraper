# File used to store functions for scraper.py
import datetime

# Use to convert epoch time to human readable string
def convert_epoch(time):
    time_string = datetime.datetime.fromtimestamp(time/1000).strftime('%c')
    return time_string