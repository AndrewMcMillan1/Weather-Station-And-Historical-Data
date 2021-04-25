# !/usr/bin/env python

import math
import time
import grovepi
import json
from time import sleep
from grovepi import *
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


# The function prints all the keys in the gicven range
# [k1..k2]. Assumes that k1 < k2
def range(root, low, k2, range_list):
    # Base Case
    if root is None:
        return

    # move toward low end of range
    if low < root.key:
        range(root.left, low, k2, range_list)

    # If data is in range
    if low <= root.key and k2 > root.key:

        # add in-range data to list
        range_list.append(root.data.temp)

    # move toward high end of range
    if k2 > root.key:
        range(root.right, low, k2, range_list)

    return range_list

# inorder traversal function
def inorder(root, order_list):

    if root is not None:

        # move to left subtree
        inorder(root.left)

        # add data to list
        order_list.append([root.data.temp, root.data.hum])

        # move to right subtree
        inorder(root.right)

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
    while current.left != None:
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


if __name__ == '__main__':

    while True:

        # check local time
        time = time.localtime()
        strTime = time.strftime("%H:%M:%S", time)

        try:
            # read sensor data all day, about every 10 minutes
            if strTime < '19:31:00':
                readData()
                sleep(600)

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

                # read and write data from tree
                print("Inorder traversal")
                allList = inorder(root)
                print("below freezing")
                range1 = range(root, 0, 32.0, [])
                print("hot")
                range2 = range(root, 10.01111, 16.019, [])
                print("min")
                minList = minNode(root, [])
                print("max")
                maxList = maxNode(root, [])

                print("all")
                for i in allList:
                    print(i)

                print("freezing")
                for i in range1:
                    print(i)

                print("hot")
                for i in range2:
                    print(i)

                print("minimum")
                for i in minList:
                    print(i)

                print("maximum")
                for i in maxList:
                    print(i)

                # wait at least until next day begins (local time)
                sleep(60)

        except IOError:
            print("Error")

        except KeyboardInterrupt as e:
            print(str(e))

            break



