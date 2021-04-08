# -*- coding=utf-8 -*-
'''
Please be advised that ArcPy is REQUIRED!
This script will extract values from a low-resolution raster to the specific points, then use those points to interpolate into a higer resolution raster.
'''
# ATTENTION! The Rasters in Data Dir should be larger than Base.shp, or the -9999 Value will be OCCUR!
import os
import shutil
from multiprocessing import Pool
from multiprocessing import cpu_count

import arcpy
from arcpy import env
from arcpy.sa import *

path=os.getcwd()+"\\"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference('WGS 1984 UTM Zone 51N') # REQUIRED! Coordinate System
cell_size = "50" # REQUIRED! Output Rasters' Resoultion!
z_Field="RASTERVALU"
env.extent = path + "Base//Base.shp"

env.workspace=path+"Data\\"
rasters=arcpy.ListRasters("*")
counts=len(rasters)
doOverrideExistedPoints=True # REQUIRED! Choose True to OVERRIDE existed points by PointsGen.py

def check(): # Requirements' check
    if not os.path.exists(path + "Base\\") or not os.listdir(path + "Base\\"):
        raise IOError("FATAL: The interplotion area is not specificed, please check!\n")
    if os.path.exists(path + "Middle\\"):
        shutil.rmtree(path + "Middle\\")
        os.mkdir(path + "Middle\\")
        os.mkdir(path + "Middle\\Points\\")
        os.mkdir(path + "Middle\\Rasters\\")
    else:
        os.mkdir(path + "Middle\\")
        os.mkdir(path + "Middle\\Points\\")
        os.mkdir(path + "Middle\\Rasters\\")
        
    if not os.path.exists(path+"PointsGen.py"):
        if doOverrideExistedPoints or not os.path.exists(path + "Points\\") or not os.listdir(path + "Points\\"):
            raise IOError("FATAL: PointsGen.py is MISSING! And you do want to OVERRIDE the points or the Points are not GIVEN!")
        print("WARNING: PointsGen.py is MISSING! It could be essential if you would like to generate points.")
        pass
            
    if (not os.path.exists(path + "Points\\") or not os.listdir(path + "Points\\")) and not doOverrideExistedPoints:
        raise IOError("FATAL: Points are not given, please check! Maybe you would like to generate one!\n")
        
    if doOverrideExistedPoints or ((not os.path.exists(path + "Points\\") or not os.listdir(path + "Points\\")) and doOverrideExistedPoints):
        print("Generating Points by PointsGen.py...")
        if os.path.exists(path + "Points\\"):
            shutil.rmtree(path + "Points\\")
            os.mkdir(path + "Points\\")
        else:
            os.mkdir(path + "Points\\")
            
        execfile(path+"PointsGen.py") # Call another py file, it could be found in the same dir
        print("Points Generated.")
    if not os.path.exists(path + "Data\\") or not os.listdir(path + "Data\\"):
        raise IOError("FATAL: Data rasters are missing, please check!\n")

    if os.path.exists(path + "Result\\"):
        shutil.rmtree(path + "Result\\")
        os.mkdir(path + "Result\\")
    else:
        os.mkdir(path + "Result\\")
    
    print("All is ready to go!\n")
    pass    



def extract(num): # Extract values from the original raster to the specific points
    
    ExtractValuesToPoints(path+"Points\\Points.shp", rasters[num], path+"Middle\\Points\\"+str(rasters[num]).rstrip(".tif"), "INTERPOLATE")
    pass

def interpolation(num): # Interpolation
    global rasters
    try:
        out = Kriging(path+"Middle\\Points\\"+str(rasters[num]).rstrip(".tif")+".shp", z_Field, KrigingModelOrdinary(), cell_size)
    except Exception as e:
        out = Idw(path+"Middle\\Points\\"+str(rasters[num]).rstrip(".tif")+".shp", z_Field, cell_size)
    pass
    out.save(path+"Middle\\Rasters\\"+rasters[num])
    clipped = ExtractByMask(out, path + "Base\\Base.shp")
    clipped.save(path+"Result\\"+rasters[num])
        
def cleanup(flag):
    if flag:
        shutil.rmtree(path+"Middle\\")


if __name__ == "__main__":
    check()
    pool=Pool(cpu_count())
    pool.map(extract,range(counts))
    pool.close()
    pool.join()
    pool1=Pool(cpu_count())
    pool1.map(interpolation,range(counts))
    pool1.close()
    pool1.join()
    print("Done. If cleanUp is TRUE, then the Middle Dir will be removed to save space.")
    cleanup(True)