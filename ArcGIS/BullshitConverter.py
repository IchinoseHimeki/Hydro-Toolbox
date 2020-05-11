# -*- coding=utf-8 -*-
'''
WARNING: This Scipt is Written by a Noob, Excute it at your RISKS
ArcGIS IS REQUIRED
Environment:Python 2.7.14 with ArcGIS 10.6
Test Example is included in Test.zip
File Structure
    Project             //root
    ├─ETo              //ETo's Csvs
    ├─ETo.gdb          //ETo's Points Data
    ├─EToASC           //ETo's Output
    ├─EToMID           //ETo's Middle Squared Raster
    │  └─CLIPPED       //ETo's Clipped Raster
    ├─PRE
    ├─PRE.gdb
    ├─PREASC
    └─PREMID
        └─CLIPPED

TODO
1.Add multi-threading support to speed up the processing since it is really SLOW
2.Simplify the code structure
3.Auto detection on file structure
4.Auto Compress the mid-data & output data to save disk space.
5.Print Logs for debug or review.
'''
import arcpy
from arcpy.sa import *
from arcpy import env
import sys
import os
from multiprocessing import Process
import csv
import threading
import time

## Global Environments
x_field = 'LON'
y_field = 'LAT'
input_format = 'DD_2'
output_format = 'DD_2'
id_field = 'LOC'    ## Seems to be USELESS, but I prefer it as a placeholder for functions
spatial_ref = arcpy.SpatialReference('Beijing 1954 GK Zone 21')
in_coor_system = arcpy.SpatialReference('Beijing 1954 GK Zone 21')
cell_size = "1000"


def ETo():
## Convert csvs to points data in ArcGIS database. Database should be CREATED BEFORE
    global x_field,y_field,input_format,output_format,id_field,spatial_ref,in_coor_system

    des = "E:/Project/ETo.gdb/"
    location="E:/Project/ETo/"

    dirs = os.listdir(location)
    for file in dirs:
        name=location + file
        new_file=file.rstrip('.csv')
        final=des+new_file
        input_table = name
        output_points = final
        arcpy.ConvertCoordinateNotation_management(input_table, output_points, x_field, y_field, input_format, output_format, id_field, spatial_ref,in_coor_system)

def PRE():
    global x_field,y_field,input_format,output_format,id_field,spatial_ref,in_coor_system

    des = "E:/Project/PRE.gdb/"
    location="E:/Project/PRE/"
    dirs = os.listdir(location)

    for file in dirs:
        name=location + file
        new_file=file.rstrip('.csv')
        final=des+new_file
        input_table = name
        output_points = final
        arcpy.ConvertCoordinateNotation_management(input_table, output_points, x_field, y_field, input_format, output_format, id_field, spatial_ref,in_coor_system)

def EToASC():
## Interpolation points data into a raster(by Kriging Method), then clip it as the research area, finally output the raster as .asc
    global cell_size
    env.workspace = "E:/Project/ETo.gdb/"
    env.snapRaster="E:/Project/Default.gdb/DEM_Hydro1K_Fin"
    env.extent = "E:/Project/Default.gdb/DEM_Hydro1K_Fin"
    env.parallelProcessingFactor = "100%"

    locations = "E:/Project/ETo/"
    z_field="ETo"

    dirs = os.listdir(locations)
    for file in dirs:
        # flag=False
        # x=0
        in_point_features=file.rstrip('.csv')
        # with open((locations+file),'r')as f:
        #     reader=csv.DictReader(f)
        #     column=[row['ETo'] for row in reader]
        #     if (len(set(column))==1):
        #         flag = False
        #     else:
        #         flag = True

        # if(flag):
        #     out =  Kriging (in_point_features, z_field, KrigingModelOrdinary(),cell_size)
        # else:
        #     out = Idw (in_point_features, z_field, cell_size)
        try:
            out =  Kriging (in_point_features, z_field, KrigingModelOrdinary(),cell_size)
        except Exception as e:
            out = Idw (in_point_features, z_field, cell_size)
            pass
        outname="E:/Project/EToMID/"+"Re_"+file.rstrip('.csv')+".tif"
        out.save(outname)
        exportname="E:/Project/EToMID/CLIPPED/Clipped_"+file.rstrip('.csv')+".tif"
        export=ExtractByMask (outname,"E:/Project/Default.gdb/Location")
        export.save(exportname)
        name=file.rstrip('.csv')
        outASCII="E:/Project/EToASC/"+name+'.asc'
        arcpy.RasterToASCII_conversion(exportname, outASCII)
        
""" def PREASC():
## Voronoi Diagram for calcuating Area PRE. Abandoned by an alternate function. Reserved for usage.
    env.workspace = "E:/Project/PRE.gdb/"
    env.snapRaster="E:/Project/Default.gdb/DEM_Hydro1K_Fin"
    env.extent = "E:/Project/Default.gdb/DEM_Hydro1K_Fin"
    env.parallelProcessingFactor = "100%"

    locations = "E:/Project/PRE/"
    cell_size="E:/Project/Default.gdb/DEM_Hydro1K_Fin"
    z_field="PRE"

    dirs = os.listdir(locations)
    for file in dirs:
        in_point_features=file.rstrip('.csv')
        TOTAL = 0
        TOTALPRE = 0
        out1="E:/Project/PREMID/"+"Re_"+file.rstrip('.csv')+".shp"
        exportname="E:/Project/PREMID/CLIPPED/"+file.rstrip('.csv')+".shp"
        arcpy.CreateThiessenPolygons_analysis (in_point_features, out1, "ALL")
        arcpy.Clip_analysis (out1, "E:/Project/Default.gdb/Location",exportname)
        arcpy.AddField_management (exportname,"FINPRE","DOUBLE")
        arcpy.AddField_management (exportname,"Prop", "DOUBLE")
        arcpy.AddField_management (exportname,"PRE_T", "DOUBLE")
        UC=arcpy.da.UpdateCursor(exportname,["Prop","FINPRE","SHAPE@AREA","PRE","PRE_T"])
        for i in UC:
            TOTAL += i[2]
        UC=arcpy.da.UpdateCursor(exportname,["Prop","FINPRE","SHAPE@AREA","PRE","PRE_T"])
        for j in UC:
            j[0]=j[2]/TOTAL
            UC.updateRow(j)
        UC=arcpy.da.UpdateCursor(exportname,["Prop","FINPRE","SHAPE@AREA","PRE","PRE_T"])
        for m in UC:
            m[1]=m[0]*m[3]
            UC.updateRow(m)
        UC=arcpy.da.UpdateCursor(exportname,["Prop","FINPRE","SHAPE@AREA","PRE","PRE_T"])
        for k in UC:
            TOTALPRE+=k[1]
        UC=arcpy.da.UpdateCursor(exportname,["Prop","FINPRE","SHAPE@AREA","PRE","PRE_T"])
        for l in UC:
            l[4]=TOTALPRE
            UC.updateRow(l)
        rastername = "E:/Project/PREMID/CLIPPED/"+file.rstrip('.csv')+".tif"
        arcpy.FeatureToRaster_conversion (exportname, "PRE_T", rastername, cell_size)
        name=file.rstrip('.csv')
        outASCII="E:/Project/PREASC/"+name+'.asc'
        arcpy.RasterToASCII_conversion(rastername, outASCII)
 """
def PREASC():
## Since we have same data in a dataset, Kriging COULD NOT interpolate the data, IDW method is the alternation.
    global cell_size 

    env.workspace = "E:/Project/PRE.gdb/"
    env.snapRaster="E:/Project/Default.gdb/DEM_Hydro1K_Fin"
    env.extent = "E:/Project/Default.gdb/DEM_Hydro1K_Fin"
    env.parallelProcessingFactor = "100%"

    locations = "E:/Project/PRE/"
    z_field="PRE"

    dirs = os.listdir(locations)
    for file in dirs:
        # flag=False
        # x=0
        in_point_features=file.rstrip('.csv')
        # with open((locations+file),'r')as f:
        #     reader=csv.DictReader(f)
        #     column=[row['PRE'] for row in reader]
        #     if (len(set(column))==1):
        #         flag = False
        #     else:
        #         flag = True

        # if(flag):
        #     out =  Kriging (in_point_features, z_field, KrigingModelOrdinary(),cell_size)
        # else:
        #     out = Idw (in_point_features, z_field, cell_size)
        try:
            out =  Kriging (in_point_features, z_field, KrigingModelOrdinary(),cell_size)
        except Exception as e:
            out = Idw (in_point_features, z_field, cell_size)
            pass
        outname="E:/Project/PREMID/"+"Re_"+file.rstrip('.csv')+".tif"
        out.save(outname)
        exportname="E:/Project/PREMID/CLIPPED/Clipped_"+file.rstrip('.csv')+".tif"
        export=ExtractByMask (outname,"E:/Project/Default.gdb/Location")
        export.save(exportname)
        name=file.rstrip('.csv')
        outASCII="E:/Project/PREASC/"+name+'.asc'
        arcpy.RasterToASCII_conversion(exportname, outASCII)

def Resize():
    locations="E:/Project/EToASC_/"
    dirs=os.listdir(locations)
    global cell_size
        
    for file in dirs:
        in_raster=locations+file
        out_raster="E:/Project/EToASC_MID/"+file.rstrip(".asc")+".tif"
        arcpy.Resample_management (in_raster, out_raster, cell_size)
        outASCII="E:/Project/EToASC/"+file
        arcpy.RasterToASCII_conversion(out_raster, outASCII)
        
if __name__=="__main__":
    #ETo()
    #PRE()
    EToASC()
    #PRE()
    #PREASC()
    #Resize()
