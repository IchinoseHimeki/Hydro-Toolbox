# coding=utf-8 
'''
File: Raster_Mean_Calculation.py
File Created: 2020-10-05 23:09:32
Author: IchinoseHimeki (darwinlee19980811@hotmail.com)
-----
Last Modified: 2022-01-21 14:22:11
Modified By: IchinoseHimeki (darwinlee19980811@hotmail.com>)
-----
Copyright 2022
Requisite: ArcGIS 10.2+ with ArcPy
Description: Calculate the Mean of the raster.
'''

import arcpy
import csv
import os


outputCsvFile = os.getcwd()+'\\result.csv'
arcpy.env.workspace = os.getcwd()
rasters = arcpy.ListRasters("*")


with open(outputCsvFile,'wb') as f:
    writer=csv.writer(f)
    writer.writerow(["Date","Mean"])

for raster in rasters:
    arcpy.CalculateStatistics_management(raster, "1", "1")    
    meanResult = arcpy.GetRasterProperties_management(raster, "MEAN")
    meanRes = meanResult.getOutput(0)
    
    with open(outputCsvFile,'a+b') as f:
        writer=csv.writer(f)
        writer.writerow([str(raster).rstrip('.asc'),str(meanRes)])


print("finish")
