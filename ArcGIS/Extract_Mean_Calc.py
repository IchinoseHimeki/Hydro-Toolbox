# -*- coding: utf-8 -*-
'''
File: Extract_Mean_Calc.py
File Created: 2021-08-06 14:06:52
Author: IchinoseHimeki (darwinlee19980811@hotmail.com)
-----
Last Modified: 2022-01-21 14:12:14
Modified By: IchinoseHimeki (darwinlee19980811@hotmail.com>)
-----
Copyright 2022
Requisite: ArcGIS 10.2+ with ArcPy
Description: This Program could convert txt(asc based) into tif, then extract it by mask, calcualting the mean of the clipped raster. Also, it could extract values into given points.
It Requires Data(.txt), Extract_Mask(Area needs to be extract), Extract_Points(Points needs to be extract).
'''

import arcpy
from arcpy.sa import *
import csv
import os
from multiprocessing import Pool
from multiprocessing import cpu_count
import shutil

globalPath=os.getcwd()
outputCsvFile = os.getcwd()+'\\result.csv'
arcpy.env.workspace = os.getcwd()
arcpy.CheckOutExtension("spatial")
files=os.listdir(globalPath+"\\Data\\")

def check():
    if not os.path.exists(globalPath + "\\Data\\") or not os.listdir(globalPath + "\\Data\\"):
        raise IOError("Data files are not given, please check!\n")
    if not os.path.exists(globalPath + "\\ExtractPoints\\") or not os.listdir(globalPath + "\\ExtractPoints\\"):
        raise IOError("Points files are not given, please check!\n")
    if not os.path.exists(globalPath + "\\ExtractMasks\\") or not os.listdir(globalPath + "\\ExtractMasks\\"):
        raise IOError("Masks files are not given, please check!\n")
    
    if os.path.exists(globalPath + "\\Middle\\"):
        shutil.rmtree(globalPath + "\\Middle\\")
        os.mkdir(globalPath + "\\Middle\\")
        os.mkdir(globalPath + "\\Middle\\TEMP")
    else:
        os.mkdir(globalPath + "\\Middle\\")
        os.mkdir(globalPath + "\\Middle\\TEMP")
    if os.path.exists(globalPath + "\\Rasters\\"):
        shutil.rmtree(globalPath + "\\Rasters\\")
        os.mkdir(globalPath + "\\Rasters\\")
    else:
        os.mkdir(globalPath + "\\Rasters\\")
    if os.path.exists(globalPath + "\\Extract_Res\\"):
        shutil.rmtree(globalPath + "\\Extract_Res\\")
        os.mkdir(globalPath + "\\Extract_Res\\")
    else:
        os.mkdir(globalPath + "\\Extract_Res\\")
    pass
    if os.path.exists(globalPath + "\\Extract_Ras\\"):
        shutil.rmtree(globalPath + "\\Extract_Ras\\")
        os.mkdir(globalPath + "\\Extract_Ras\\")
    else:
        os.mkdir(globalPath + "\\Extract_Ras\\")
    pass

def asciiToRaster(file):
    filePath=globalPath+"\\Data\\"+file
    outRaster=globalPath+"\\Rasters\\"+str(file).rstrip(".txt")+".tif"
    arcpy.ASCIIToRaster_conversion(filePath, outRaster, "FLOAT")

def extractByMask_meanCalc(file):
    os.mkdir(globalPath+"\\Middle\\TEMP\\"+str(file).rstrip(".txt"))
    arcpy.env.workspace=globalPath+"\\Middle\\TEMP\\"+str(file).rstrip(".txt")
    raster=globalPath+"\\Rasters\\"+str(file).rstrip(".txt")+".tif"
    rastered = ExtractByMask(raster, globalPath+"\\ExtractMasks\\mask.shp")
    rastered.save(globalPath+"\\Extract_Ras\\"+str(file).rstrip(".txt")+"\\Raster.tif")
    arcpy.CalculateStatistics_management(rastered, "1", "1")    
    meanResult = arcpy.GetRasterProperties_management(rastered, "MEAN")
    meanRes = meanResult[0]
    return [str(file).rstrip(".txt"),meanRes]

def extractToPoints(file):
    ExtractValuesToPoints(globalPath+"\\ExtractPoints\\Points.shp", globalPath+"\\Rasters\\"+str(file).rstrip(".txt")+".tif", globalPath+"\\Middle\\"+str(file).rstrip(".txt")+".shp", "INTERPOLATE")
    arcpy.TableToExcel_conversion(globalPath+"\\Middle\\"+str(file).rstrip(".txt")+".shp", globalPath+"\\Extract_Res\\"+str(file).rstrip(".txt")+".xls")

if __name__ == '__main__':
    doCheck=True
    if doCheck:
        check()
        print("Checked\n")
    meanRes=[]
    pool0=Pool(cpu_count())
    pool0.map_async(asciiToRaster,files)
    pool0.close()
    pool0.join()
    print("ASCii files are now be rasters.\n")
    pool1=Pool(cpu_count())
    meanRes=pool1.map_async(extractByMask_meanCalc,files).get()
    pool1.close()
    pool1.join()
    shutil.rmtree(globalPath+"\\Middle\\TEMP\\")
    print("Rasters has been extracted and the mean has been calcualted.\n")
    pool2=Pool(cpu_count())
    pool2.map_async(extractToPoints,files)
    pool2.close()
    pool2.join()
    print("Value has been extracted into xls.\n")
    with open(outputCsvFile,"a+b") as f:
        write=csv.writer(f)
        write.writerow(["File","Mean"])
        write.writerows(meanRes)
    print("Mean Result has been written.\n")
    doRemove=True
    if doRemove:
        shutil.rmtree(globalPath+"\\Middle\\")
        shutil.rmtree(globalPath+"\\Rasters\\")
        print("Removed.\n")
    print("finish")
