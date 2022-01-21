'''
File: PRE_Extract.py
File Created: 2021-11-27 00:38:33
Author: IchinoseHimeki (darwinlee19980811@hotmail.com)
-----
Last Modified: 2022-01-21 15:04:11
Modified By: IchinoseHimeki (darwinlee19980811@hotmail.com>)
-----
Copyright 2022
Requisite: Python 3.10+
Description: Split accmulated PRE into pre period PRE.
'''

import os
import csv
import datetime
import math

globalPath=os.getcwd()
step=30 # Time Step(minutes)

def constructHead(data): # Construct [datetime,[datetime_str,0.0]]
    ran=math.ceil(((data[len(data)-1][0]-data[0][0]).seconds+(3600*24*(data[len(data)-1][0]-data[0][0]).days))/60/step)+1# Date.seconds is not the converted seconds, it need to plus 3600*24*date.days, also +1 is needed since the step could be exact.
    timeList=[] #Datetime
    strTimeList=[] #str(Datetime)
    for i in range(ran):
        timeList.append(data[0][0]+datetime.timedelta(minutes=step*i)) #Add specific time step
    for i in timeList:
        strTimeList.append([datetime.datetime.strftime(i,"%Y-%m-%d %H:%M:%S"),0.0])
    return [timeList,strTimeList]
def constructTime(raw): # Convert MM/DD/YY 上午hh时mm分ss秒 into datetime
    str=raw.replace("上午","AM").replace("下午","PM")
    time=datetime.datetime.strptime(str,"%m/%d/%y %p%I时%M分%S秒")
    return time
def readCsv(path): # Read Time,PRE leaving all empty behind [datetime, Measured Value]
    data=[]
    with open (path,"r",newline="",encoding="utf-8") as f: # using Chinese Characters
        reader=csv.reader(f)
        next(f)
        next(f) # Skip Two Rows
        for i in reader:
            if i[3]=="": # Make empty PRE into 0-> Skip empty data
                # i[3]="0"
                continue
            data.append([constructTime(i[1]),float(i[3])]) 
    return data
def constructData(data): # remapping data in one,[datetime, measured value]+[datetime[str(datetime),0.0]]->[str(datetime), Accmulated PRE]
    head=constructHead(data)
    for i in range(len(data)):
        tempList=[]
        for j in range(len(head[0])):
            tempList.append(((head[0][j]-data[i][0]).seconds+((head[0][j]-data[i][0]).days*3600*24))/60/step) # Calculate how many steps are passed, so weired that here does not need +1, perhaps a potential bug.
        for j in range(len(tempList)): # Exclude values which < 0
            if tempList[j]<0: 
                tempList[j]=114514 
        tempDis=min(tempList) # get the minium data
        if tempDis < 1: # Only choose data distance smaller than 1 step.
            location=tempList.index(tempDis)
            head[1][location][1]=data[i][1]
            # print(str(location)+" "+str(head[1][location][1]))
        else:
            continue
    return head[1]

def calcList(inputData): # Split accumulated preceptation into single one [Time, PRE]->[Time, Splited PRE]
    without0=[]
    minusedData=[]
    for i in inputData: # Clean all zero value
        if i[1]!=0:
            without0.append(i)
    for i in range(1,len(without0)): # Minus data
        minusedData.append([without0[i][0],format((without0[i][1]-without0[i-1][1]),".1f")]) # Convert error data into 0.x
    for i in range(len(minusedData)): # Construct Data, replace inputData's 0.0 by minusedData if matched
        for j in range(len(inputData)):
            if minusedData[i][0]==inputData[j][0]:
                inputData[j][1]=minusedData[i][1] # Copy data into results.
                break
    return inputData
    
def printResult(path): # Print Result
    data=calcList(constructData(readCsv(path)))
    with open(globalPath+"\\Res_"+str(step)+".csv","a+",newline="") as f:
        writer=csv.writer(f)
        writer.writerow(["Time","PRE"])
        writer.writerows(data)
    pass

if __name__ == "__main__":
    printResult(globalPath+"\\test.csv")
