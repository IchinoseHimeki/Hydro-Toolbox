# -*- coding=utf-8 -*-
import os
import sys
import csv
import re
'''
This script is convert files from http://stdown.agrivy.com/, which is in a .met format. From
'''
# Dir Structure
Dir45 = 'E:/Project/CMIP5/FILE/45/'
Out45 = 'E:/Project/CMIP5/FILE/45CSV/'
Dir85 = 'E:/Project/CMIP5/FILE/85/'
Out85 = 'E:/Project/CMIP5/FILE/85CSV/'
startTime = '2020'
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
    if(name == "50727"):
        return "119.56", "47.1"
    elif(name == "50834"):
        return "121.13", "46.36"
    elif(name == "50838"):
        return "122.05", "46.08"
    elif(name == "50936"):
        return "122.5", "45.38"


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