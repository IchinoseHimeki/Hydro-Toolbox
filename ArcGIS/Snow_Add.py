# -*- coding: utf-8 -*-
'''
@Author: Darwin Lee (darwinlee19980811@hotmail.com) 
@Date: 2022-01-18 17:16:00 
@Last Modified by:   Darwin Lee (darwinlee19980811@hotmail.com) 
@Last Modified time: 2022-01-18 17:16:00
Please be advised that ArcGIS is required! 
Merging two areas into one tif. Then Calculating Mean of each Month.
'''

from multiprocessing import cpu_count
import os
import arcpy
from arcpy.sa import *
import datetime
from multiprocessing.pool import *
import shutil

globalPath=os.getcwd()
primary="A"
secondary="T"
arcpy.env.workspace = globalPath+"//clip_"+primary
rasters=arcpy.ListRasters("","tif")

def check(): # Make dirs.
    if not os.path.exists(globalPath+"//middle//"):
        os.mkdir(globalPath+"//middle//")
        os.mkdir(globalPath+"//middle//setNull")
        os.mkdir(globalPath+"//middle//setNull//A")
        os.mkdir(globalPath+"//middle//setNull//T")
        os.mkdir(globalPath+"//middle//multi")
        os.mkdir(globalPath+"//middle//classify")
    else:
        shutil.rmtree(globalPath+"//middle//")
        os.mkdir(globalPath+"//middle//")
        os.mkdir(globalPath+"//middle//setNull")
        os.mkdir(globalPath+"//middle//setNull//A")
        os.mkdir(globalPath+"//middle//setNull//T")
        os.mkdir(globalPath+"//middle//multi")
        os.mkdir(globalPath+"//middle//classify")
    if not os.path.exists(globalPath+"//results//"):
        os.mkdir(globalPath+"//results//")
    else:
        shutil.rmtree(globalPath+"//results//")
        os.mkdir(globalPath+"//results//")

def convertDate(txt): # Convert 2010001.tif into 2010-01
    year=int(txt[0:4])
    date=int(txt[4:7])
    baseTime=datetime.date(year-1,12,31)
    targetTime=baseTime+datetime.timedelta(days=date)
    formatTime=targetTime.strftime("%Y-%m")
    return [txt,formatTime]

def setNullandAdd(raster): # Set all abnormal value like 250 into null, then merge two data into one raster, primary raster has been chosen.
    a_null=SetNull(globalPath+"//clip_A//"+raster,globalPath+"//clip_A//"+raster,"VALUE > 100") # All > 100 (Abnormal) data set to NoData. 
    t_null=SetNull(globalPath+"//clip_T//"+raster,globalPath+"//clip_T//"+raster,"VALUE > 100")
    a_null.save(globalPath+"//middle//setNull//A//"+raster)
    t_null.save(globalPath+"//middle//setNull//T//"+raster)
    if primary=="A":
        multi=Con(IsNull(a_null),t_null,a_null) # Merge data into one. 
    elif primary=="T":
        multi=Con(IsNull(t_null),a_null,t_null) 
    multi.save(globalPath+"//middle//multi//"+raster)
    pass

def monthCalculation(path): # Calculate each month's average data.
    arcpy.env.workspace = globalPath+"//middle//classify//"+path
    mean = CellStatistics(arcpy.ListRasters("","tif"), "MEAN", "DATA")
    mean.save(globalPath+"//results//"+str(path)+".tif")
    pass

if __name__ == '__main__':
    
    check()
    
    pool0=Pool(cpu_count())
    pool0.map_async(setNullandAdd,rasters)
    pool0.close()
    pool0.join()
        
    lookupList=[]
    paths=[]
    
    for i in rasters:
        lookupList.append(convertDate(i))

    for i in range(len(lookupList)):
        if not lookupList[i][1] in paths:
            paths.append(lookupList[i][1])
            os.mkdir(globalPath+"//middle//classify//"+lookupList[i][1]+"//")
            shutil.copy(globalPath+"//middle//multi//"+lookupList[i][0],globalPath+"//middle//classify//"+lookupList[i][1]+"//"+lookupList[i][0])
        else:
            shutil.copy(globalPath+"//middle//multi//"+lookupList[i][0],globalPath+"//middle//classify//"+lookupList[i][1]+"//"+lookupList[i][0])
            continue
    
    classifyData=os.listdir(globalPath+"//middle//classify//")
    
    pool1=Pool(cpu_count())
    pool1.map_async(monthCalculation,classifyData)
    pool1.close()
    pool1.join()