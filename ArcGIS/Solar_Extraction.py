# -*- coding: utf-8 -*-
'''
File: Solar_Extraction.py
File Created: 2022-03-27 15:27:41
Author: Darwin Lee (darwinlee19980811@hotmail.com)
-----
Last Modified: 2022-03-28 19:48:25
Modified By: Darwin Lee (darwinlee19980811@hotmail.com>)
-----
Copyright 2022
Requisite: ArcPy 10.x with Python 2.7.x
Description: Fix file header, define projection, extract by mask and extract all values into CSV.
'''

import arcpy
from arcpy.sa import *

import datetime
import csv
import os
import shutil
import multiprocessing

globalPath=os.getcwd()
fileList=os.listdir(globalPath+"\\input\\")
modHeader=["ncols 7200\n","nrows 3600\n","xllcorner -180\n","yllcorner -90\n","cellsize 0.05\n","NODATA_value -999900\n"]
arcpy.CheckOutExtension("Spatial")

def check():
    if not os.path.exists(globalPath+"\\middle\\"):
        os.mkdir(globalPath+"\\middle\\")
        os.mkdir(globalPath+"\\middle\\rawasc\\")
        os.mkdir(globalPath+"\\middle\\modasc\\")
        os.mkdir(globalPath+"\\middle\\modRaster\\")
        os.mkdir(globalPath+"\\middle\\clipped\\")
        os.mkdir(globalPath+"\\middle\\convertasc\\")
    else:
        shutil.rmtree(globalPath+"\\middle\\")
        os.mkdir(globalPath+"\\middle\\")
        os.mkdir(globalPath+"\\middle\\rawasc\\")
        os.mkdir(globalPath+"\\middle\\modasc\\")
        os.mkdir(globalPath+"\\middle\\modRaster\\")
        os.mkdir(globalPath+"\\middle\\clipped\\")
        os.mkdir(globalPath+"\\middle\\convertasc\\")
    print("Checked.\n")
    pass


def convertDate(txt): # Convert 2010001 into 2010-01-01
    year=int(txt[0:4])
    date=int(txt[4:7])
    baseTime=datetime.date(year-1,12,31)
    targetTime=baseTime+datetime.timedelta(days=date)
    formatTime=targetTime.strftime("%Y-%m-%d")
    return formatTime

def extractValue(file): # Extract all no null data into one line.
    data=[]
    splitData=[]
    with open(file,"r") as f:
        rawData=f.readlines()
    del rawData[0:6]
    for i in rawData:
        splitData.append(i.split(" "))
    for i in splitData:
        for j in i:
            if j != "-9999" and j != "\n": # Friendly reminder: "\n"
                data.append(str(float(j)/100)) # Divide by 100 to make data reliable.
    return data

def mainProcedure(file): # Since the process is not too complex, they are put altogether.
    data=[]
    outFileName=str(file)[7:14]
    rawData=[]
    date=convertDate(outFileName)
    data.append(date)
    arcpy.RasterToASCII_conversion(globalPath+"\\input\\"+file,globalPath+"\\middle\\rawasc\\"+outFileName+".txt")
    with open(globalPath+"\\middle\\rawasc\\"+outFileName+".txt","r") as f:
        rawData=f.readlines()
        del rawData[0:6]
    with open(globalPath+"\\middle\\modasc\\"+outFileName+".txt","a") as f:
        f.writelines(modHeader)
        f.writelines(rawData)
    os.mkdir(globalPath+"\\middle\\modRaster\\"+outFileName+"\\") # Avoid file conflicts caused by ArcGIS.
    arcpy.ASCIIToRaster_conversion(globalPath+"\\middle\\modasc\\"+outFileName+".txt",globalPath+"\\middle\\modRaster\\"+outFileName+"\\"+outFileName+".tif","FLOAT")
    arcpy.DefineProjection_management(globalPath+"\\middle\\modRaster\\"+outFileName+"\\"+outFileName+".tif",arcpy.SpatialReference(4326))
    clippedRaster=ExtractByMask(globalPath+"\\middle\\modRaster\\"+outFileName+"\\"+outFileName+".tif",globalPath+"\\clip\\mask.shp")
    clippedRaster.save(globalPath+"\\middle\\clipped\\"+outFileName+".tif")
    arcpy.RasterToASCII_conversion(globalPath+"\\middle\\clipped\\"+outFileName+".tif",globalPath+"\\middle\\convertasc\\"+outFileName+".txt")
    extractData=extractValue(globalPath+"\\middle\\convertasc\\"+outFileName+".txt")
    for i in extractData:
        data.append(i)
    shutil.rmtree(globalPath+"\\middle\\modRaster\\"+outFileName+"\\") # Data took so many space, so wipe it after the file was processed.
    os.remove(globalPath+"\\middle\\rawasc\\"+outFileName+".txt") 
    os.remove(globalPath+"\\middle\\modasc\\"+outFileName+".txt") 
    os.remove(globalPath+"\\middle\\convertasc\\"+outFileName+".txt") 
    print(outFileName+" is done.\n") 
    return data

if __name__ == '__main__':
    check()
    
    pool0=multiprocessing.Pool(multiprocessing.cpu_count())
    csvData=pool0.map_async(mainProcedure,fileList).get()
    pool0.close()
    pool0.join()
    print("Data Gathered.\n")
    with open(globalPath+"\\Results.csv","ab") as f:
        csvWriter=csv.writer(f)
        csvWriter.writerow(["Date","Data"])
        csvWriter.writerows(csvData)

