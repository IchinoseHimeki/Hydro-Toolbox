# -*- coding=utf-8 -*-
'''
File: Met_Extraction.py
File Created: 2021-05-11 21:14:33
Author: IchinoseHimeki (darwinlee19980811@hotmail.com)
-----
Last Modified: 2022-01-21 15:20:41
Modified By: IchinoseHimeki (darwinlee19980811@hotmail.com>)
-----
Copyright 2022
Requisite: Python 3.10+
Description: This script is convert files from http://stdown.agrivy.com/, which is in a .met format. From
'''

import os
import sys
import csv
import re

# Dir Structure
Dir45 = 'E:/Project/CMIP5/FILE/45/'
Out45 = 'E:/Project/CMIP5/FILE/45CSV/'
Dir85 = 'E:/Project/CMIP5/FILE/85/'
Out85 = 'E:/Project/CMIP5/FILE/85CSV/'
startTime = '1919'
endTime = '2050'


def create_csv(Location, Kind, Date):
    path = Location+Kind+Date+'.csv'
    if(not(os.path.exists(path))):
        with open(path, 'w', newline='') as f:
            csv_write = csv.writer(f)
            csv_head = ["LOC", "LON", "LAT", Kind]
            csv_write.writerow(csv_head)


def write_csv(Location, Kind, Date, Data):
    path = path = Location+Kind+Date+'.csv'
    with open(path, 'a', newline='') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(Data)

# Get Location Coordinate, feel free to add new. Name is the ID of the observation station, Coordinate is "Lon. Lat."


def getLocation(name):
    if(name == "11451"):
        return "22.33","44.55"
    elif(name == "51419"):
        return "125.25","66.66"
    elif(name == "19810"):
        return "119.1","81.0"


def read_met45():
    global startTime, endTime
    Out45PRE = Out45+"PRE/"
    Out45ETo = Out45+"ETo/"
    Dirs45 = os.listdir(Dir45)
    for files in Dirs45:
        fileName = Dir45 + files
        name = files[0:5]
        location = getLocation(name)
        with open(fileName, "r") as f:
            line = f.readlines()
            for l in line:
                newLine = re.split(r'(?:\s)\s*', l)
                if((newLine[0] >= startTime) & (newLine[0] <= endTime):
                    Date=newLine[0]+newLine[1]
                    DataPRE=[name, location[0], location[1], newLine[5]]
                    DataETo=[name, location[0], location[1], newLine[6]]
                    create_csv(Out45PRE, 'PRE', Date)
                    create_csv(Out45ETo, 'ETo', Date)
                    write_csv(Out45PRE, 'PRE', Date, DataPRE)
                    write_csv(Out45ETo, 'ETo', Date, DataETo)
                else:
                    continue

def read_met85():
    global startTime, endTime
    Out85PRE=Out85+"PRE/"
    Out85ETo=Out85+"ETo/"
    Dirs85=os.listdir(Dir85)
    for files in Dirs85:
        fileName=Dir85 + files
        name=files[0:5]
        location=getLocation(name)
        with open(fileName, "r") as f:
            line=f.readlines()
            for l in line:
                newLine=re.split(r'(?:\s)\s*', l)
                if((newLine[0] >= startTime) & (newLine[0] <= endTime)):
                    Date=newLine[0]+newLine[1]
                    DataPRE=[name, location[0], location[1], newLine[5]]
                    DataETo=[name, location[0], location[1], newLine[6]]
                    create_csv(Out85PRE, 'PRE', Date)
                    create_csv(Out85ETo, 'ETo', Date)
                    write_csv(Out85PRE, 'PRE', Date, DataPRE)
                    write_csv(Out85ETo, 'ETo', Date, DataETo)
                else:
                    continue

if __name__ == "__main__":
    read_met45()
    read_met85()
