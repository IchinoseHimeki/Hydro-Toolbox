# coding=utf-8
# Calculate the Mean of the raster
# Please be advised that ArcGIS is REQUIRED

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
