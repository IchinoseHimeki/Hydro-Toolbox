# -*- coding: utf-8 -*-
'''
Author: Darwin Lee (darwinlee19980811@hotmail.com) 
Date: 2021-08-06 14:48:10 
Last Modified by: Darwin Lee (darwinlee19980811@hotmail.com)
Last Modified time: 2021-08-06 14:50:49

Please be advised that Matplotlib is REQUIRED!
This scipt will scan a few points, spilt and input measured pipe pressure data, joining data as specific, then plot them into one png.
It requires Pre/Pos.csv(Pipe pressure meter and locations), Data.csv(Measured data in day format) and Control.csv(Determine which point should be used to draw lines.)
'''
import csv
import os
import matplotlib.pyplot as plt
import datetime
import shutil
import itertools
import matplotlib
from multiprocessing import Pool

globalPath=os.getcwd()
matplotlib.rc("font",family='STSong')

def check():
    global path
    if not os.path.exists(globalPath+"//Pre//Data.csv"):
        raise IOError()
    if not os.path.exists(globalPath+"//Pre//Control.csv"):
        raise IOError()
    if not os.path.exists(globalPath+"//Pre//Pos.csv"):
        raise IOError()
    if os.path.exists(globalPath+"//Data"):
        shutil.rmtree(globalPath+"//Data")
        os.mkdir(globalPath+"//Data")
    else:
        os.mkdir(globalPath+"//Data")
    if os.path.exists(globalPath+"//Res"):
        shutil.rmtree(globalPath+"//Res")
        os.mkdir(globalPath+"//Res")
    else:
        os.mkdir(globalPath+"//Res")
    pass

def spiltData(path,printPath): ## Spilt Data.csv into sperated data
    time=[]
    points=[]
    rawTime=[]
    rawPoints=[]
    with open (path,"r+") as f:
        csvFile = csv.reader(f)
        next(csvFile)
        for i in csvFile:
            if len(i)<7:
                raise BaseException("There should be 6 point data, plus 1 date. So 7 data is required!")
            for j in i:
                if j=='':
                    raise BaseException("Check csv file in Notepad! There should be data after every \",\"!")
            rawTime.append(datetime.datetime.strptime(i[0],"%Y/%m/%d"))
            rawPoints.append([i[1],i[2],i[3],i[4],i[5],i[6]])
        for i in range(len(rawTime)):
            if not rawTime[i] in time:
                time.append(rawTime[i])
                points.append(rawPoints[i])
            else:
                info=datetime.datetime.strftime(rawTime[i],"%Y/%m/%d")+"'s data is duplicated! Only the first one is considered!\n"
                printWarnings(info)
                print(info)
                continue
        for i in range(len(time)):
            printTime=datetime.datetime.strftime(time[i],"%Y-%m-%d")
            with open (printPath+"//Data//"+printTime+".csv","w",newline="") as f:
                csvWrite=csv.writer(f)
                csvWrite.writerow(["Date","1","2","3","4","5","6"])
                data=[str(printTime)]
                data.extend(points[i])
                csvWrite.writerow(data)
    pass

def readData(path): ## Read spilted data, return [time,points[]]
    x=readPos(globalPath+"//Pre//Pos.csv")[0]
    points=[]
    with open (path,"r") as f:
        csvFile=csv.reader(f)
        next(csvFile)
        for i in csvFile:
            time=i[0]
            for j in range(1,7):
                points.append([float(x[j-1]),float(i[j])])
    return [time,points]

def readPos(path): ## Read Pos.csv into List, return newPos[]
    rawPoints=[]
    rawX=[]
    points=[]
    x=[]
    with open(path,'r+') as f:
        csvFile = csv.reader(f)
        next(csvFile)
        for i in csvFile:
            rawPoints.append(i[0])
            rawX.append(i[1])
        if len(rawPoints)!=len(rawX):
            raise BaseException("Points and Xs are not matched!")
        for i in range(len(rawPoints)):
            if not rawPoints[i] in points and not rawX[i] in x:
                points.append(rawPoints[i])
                x.append(float(rawX[i]))
            else:
                continue
        if len(points)<6:
            raise BaseException("At least 6 points are considered!")
        if len(points)>6:
            info="Warning: More than 6 positions found! Removing others!\n"
            printWarnings(info)
            print(info)
            points=points[0:6]
            x=x[0:6]
    return x,points

def readControl(path): ## Read Control.csvo into List, return control[]
    points=readPos(globalPath+"//Pre//Pos.csv")[1]
    control=[]
    rawControl=[]
    with open (path, "r+") as f:
        csvFile=csv.reader(f)
        next(csvFile)
        for i in csvFile:
            flag=False
            for j in i:
                if j not in points:
                    info="Point "+ str(j) + " is not defined! This line is going to be ignored!\n"
                    printWarnings(info)
                    print(info)
                    flag=False
                    break
                flag=True
            if flag:
                rawControl.append(i)
            for i in range(len(rawControl)):
                rawControl[i].sort()
                if rawControl[i][0]==rawControl[i][1]:
                    info="Point "+str(rawControl[i][0])+" is matched with itself!\n"
                    printWarnings(info)
                    print(info)
                    rawControl.remove(rawControl[i])
            for i in range(len(rawControl)):
                if not rawControl[i] in control:
                    control.append(rawControl[i])                
    return control

def printWarnings(info): ## Writing warning log into Warns.log
    time=datetime.datetime.now()
    printTime=time.__format__("%Y-%m-%d %H:%M:%S")
    with open(globalPath+"//Warns.log","a+",newline='') as f:
        f.writelines(printTime+" "+info)
    pass

def toPrintEquation(eq): ## Convert [k,b] into y=kx+b
    if eq[1]<0:
        toB=str(eq[1])
    else:
        toB="+"+str(eq[1])
    return "y="+str(eq[0])+"x"+toB

def mathEquation(p1,p2): ## Construct [k,b] by given [x1,y1] and [x2,y2]
    k=(p1[1]-p2[1])/(p1[0]-p2[0])
    b=p1[1]-k*p1[0]
    if k==0:
        info=str(p1)+str(p2)+" are paralleled with x axis! please check if points are correctly matched!\n"
        printWarnings(info)
        print(info)
    return [k,b]

def crossing(eq1,eq2): ## Finding Crossing by given [k1,b1] and [k2,b2]
    if eq1[0]==eq2[0]:
        return
    x=(eq2[1]-eq1[1])/(eq1[0]-eq2[0])
    y=eq1[0]*x+eq1[1]
    return [x,y]

def plotData(path): # Prepare the data to plot
    control=readControl(globalPath+"//Pre//Control.csv")
    points=[]
    num=0
    data=readData(path)
    time=data[0]
    equations=[]
    crossingPoints=[]
    plotPointsX=[]
    plotPointsY=[]
    plotCrossingPointsX=[]
    plotCrossingPointsY=[]
    for i in range(len(data[1])):
        plotPointsX.append(data[1][i][0])
        plotPointsY.append(data[1][i][1])
    plotPoints=[plotPointsX,plotPointsY]
    for i in control:
        pointData=[]
        for j in i:
            pointData.extend([data[1][int(j)-1]])
        points.append([num,pointData])
        num+=1
    crossingList=list(itertools.combinations(points,2))
    for i in range(len(points)):    
        equations.append(toPrintEquation(mathEquation(points[i][1][0],points[i][1][1])))
    for i in range(len(crossingList)):
        crossingPoints.append(crossing(mathEquation(crossingList[i][0][1][0],crossingList[i][0][1][1]),mathEquation(crossingList[i][1][1][0],crossingList[i][1][1][1])))
    crossingPoints = list(filter(None, crossingPoints))
    for i in range(len(crossingPoints)):
        plotCrossingPointsX.append(crossingPoints[i][0])
        plotCrossingPointsY.append(crossingPoints[i][1])
    plotCrossingPoints=[plotCrossingPointsX,plotCrossingPointsY]
    plot(time,plotPoints,equations,plotCrossingPoints)
    
    pass

def plot(time,dataList,equations,crossingPoints):
    control=readControl(globalPath+"//Pre//Control.csv")
    color=["b","g","r","c","m","#66ccff","#39c5bb","#114514","#191981","#984432"]
    fig, ax = plt.subplots()
    ax.scatter(dataList[0],dataList[1],c="k",marker="x",label="Measured Data")
    ax.scatter(crossingPoints[0],crossingPoints[1],c="r",marker="*",label="Possible Leaking")
    for i in range(len(crossingPoints[0])):
        ax.text(crossingPoints[0][i]+3,crossingPoints[1][i]+3,"Leak ("+str(crossingPoints[0][i])[:5]+","+str(crossingPoints[1][i])[:5]+")")
    for i in range(len(dataList[0])):
        ax.axvline(dataList[0][i],c="#C1C1C1",linestyle="--")
        # ax.text(dataList[0][i],100,str(points[i]))
    for i in range(len(control)):
        xy1=[dataList[0][int(control[i][0])-1],dataList[1][int(control[i][0])-1]]
        xy2=[dataList[0][int(control[i][1])-1],dataList[1][int(control[i][1])-1]]
        plt.axline(xy1,xy2,c=color[i],label=equations[i])
    ax.spines[["top"]].set_visible(False)
    ax.set_title(str(time)+" 各测点压力分布图",fontsize=18)
    ax.set_ylabel("P (m)")
    ax.set_xlabel("Location(m)")
    plt.savefig(globalPath+"//Res//"+str(time)+".png")
    pass

if __name__ == "__main__":
    startTime = datetime.datetime.now()
    print("Pipe Leak Identification V1.0")
    check()
    print("Data are Ok to go!")
    spiltData(globalPath+"//Pre//Data.csv",globalPath)
    print("Data Spilted!")
    pool=Pool(os.cpu_count())
    csvList=os.listdir(globalPath+"//Data//")
    for i in range(len(csvList)):
        csvList[i]=globalPath+"//Data//"+str(csvList[i])
    pool.map_async(plotData,csvList)
    pool.close()
    pool.join()
    print("Finished!")
    endTime = datetime.datetime.now()
    elapsedSec = (endTime - startTime).total_seconds()
    print("Total Used:" + "{:.2f}".format(elapsedSec) + " seconds.")