# -*- coding=utf-8 -*-
'''
File: ESA_Calculation.py
File Created: 2021-04-08 14:24:32
Author: IchinoseHimeki (darwinlee19980811@hotmail.com)
-----
Last Modified: 2022-01-21 14:06:09
Modified By: IchinoseHimeki (darwinlee19980811@hotmail.com>)
-----
Copyright 2022
Requisite: ArcGIS 10.2+ with ArcPy, 7zip
Description: Inspired by https://blog.csdn.net/liyanzhong/article/details/52557425
Due to 7-zip and cmd, the path should NEVER have any blanks!
Contains the post processes of ESA's data, especially the GlobalSnow SWE products.
'''

import os
import shutil
from multiprocessing import Pool, Value
from multiprocessing import cpu_count
import csv

import arcpy
from arcpy import env
from arcpy.sa import *

path=os.getcwd()+"\\"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference('WGS 1984 UTM Zone 51N') # REQUIRED! Coordinate
Counts=len(os.listdir(path+"gz\\"))
source="'0 0';'721 0';'721 -721';'-0 -721'" # ATTENTION! warp source data!
target="'-9000000 9000000';'9000000 9000000';'9000000 -9000000';'-9000000 -9000000'" # ATTENTION! warp target data!
targetCoor=arcpy.SpatialReference('WGS 1984 UTM Zone 51N') # REQUIRED! Coordinate, should be same!
# If encountering ERROR 000824 or license issue, uncomment the following code.
# arcpy.CheckOutExtension("spatial")


def check():
    if not os.path.exists(path + "gz\\") or not os.listdir(path + "gz\\"):
        raise IOError("gz/HDF files are not given, please check!\n")

    if not os.path.exists(path + "Base\\") or not os.listdir(path + "Base\\"):
        raise IOError("The interplotion area is not specificed, please check!\n")

    if os.path.exists(path + "Middle\\"):
        shutil.rmtree(path + "Middle\\")
        os.mkdir(path + "Middle\\")
        os.mkdir(path + "Middle\\HDFs\\")
        os.mkdir(path + "Middle\\Rasters\\")
        os.mkdir(path + "Middle\\WarpedRasters")
        os.mkdir(path + "Middle\\ReprojectedRasters\\")
    else:
        os.mkdir(path + "Middle\\")
        os.mkdir(path + "Middle\\HDFs\\")
        os.mkdir(path + "Middle\\Rasters\\")
        os.mkdir(path + "Middle\\WarpedRasters")
        os.mkdir(path + "Middle\\ReprojectedRasters\\")

    if os.path.exists(path + "Results\\"):
        shutil.rmtree(path + "Results\\")
        os.mkdir(path + "Results\\")
    else:
        os.mkdir(path + "Results\\")

    print("All is ready to go!\n")
    pass

def unzip():
    gzs=os.listdir(path+"gz\\")
    for file in gzs:
        string="\"C:\\Program Files\\7-Zip\\7z.exe\" x " + "\'"+str(path)+"gz\\" + str(file)+"\'"+" -o\'"+str(path)+"Middle\\HDFs\\"+"\'"
        os.system("\"C:\\Program Files\\7-Zip\\7z.exe\" x " +str(path)+"gz\\" + str(file)+ " -o"+str(path)+"Middle\\HDFs\\")
    pass

def extractHDFToTif(num):
    HDFfiles=os.listdir(path+"Middle\\HDFs\\")
    file=path+"Middle\\HDFs\\"+str(HDFfiles[num])
    arcpy.ExtractSubDataset_management(file,path+"Middle\\Rasters\\"+str(HDFfiles[num]).rstrip(".HDF")+".tif", 0)
    pass

def warp(num,fileList):
    files=fileList
    raster=path+"Middle\\Rasters\\"+str(files[num])
    warped=path+"Middle\\WarpedRasters\\"+str(files[num])
    arcpy.Warp_management(raster, source, target, warped, "POLYORDER1","BILINEAR")
    pass

def assignProjection(num,fileList):
    files=fileList
    file=path+"Middle\\WarpedRasters\\"+str(files[num])
    arcpy.DefineProjection_management(file,path+"custom.prj") # REQUIRED！ .prj File.
    pass

def reprojection(num,fileList):
    files=fileList
    file=path+"Middle\\WarpedRasters\\"+str(files[num])
    output=path+"Middle\\ReprojectedRasters\\"+str(files[num])
    arcpy.ProjectRaster_management(file,output,targetCoor)
    pass

def meanCalculationWithExtraction(num,fileList):
    os.mkdir(path+"Middle\\TEMP"+str(num)) # A MASSIVE C**K TO THE F**KING ArcGIS！
    env.workspace=path+"Middle\\TEMP"+str(num) # A MASSIVE C**K TO THE F**KING ArcGIS！
    rasters=fileList
    file=path+"Middle\\ReprojectedRasters\\"+str(rasters[num])
    raster = ExtractByMask(file, path+"Base\\Base.shp")
    raster.save(path+"Results\\"+str(str(rasters[num]).replace("GlobSnow_SWE_L3A_","")).replace("_v2.0.hdf.tif","")+".tif")
    arcpy.CalculateStatistics_management(raster, "1", "1")
    meanResult = arcpy.GetRasterProperties_management(raster, "MEAN")
    meanRes = meanResult.getOutput(0)
    shutil.rmtree(path+"Middle\\TEMP"+str(num)) # A MASSIVE C**K TO THE F**KING ArcGIS！
    return [str(str(rasters[num]).replace("GlobSnow_SWE_L3A_","")).replace("_v2.0.hdf.tif",""),str(meanRes)]

def cleanup(flag):
    if flag:
        shutil.rmtree(path+"Middle\\")
    pass

# To Pass multiple args by map, an encapsulation is required.
def WP(num):
    HDFfiles=os.listdir(path+"Middle\\HDFs\\")
    fileList=[]
    for file in HDFfiles:
        fileList.append(file+".tif")
    return warp(num,fileList)
def AP(num):
    HDFfiles=os.listdir(path+"Middle\\HDFs\\")
    fileList=[]
    for file in HDFfiles:
        fileList.append(file+".tif")
    return assignProjection(num,fileList)
def RP(num):
    HDFfiles=os.listdir(path+"Middle\\HDFs\\")
    fileList=[]
    for file in HDFfiles:
        fileList.append(file+".tif")
    return reprojection(num,fileList)
def MP(num):
    HDFfiles=os.listdir(path+"Middle\\HDFs\\")
    fileList=[]
    for file in HDFfiles:
        fileList.append(file+".tif")
    return meanCalculationWithExtraction(num,fileList)

if __name__ == "__main__":
    number=[]
    check()
    unzip()
    print("Extracting HDFs.\n")
    pool0=Pool(cpu_count())
    pool0.map_async(extractHDFToTif,range(Counts))
    pool0.close()
    pool0.join()
    print("Warping rasters. Attention, this could be removed.\n")
    pool1=Pool(cpu_count())
    pool1.map_async(WP,range(Counts))
    pool1.close()
    pool1.join()
    print("Assigning Projection as given.\n")
    pool2=Pool(cpu_count())
    pool2.map_async(AP,range(Counts))
    pool2.close()
    pool2.join()
    print("Reprojecting Rasters.\n")
    pool3=Pool(cpu_count())
    pool3.map_async(RP,range(Counts))
    pool3.close()
    pool3.join()
    print("Calculating Rasters' Mean.\n")
    pool4=Pool(cpu_count())
    number=pool4.map_async(MP,range(Counts)).get() # Getting the mapresult
    pool4.close()
    pool4.join()
    print("Printing Results.\n")
    with open(path+"Result.csv",'a+b') as f:
        writer=csv.writer(f)
        writer.writerow(["File","Mean"])
        writer.writerows(number)
    print("Done! If cleanUp is True, Middle Dir will be removed!")
    cleanup(True)