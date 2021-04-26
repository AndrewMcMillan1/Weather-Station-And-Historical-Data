# !/usr/bin/env python

import math
import time
import datetime
import grovepi
import json
from time import sleep
from grovepi import *
import sqlite3 as sql
from math import isnan

# Temp/humidity sensor port
sensor_port = 7
sensor_type = 0

# List to hold tuples of sensor data
sensorData = []

def readData():
    # insert reading as tuple in list
    [temp, humidity] = grovepi.dht(sensor_port, sensor_type)

    # ensure that reading is a number
    if not math.isnan(temp) and not math.isnan(humidity):

        # celsius to fahrenheit
        fahrenheit = ((temp * 9) / 5.0) + 32
        print("temp = %.02f F humidity =%.02f%%" % (fahrenheit, humidity))
        t = fahrenheit
        h = humidity

        sensorData.append([t, h])

# node data
class reading:
    temp = 0
    hum = 0

    # parameterized constructor
    def __init__(self, t, h):
        self.temp = t
        self.hum = h


# node struct
class newNode:

    # Node constructor
    def __init__(self, key, reading):

        self.data = reading
        self.key = key
        self.count = 1
        self.left = None
        self.right = None
        self.height = 1


# The function finds keys in range [low, high)
def range(root, low, high, range_list):
    # Base Case
    if root is None:
        return

    # move toward low end of range
    if low < root.key:
        range(root.left, low, high, range_list)

    # If data is in range
    if low <= root.key and high > root.key:

        # add in-range data to list
        range_list.append([root.data.temp, root.data.hum])

    # move toward high end of range
    if high > root.key:
        range(root.right, low, high, range_list)

    return range_list

# inorder traversal function
def inorder(root, order_list):

    if root is not None:

        # move to left subtree
        inorder(root.left, order_list)

        # add data to list
        order_list.append([root.data.temp, root.data.hum])

        # move to right subtree
        inorder(root.right, order_list)

    return order_list


# Insert a node function
def insert(root, key, bid):
    # If tree is empty, create new node
    if root is None:
        k = newNode(key, bid)
        return k

    # recursive function moves down the tree
    if key < root.key:
        root.left = insert(root.left, key, bid)
    else:
        root.right = insert(root.right, key, bid)

    # calculate height
    root.height = 1 + max(getHeight(root.left),
                          getHeight(root.right))

    # get balance
    bal = getBalance(root)

    # If the node is unbalanced, re-balance
    #  case 1
    if bal > 1 and key < root.left.key:
        return rotateRight(root)

    #  case 2
    if bal < -1 and key > root.right.key:
        return rotateLeft(root)

    #  case 3
    if bal > 1 and key > root.left.key:
        root.left = rotateLeft(root.left)
        return rotateRight(root)

    #  case 4
    if bal < -1 and key < root.right.key:
        root.right = rotateRight(root.right)
        return rotateLeft(root)

    return root

# left rotation
def rotateLeft(z):

    y = z.right
    tree2 = y.left

    # rotate
    y.left = z
    z.right = tree2

    # Update height
    z.height = 1 + max(getHeight(z.left),
                           getHeight(z.right))
    y.height = 1 + max(getHeight(y.left),
                           getHeight(y.right))

    # Return the new root
    return y

# right rotation
def rotateRight(z):

    y = z.left
    tree3 = y.right

    # rotate
    y.right = z
    z.left = tree3

    # update height
    z.height = 1 + max(getHeight(z.left),
                        getHeight(z.right))
    y.height = 1 + max(getHeight(y.left),
                        getHeight(y.right))

    # Return the new root
    return y


# calc height
def getHeight(root):

    if not root:
        return 0

    return root.height


# calc balance
def getBalance(root):

    if not root:
        return 0

    return getHeight(root.left) - getHeight(root.right)


# delete entire tree function
def deleteTree(node):
    if node:

        # recursively visit all nodes
        deleteTree(node.left)
        deleteTree(node.right)

        # delete pointers
        node.left = None
        node.right = None


# find minimum key value
def minNode(node, min_data):
    current = node

    # move only left
    while current.left is not None:
        current = current.left

    # add min temp node to list
    min_data.append([current.data.temp, current.data.hum])
    return min_data


# find maximum key value
def maxNode(node, max_data):

    current = node

    # move only to right
    while current.right is not None:
        current = current.right

    # add max temp node to list
    max_data.append([current.data.temp, current.data.hum])
    return max_data


# calculates average of list
def calc_avg(num):

    avg = None
    sums = 0
    for t in num:
        sums = sums + t

        avg = sums / len(num)
    return avg

# find average of tuple indices in list of tuples
def list_tuple_avg(list, tuple_index):

    avg = None

    if list:
        t = [lis[tuple_index] for lis in list]
        avg = calc_avg(t)

    return avg

# get name of previous month
def find_previous_month(mo):

    monthList = ["December", "January", "February", "March", "April",
                 "May", "June", "July", "August", "September", "October", "November"]

    num = int(mo)
    num2 = (num - 1)

    last_month = monthList[num2]

    return last_month


# connect to database
def create_connection():

    conn = None

    try:
        conn = sql.connect('today.db')
    except sql.Error as e:
        print(e)

    return conn


# create tables
def create_tables(conn):

    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS today ( 
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                avgTemp REAL,
                high REAL,
                low REAL,
                tempSwing REAL,
                avgHum REAL,                         
                avgFreezeHum REAL,
                avgHotHum REAL                        

            )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS month (
                id INTEGER primary key,
                monthName TEXT,           
                avgTemp REAL,
                high REAL,
                low REAL,
                tempSwing REAL,
                avgHum REAL,
                avgFreezeHum REAL,
                avgHotHum REAL                                                                          

            )""")
    conn.commit()


# insert daily record
def insert_today(conn):

    # insert tuple as record
    cur = conn.cursor()
    cur.execute("INSERT INTO today (avgTemp, high, low, tempSwing, avgHum, avgFreezeHum, avgHotHum)"
                " VALUES (?,?,?,?,?,?,?)", (a, b, c, d, e, f, g))  # record
    conn.commit()


def select_today(conn, last_month):
    # insert tuple as record
    cur = conn.cursor()
    cur.execute("SELECT MAX(high), MIN(low), MAX(tempSwing) FROM today")
    selection = (cur.fetchall())
    high = selection[0][0]
    low = selection[0][1]
    swing = selection[0][2]
    cur.execute("SELECT COUNT(high) FROM today WHERE avgHum > 80")
    sel = (cur.fetchall())
    dd = sel[0][0]
    cc = str(dd)

    # display data/statistics
    print("Daily Extremes for the Previous Month (", last_month, ")")
    print("High Temperature: ", high)
    print("Low Temperature: ", low)
    print("High Daily Swing: ", swing)
    print("Humid Days: ", cc)
    print()


def insert_select_month(conn, prev_mo):

    # insert tuple as record
    cur = conn.cursor()
    cur.execute(("INSERT INTO month (avgTemp, high, low, tempSwing, avgHum, avgFreezeHum, avgHotHum)"
                 " SELECT avg(avgTemp), avg(high), avg(low), avg(tempSwing), "
                 "avg(avgHum), avg(avgFreezeHum), avg(avgHotHum) FROM today"))
    conn.commit()

    # add month name into record
    lastRecord = (cur.lastrowid)
    cur.execute("UPDATE month SET monthName=? WHERE ID=?", (prev_mo, lastRecord))
    conn.commit()

    # count number of records
    cur.execute("SELECT COUNT(*) FROM month")
    sel = (cur.fetchall())
    dd = sel[0][0]
    cc = str(dd)

    # select most recend record
    cur.execute("SELECT * FROM month WHERE id=?", cc)
    selection = (cur.fetchall())

    # generate output variables
    avg = selection[0][2]
    high = selection[0][3]
    low = selection[0][4]
    swing = selection[0][5]
    hum = selection[0][6]
    freeze = selection[0][7]
    hot = selection[0][8]

    # display data/statistics
    print("Monthly Averages For The Previous Month (", prev_mo, ")")
    print("Average Temperature: ", avg)
    print("Average High Temperature: ", high)
    print("Average Low Temperature: ", low)
    print("Average Swing: ", swing)
    print("Average Humidity: ", hum)
    print("Average Humidity When Temp Below Freezing: ", freeze)
    print("Average Humidity When Temp > 85 Degrees: ", hot)


def select_month(conn):
    # insert tuple as record
    cur = conn.cursor()
    cur.execute("SELECT * FROM month WHERE monthName")
    allday = (cur.fetchall())
    high = allday[0][0]
    print(high)




if __name__ == '__main__':

    while True:

        # check local time
        curr_time = time.localtime()
        curr_clock = time.strftime("%H:%M:%S", curr_time)

        try:
            # read sensor data all day, every 10 minutes(600), approx. 144/day
            if curr_clock < '23:59:00':
                readData()
                sleep(5)

            # last minute of day: begin operations
            else:

                root = None

                # int appended to string to create unique keys
                j = 1

                # iterate sensor data list
                for index, tuple in enumerate(sensorData):
                    element_one = tuple[0]
                    element_two = tuple[1]

                    # create new node parameter variables
                    read = reading(element_one, element_two)
                    x = str(element_one) + str(j)
                    yy = float(x)

                    # insert node with unique key into tree
                    root = insert(root, yy, read)
                    j = j + 1

                # call tree functions that read, then write to lists
                allList = inorder(root, [])
                range1 = range(root, 0, 75.5, [])
                range2 = range(root, 75.5, 80.0, [])
                minList = minNode(root, [])
                maxList = maxNode(root, [])

                # calculate daily data/stats for database
                a = list_tuple_avg(allList, 0)
                b = maxList[0][0]
                c = minList[0][0]
                d = round(maxList[0][0] - minList[0][0], 1)
                e = list_tuple_avg(allList, 1)
                f = list_tuple_avg(range1, 0)
                g = list_tuple_avg(range2, 1)

                # connect to db and initialize cursor
                conn = create_connection()
                cur = conn.cursor()

                # SQL statements
                create_tables(conn)
                insert_today(conn)

                # get index of day and month value in datestring
                datestring = str(datetime.datetime.now())
                # string[ start_index_pos: end_index_pos: step_size]
                day = datestring[8: 10]
                month = datestring[5: 7]

                # get name of previous month
                previousMonth = find_previous_month(month)

                # create last month's record if first of month
                if day == '01':
                    # insert month SQL
                    select_today(conn, previousMonth)
                    insert_select_month(conn, previousMonth)

                # delete temp tables (for testing only)
                cur.execute("DROP TABLE today")
                cur.execute("DROP TABLE month")
                conn.commit
                conn.close()

                # wait at least until next day begins (local time)
                sleep(60)

        # handle input/output error
        except IOError:
            print("Error")

        # handle keyboard interrupt exit
        except KeyboardInterrupt as e:
            print(str(e))

            break



