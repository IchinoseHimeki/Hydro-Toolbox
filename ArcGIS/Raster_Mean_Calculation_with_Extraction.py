# coding=utf-8
'''
File: Raster_Mean_Calculation_with_Extraction.py
File Created: 2022-01-21 14:03:32
Author: IchinoseHimeki (darwinlee19980811@hotmail.com)
-----
Last Modified: 2022-01-21 14:17:14
Modified By: IchinoseHimeki (darwinlee19980811@hotmail.com>)
-----
Copyright 2022
Requisite: ArcGIS 10.2+ with ArcPy
Description: Calculate the Mean of the raster, with Extraction from Specific shape.
'''

import arcpy
from arcpy.sa import *
import csv
import os


outputCsvFile = os.getcwd()+'\\result.csv'
arcpy.env.workspace = os.getcwd()
rasters = arcpy.ListRasters("*")


with open(outputCsvFile,'wb') as f:
    writer=csv.writer(f)
    writer.writerow(["Date","Mean"])

for raster in rasters:
    rastered = ExtractByMask(raster, "\\result.shp")
    arcpy.CalculateStatistics_management(rastered, "1", "1")    
    meanResult = arcpy.GetRasterProperties_management(rastered, "MEAN")
    meanRes = meanResult.getOutput(0)
    
    with open(outputCsvFile,'a+b') as f:
        writer=csv.writer(f)
        writer.writerow([str(raster).rstrip('.asc'),str(meanRes)])


print("finish")
