# -*- coding=utf-8 -*-
'''
Please be advised that h5py is REQUIRED!
This program output some h5 data into one csv.
'''
import os
import shutil
from multiprocessing import Pool
from multiprocessing import cpu_count
import csv
import h5py

globalPath=os.getcwd()+"\\"

x1=2
y1=2
x2=4
y2=4

def check():
    if not os.path.exists(globalPath + "\\HDFs\\") or not os.listdir(globalPath + "HDFs\\"):
        raise IOError("HDF files are not given, please check!\n")

    # if not os.path.exists(globalPath + "Base\\") or not os.listdir(globalPath + "Base\\"):
        # raise IOError("The interplotion area is not specificed, please check!\n")

    if os.path.exists(globalPath + "Middle\\"):
        shutil.rmtree(globalPath + "Middle\\")
        os.mkdir(globalPath + "Middle\\")
        os.mkdir(globalPath + "Middle\\SD\\")
        os.mkdir(globalPath + "Middle\\SWE\\")
        os.mkdir(globalPath + "Middle\\ASCs\\")
        os.mkdir(globalPath + "Middle\\ASCs\\SD")
        os.mkdir(globalPath + "Middle\\ASCs\\SWE")
    else:
        os.mkdir(globalPath + "Middle\\")
        os.mkdir(globalPath + "Middle\\SD\\")
        os.mkdir(globalPath + "Middle\\SWE\\")
        os.mkdir(globalPath + "Middle\\ASCs\\")
        os.mkdir(globalPath + "Middle\\ASCs\\SD")
        os.mkdir(globalPath + "Middle\\ASCs\\SWE")

    if os.path.exists(globalPath + "Results\\"):
        shutil.rmtree(globalPath + "Results\\")
        os.mkdir(globalPath + "Results\\")
    else:
        os.mkdir(globalPath + "Results\\")

    print("All is ready to go!\n")
    pass

def extractValue(HDF):
    global x1,x2,y1,y2
    sdData=[]
    sdRes=[]
    sweData=[]
    sweRes=[]
    startX=x1-1
    startY=y1-1
    endX=x2-1
    endY=y2-1
    if endX-startX<=0 or endY-startY<=0 or endX<=0 or endY<=0 or startX<=0 or startY<=0:
        raise BaseException("XY are given incorrectly! Check inputs!")
    file=globalPath+"\\HDFs\\"+str(HDF)
    if len(HDF)==42:
        fileName=str(HDF)[14:22]
    else:
        fileName=str(HDF)[13:21]
    f=h5py.File(file,"r")
    sd = f["SD[cm]"]
    swe = f["SWE[mm]"]
    sdData=sd[:]
    sweData=swe[:]
    for i in range(len(sdData)):
        if i > startY and i <= endY:
            for j in range(len(sdData[i])):
                if j> startX and j <= endX:
                    sdRes.append(sdData[i][j])
    for i in range(len(sweData)):
        if i > startY and i <= endY:
            for j in range(len(sweData[i])):
                if j> startX and j <= endX:
                    sweRes.append(sweData[i][j])
    sdRes.insert(0,fileName)
    sweRes.insert(0,fileName)
    return [sdRes,sweRes]

def cleanup(flag):
    if flag:
        shutil.rmtree(globalPath+"Middle\\")
    pass

if __name__ == "__main__":
    
    check()
    HDFfiles=os.listdir(globalPath+"\\HDFs\\")
    pool2=Pool(cpu_count())
    allData=pool2.map_async(extractValue,HDFfiles).get()
    sdData=[]
    sweData=[]
    pool2.close()
    pool2.join()
    for i in allData:
        sdData.append(i[0])
        sweData.append(i[1])
    with open(globalPath+"SDResult.csv",'a+',newline="") as f:
        writer=csv.writer(f)
        writer.writerows(sdData)
    with open(globalPath+"SWEResult.csv",'a+',newline="") as f:
        writer=csv.writer(f)
        writer.writerows(sweData)