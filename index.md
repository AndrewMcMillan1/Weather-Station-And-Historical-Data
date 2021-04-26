# Andrew McMillan's ePortfolio

## Professional Self-Assessment

  The capstone course provided the opportunity to review and reexamine material from previous courses and to enhance select projects from those courses. This ePortfolio contains that enhanced work and highlights my strengths as a developer in both an individual and collaborative context. The creation process has reinforced my computer science education as a whole and prepared me to work in a variety of modern team environments and project management methodologies. I am comfortable using different tools and strategies that facilitate development and collaboration in the software development life cycle. Working on physical science data applications such as this would be ideal for me as a professional in the computer science field.  
  
  The course simulated the software development life cycle and emphasized team collaboration and transparency with stakeholders. I created an early narrative that identified potential use cases for various artifact enhancements. I believe my ultimate choice of application design is a positive indicator of my practicality, and that the application concept has market appeal. I supported a collaborative environment by creating the narratives, code review, and milestone deliverables, incorporating feedback from those, and by providing periodic progress updates to my instructor. One of the best quality control methods is code review. The code review video identifies inefficiencies and security flaws with the original artifacts and envisions specific design, algorithmic, and database solutions. Video communication and presentation software skills are in demand in these times of distributed teams and remote work. They are excellent tools for information sharing and communicating with stakeholders. Competence with version control tools and techniques is critical for individuals and collaborators. I used the GitHub repository and my local machine for effective version control that maintains the history of enhancements and demonstrates the ability to use branching and merging to safely develop new features.
  
  Enhancements were required in each of the three categories: design and architecture, data structures and algorithms, and database. Security was also a heavily emphasized requirement. The temperature and humidity artifact that the overall design is based on was heavily altered and enhanced. The original program was basically a temperature and humidity sensor reader with simple conditional lighting variations. I converted it into a weather station plus historical data application that reads temperature and humidity data, and through numerous processes and manipulation, converts it into daily and monthly statistical records and displays them. I believe it showcases my ability as a developer to take limited input and create much more. The algorithmic/data structure enhancement centers around a self-balancing AVL tree but includes more additional functions and structures. There are numerous feature additions that show an ability to adapt the artifact to the specific programming task. The database enhancement involves heavy use of aggregate functions. These are very important in data analytics which is of growing importance in nearly every field.
  
  Secure coding is a critical practice. It tends to be less of an issue with Python, and the program takes no input and has no external data file dependencies, but there are potential crash points. The sensor data must be numbers because the tree functions require data type consistency for Boolean comparisons, and that same data goes through mathematical operations in lists that must have consistent numerical data types. Certain operations cannot be performed on empty lists, which do occur frequently when the tree range searches return nothing. Those conditions are checked to prevent crashes. The data can become corrupted if data structures are not emptied after each cycle. The entire tree and all the lists need to be emptied so it doesn’t append to previous day’s data and corrupt the data or cause overflows. Accessing the database also has risks. I made sure the connection was made and handled the exception, otherwise. 
  
  The biggest challenge was the transformation of three separate and unrelated artifacts into one. That meant altering each artifact in a way that would make them compatible. That takes a lot of planning and structured development, and that’s why project management and development frameworks are important. The weather station is designed to run continuously. It requires timing mechanisms that regulate the number of sensor readings, schedule function calls to perform CRUD operations on the data, and schedule record inserts at the end of the day and month. All three components are regulated by timer mechanisms. The data from the sensor is read with the sensor function every few minutes. At the very end of the day, that data is inserted into the tree node structures, sorted by temperature. Multiple functions calls read the tree data and write to data structures. Non-tree functions then extract the data and perform a few calculations to generate statistic value variables that become the column values of one daily record. After daily record insertion, the date is checked. If it is the first of the month, all the records are aggregated, and a new monthly record is generated for the monthly table.    
  
## The Weather Station and Historical Data App

```python
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

    
# Driver Code
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
                
                # delete lists in preperation for new day of data
                del sensorData[:]
                del allList[:]
                del range1[:]
                del range2[:]
                del minList[:]
                del maxList[:]

                # wait at least until next day begins (local time)
                sleep(60)

        # handle input/output error
        except IOError:
            print("Error")

        # handle keyboard interrupt exit
        except KeyboardInterrupt as e:
            print(str(e))

            break


```
## Narratives

# Architecture and Design

  The artifact is the Raspberry pi and Grove pi weather station that collects temperature and humidity data from a sensor and performs numerous data structure, algorithmic, and database operations to transform temperature and humidity input into more complex historical records containing multiple metrics and statistics. I included this artifact because I imagined the simple “gather and display” design could expand into a much heavier data analysis and presentation. This artifact shows an ability to take raw and limited data through a long process to generate entirely new information. Timers handle the cycles of sensor reading, function calls, and database work. It was a challenge to test the program because the app is intended to continuously run, and the monthly table receives only one record a month. I shortened the timescales dramatically to witness the month table populating with data and the display functions displaying it.   
  
# Data Structures and Algorithms

  The Data structure is a self-balancing AVL tree, sorted by temperature in ascending order, consisting of nodes that contain the temperature and humidity data. Multiple functions traverse the tree and return data, such as an in-order traversal, range search, minimum value, and maximum value. The tree was chosen because it is more of a programming challenge and has very interesting set of algorithms that perform operations on the nodes. The enhancements include adding functions that fit the types of data reeds needed to capture interesting data. I adapted to more efficient recursive algorithms from the original artifact. Multiple other non-tree functions perform additional operations like calculations and data manipulation. 

# Database

  The database element is an SQLite3 database that takes data from the various data structure reads and calculations, stores the data in a daily stats table that fills up for a month, and makes use of SQL aggregate functions while moving data from the daily table to the monthly table. The artifact was chosen because SQLite is built into python and the overall design and database aspect could be enhanced by making heavy use of aggregate functions among other more complex queries. I learned that SQL can be complex, and that the process of working with data and doing meaningful analysis with it can be time consuming when hard coding.   


# Database

```python
# Here is some in python
def foo():
  print 'foo'
```  


You can use the [editor on GitHub](https://github.com/AndrewMcMillan1/AndrewMcMillan1/edit/gh-pages/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for


Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

