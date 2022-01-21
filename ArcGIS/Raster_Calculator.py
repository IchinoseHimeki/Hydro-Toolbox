'''
File: Raster_Calculator.py
File Created: 2020-10-30 11:03:32
Author: IchinoseHimeki (darwinlee19980811@hotmail.com)
-----
Last Modified: 2022-01-21 14:14:39
Modified By: IchinoseHimeki (darwinlee19980811@hotmail.com>)
-----
Copyright 2022
Requisite: ArcGIS 10.2+ with ArcPy
Description: Weight Calculation is not guaranteed!
Calculate the weight value of each phrase, then do expressions below:
ResultRaster=Raster1*weight1+Raster2*weight2+Raster3*weight3+Raster4*weight4+Raster5*weight5+Raster6*weight6

Expression Constructing seems to be very stupid, hope there will be a better way to improve
'''
import arcpy
import arcpy.sa
from arcpy.sa import *
from arcpy import env

import os
from multiprocessing import Pool
from multiprocessing import cpu_count

# Set environment settings
# Import Path by os.getcwd
path=os.getcwd() 
env.workspace = path
env.snapRaster = path + "\\2.tif"
env.extent = path + "\\2.tif"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference('Xian 1980 GK Zone 20')

# Use ArcGIS Raster API Instead.
rasters = arcpy.ListRasters("*")

# Use arraies instead.
# The expression below is not GUARANTEED!
x=[0.297,0.033,0.308,0.17,0.096,0.096]
k=[0 for i in range(2)]
k[0]=(-0.2)*x[0]
k[1]=(0.01)*k[0]
y=[0 for i in range(6)]

# MultiProcessing to save time.
def Calc(num):
   
   # The expression below is not GUARANTEED!
   y[0]=x[0]+k[0]+(num+1)*k[1]
   y[1]=(x[1]*(1-y[0]))/(1-x[0]) 
   y[2]=(x[2]*(1-y[0]))/(1-x[0])
   y[3]=(x[3]*(1-y[0]))/(1-x[0])
   y[4]=(x[4]*(1-y[0]))/(1-x[0])
   y[5]=(x[5]*(1-y[0]))/(1-x[0])
   ## reduce the array size to save space.
   
   # Seems to be aggressive, but it DO WORK!
   
   expression='(\"'+str(rasters[0])+'\"'+'*'+str(y[0])+')+'+'(\"'+str(rasters[1])+'\"'+'*'+str(y[1])+')+'+'(\"'+str(rasters[2])+'\"'+'*'+str(y[2])+')+'+'(\"'+str(rasters[3])+'\"'+'*'+str(y[3])+')+'+'(\"'+str(rasters[4])+'\"'+'*'+str(y[4])+')+'+'(\"'+str(rasters[5])+'\"'+'*'+str(y[5])+')'
   # Construct the target expressions, which seem to be quite unreadable
   output_raster=path+"\\phrase"+str(num+1)+".tif"
   arcpy.gp.RasterCalculator_sa(expression, output_raster)
   
if __name__ == "__main__":

   pool=Pool(cpu_count())
   pool.map(Calc,range(41))
   pool.close()
   pool.join()
