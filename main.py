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

while True:

    try:

        [temp, humidity] = grovepi.dht(dht_sensor_port, dht_sensor_type)

        if math.isnan(temp) == False and math.isnan(humidity) == False:
            # celsius to fahrenheit
            fahrenheit = ((temp * 9) / 5.0) + 32
            print("temp = %.02f F humidity =%.02f%%" % (fahrenheit, humidity))
            t = fahrenheit
            h = humidity

            data.append([t, h])

        else:
            print("No data")

    except IOError:
        print("Error")

    except KeyboardInterrupt as e:
        print(str(e))

        break

    #  3 minutes between readings
    sleep(3)



