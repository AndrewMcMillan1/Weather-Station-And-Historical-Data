# !/usr/bin/env python

import math
import time
import grovepi
import json
from time import sleep
from grovepi import *
from math import isnan

# Temp/humidity sensor port
dht_sensor_port = 7
dht_sensor_type = 0

# List to hold tuples of sensor data
data = []

def readData():

    # insert reading into tuple
    [temp, humidity] = grovepi.dht(dht_sensor_port, dht_sensor_type)

    # make sure reading is a number
    if math.isnan(temp) == False and math.isnan(humidity) == False:
        # celsius to fahrenheit
        fahrenheit = ((temp * 9) / 5.0) + 32
        print("temp = %.02f F humidity =%.02f%%" % (fahrenheit, humidity))
        t = fahrenheit
        h = humidity

        # append tuple to list
        data.append([t, h])

    else:
        print("No data")


# main method
if __name__ == '__main__':

    while True:

        try:
            while curr_clock < '23:59:00':
                readData()
                sleep(4)
                curr_time = time.localtime()
                curr_clock = time.strftime("%H:%M:%S", curr_time)

            sleep(60)

        except IOError:
            print("Error")

        except KeyboardInterrupt as e:
            print(str(e))

            break




