'''
File: snowdepth.py
File Created: 2022-03-01 23:52:41
Author: Darwin Lee (darwinlee19980811@hotmail.com)
-----
Last Modified: 2022-03-10 10:25:40
Modified By: Darwin Lee (darwinlee19980811@hotmail.com>)
-----
Copyright 2022
Requisite: Arcpy 10.x with python 2.7.x
Description: Define Projection & Reprojection & Resample Rasters, then clip it according to specific shapefile. 
'''
import arcpy
from arcpy.sa import *
from arcpy import env

import shutil
import os
import multiprocessing
import datetime

globalPath = os.getcwd()
flagClean = False

source = arcpy.SpatialReference("WGS 1984")
target = arcpy.SpatialReference(globalPath+"//clip//AEA_WGS_1984.prj") # Projection is IMPORTANT!
arcpy.CheckOutExtension("Spatial")



fileList=os.listdir(globalPath+"//input//")

def check(): # Check.
    if not os.path.exists(globalPath+"//middle//"):
        os.mkdir(globalPath+"//middle//")
        os.mkdir(globalPath+"//middle//rasters")
        os.mkdir(globalPath+"//middle//reprojection")
        os.mkdir(globalPath+"//middle//clipped")
        os.mkdir(globalPath+"//middle//fixzero//")
        os.mkdir(globalPath+"//middle//days//")
        os.mkdir(globalPath+"//middle//classify")
        os.mkdir(globalPath+"//middle//classify//fixzero")
        os.mkdir(globalPath+"//middle//classify//days")
    else:
        shutil.rmtree(globalPath+"//middle//")
        os.mkdir(globalPath+"//middle//")
        os.mkdir(globalPath+"//middle//rasters")
        os.mkdir(globalPath+"//middle//reprojection")
        os.mkdir(globalPath+"//middle//clipped")
        os.mkdir(globalPath+"//middle//fixzero//")
        os.mkdir(globalPath+"//middle//days//")
        os.mkdir(globalPath+"//middle//classify")
        os.mkdir(globalPath+"//middle//classify//fixzero")
        os.mkdir(globalPath+"//middle//classify//days")
    if not os.path.exists(globalPath+"//results//"):
        os.mkdir(globalPath+"//results//")
        os.mkdir(globalPath+"//results//fixzero")
        os.mkdir(globalPath+"//results//days")
        os.mkdir(globalPath+"//results//mean")
        
    else:
        shutil.rmtree(globalPath+"//results//")
        os.mkdir(globalPath+"//results//")
        os.mkdir(globalPath+"//results//fixzero")
        os.mkdir(globalPath+"//results//days")
        os.mkdir(globalPath+"//results//mean")
    pass

def convertDate(txt): # Convert 2010001.tif into 2010-01
    year=int(txt[0:4])
    date=int(txt[4:7])
    baseTime=datetime.date(year-1,12,31)
    targetTime=baseTime+datetime.timedelta(days=date)
    formatTime=targetTime.strftime("%Y-%m")
    return [txt.rstrip(".txt")+".tif",formatTime]

def ascToTif(file):
    arcpy.ASCIIToRaster_conversion(globalPath+"//input//"+file, globalPath+"//middle//rasters//"+file.rstrip(".txt")+".tif", "FLOAT")

def defineProjection(raster):
    arcpy.DefineProjection_management(globalPath+"//middle//rasters//"+raster,source)
    pass

def reprojectionResample(raster):
    os.mkdir(globalPath+"//middle//reprojection//"+raster.rstrip(".tif")+"//")
    arcpy.ProjectRaster_management(globalPath+"//middle//rasters//"+raster, globalPath+"//middle//reprojection//"+raster.rstrip(".tif")+"//"+raster, target, "CUBIC", "500")
    pass

def clip(raster):
    os.mkdir(globalPath+"//middle//clipped//fixzero_"+raster.rstrip(".tif")+"//")
    os.mkdir(globalPath+"//middle//clipped//days_"+raster.rstrip(".tif")+"//")
    outRaster = ExtractByMask(globalPath+"//middle//reprojection//"+raster.rstrip(".tif")+"//"+raster, globalPath+"//clip//Mask.shp")
    outRaster.save(globalPath+"//middle//clipped//fixzero_"+raster.rstrip(".tif")+"//"+raster)
    outRaster.save(globalPath+"//middle//clipped//days_"+raster.rstrip(".tif")+"//"+raster)
    pass

def calc(raster): # Fix zero & days 
    fixZeroRasterName=globalPath+"//middle//clipped//fixzero_"+raster.rstrip(".tif")+"//"+raster
    daysRasterName=globalPath+"//middle//clipped//days_"+raster.rstrip(".tif")+"//"+raster
    fixZero=Con(Raster(fixZeroRasterName)<0,0.0,fixZeroRasterName)
    fixZero.save(globalPath+"//middle//fixzero//"+raster)
    fixZero.save(globalPath+"//results//fixzero//"+raster)
    days=Con(Raster(daysRasterName)<0.5,0.0,1.0)
    days.save(globalPath+"//middle//days//"+raster)
    shutil.rmtree(globalPath+"//middle//reprojection//"+raster.rstrip(".tif")+"//")
    pass

def classify():
    lookupList=[]
    paths=[]
    for i in fileList:
        lookupList.append(convertDate(i))

    for i in range(len(lookupList)):
        if not lookupList[i][1] in paths:
            paths.append(lookupList[i][1])
            os.mkdir(globalPath+"//middle//classify//fixzero//"+lookupList[i][1]+"//")
            os.mkdir(globalPath+"//middle//classify//days//"+lookupList[i][1]+"//")           
            shutil.copy(globalPath+"//middle//fixzero//"+lookupList[i][0],globalPath+"//middle//classify//fixzero//"+lookupList[i][1]+"//"+lookupList[i][0])
            shutil.copy(globalPath+"//middle//days//"+lookupList[i][0],globalPath+"//middle//classify//days//"+lookupList[i][1]+"//"+lookupList[i][0])
        else:
            shutil.copy(globalPath+"//middle//fixzero//"+lookupList[i][0],globalPath+"//middle//classify//fixzero//"+lookupList[i][1]+"//"+lookupList[i][0])
            shutil.copy(globalPath+"//middle//days//"+lookupList[i][0],globalPath+"//middle//classify//days//"+lookupList[i][1]+"//"+lookupList[i][0])
            continue
    pass

def monthCalculation(path): # Calculate each month's average and multiply data.
    pathList=os.listdir(globalPath+"//middle//classify//fixzero//"+path)
    # meanList=[]
    # dayList=[]
    # for i in pathList:
    #     if i.endswith(".tif"):
    #         meanList.append(globalPath+"//middle//classify//fixzero//"+path+"//"+i)
    #         dayList.append(globalPath+"//middle//classify//days//"+path+"//"+i)
    #     else:
    #         continue
    # mean = CellStatistics(meanList, "MEAN", "DATA")    
    # day = CellStatistics(dayList,"SUM","DATA")
    arcpy.env.workspace = globalPath+"//middle//classify//fixzero//"+path
    mean = CellStatistics(arcpy.ListRasters("","tif"), "MEAN", "DATA")
    arcpy.env.workspace = globalPath+"//middle//classify//days//"+path
    day = CellStatistics(arcpy.ListRasters("","tif"),"SUM","DATA")
    mean.save(globalPath+"//results//mean//"+str(path)+".tif")
    day.save(globalPath+"//results//days//"+str(path)+".tif")
    pass

def batchWork(file):
    fileName=str(file).rstrip(".txt")+".tif"
    ascToTif(file)
    print(fileName+" is tif.\n")
    defineProjection(fileName)
    print(fileName+" is projected.\n")
    reprojectionResample(fileName)
    print(fileName+" is reprojected.\n")
    clip(fileName)
    print(fileName+" is cliped.\n")
    calc(fileName)
    print(fileName+" is done.\n")
    pass

if __name__ == '__main__':
    print("Initialized.")
    check()
    print("Checked.") 
    pool0=multiprocessing.Pool(multiprocessing.cpu_count())
    pool0.map_async(batchWork,fileList)
    pool0.close()
    pool0.join()
    
    print("Txts are now tifs.")
    classify()
    print("Classified.")
    classifyData=os.listdir(globalPath+"//middle//classify//fixzero//")
    for i in classifyData:
        monthCalculation(i)
        print(i+" is done.")
    print("All done.")
    pass