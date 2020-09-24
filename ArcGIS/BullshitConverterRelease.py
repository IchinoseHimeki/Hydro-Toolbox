# -*- coding=utf-8 -*-
import datetime
import os
import shutil
import zipfile
from multiprocessing import Process

import arcpy
from arcpy import env
from arcpy.sa import *
'''
GitHub Version
IMPORTANT:
CONTACT JILIN UNIVERSITY FIRST FOR ANY COMMERCIAL USE
ANY FORK OR FORK LIKE SOFTWARE FROM THIS SHOULD HAVE THE SAME LIMIT

A better Bullshit Converter, in general.
1. Semi-Auto Structure Detection
2. Multiprocessing Converting, Interpolating, Compressing.
3. Easy Switch for Output Formats.
4. Optional Compressing Outputs and Mid-Files.
5. Easier File Requirements.
'''

# Switches
doRaster = True  # If output clipped raster
doPoints = True  # If output extracted points' values
doASC = True # If output ASCs
doOverWrite = True  # If overwrite existed data, recommended & backup is also recommended
doCompress = True  # Zipped output and middle files into zips to save disk space
spatial_ref = arcpy.SpatialReference('WGS 1984 UTM Zone 52N')  # Should be same
in_coor_system = arcpy.SpatialReference('WGS 1984 UTM Zone 52N')
cell_size = "90"  # Set cell size

path = os.getcwd() + '\\'
x_field = 'LON'
y_field = 'LAT'
input_format = 'DD_2'
output_format = 'DD_2'
id_field = 'LOC'  # Seems to be USELESS, but I prefer it as a placeholder for functions


def reconstruct(kind):  # Reconstruct the database to avoid errors
    global path
    if os.path.exists(path + kind + ".gdb\\"):
        shutil.rmtree(path + kind + ".gdb\\")
        arcpy.CreateFileGDB_management(path, kind + ".gdb")
    else:
        arcpy.CreateFileGDB_management(path, kind + ".gdb")
    print(kind + ": Database has been reconstructed.\n")
    return


def cleanDirs(kind):  # Wipe out and remake dirs to avoid errors
    global path, doASC, doPoints, doRaster
    if os.path.exists(path + kind + "MID\\"):
        shutil.rmtree(path + kind + "MID\\")
        os.mkdir(path + kind + "MID\\")
    else:
        os.mkdir(path + kind + "MID\\")

    if doPoints:
        os.mkdir(path + kind + "MID\\Points\\")
        if os.path.exists(path + kind + "XLS\\"):
            shutil.rmtree(path + kind + "XLS\\")
            os.mkdir(path + kind + "XLS\\")
        else:
            os.mkdir(path + kind + "XLS\\")

    if not doRaster and doASC:
        os.mkdir(path + kind + "MID\\Raster\\")
        if os.path.exists(path + kind + "ASC\\"):
            shutil.rmtree(path + kind + "ASC\\")
            os.mkdir(path + kind + "ASC\\")
        else:
            os.mkdir(path + kind + "ASC\\")
        print(kind + ": Dirs are clear.\n")
        return

    if doRaster and not doASC:
        if os.path.exists(path + kind + "TIF\\"):
            shutil.rmtree(path + kind + "TIF\\")
            os.mkdir(path + kind + "TIF\\")
        else:
            os.mkdir(path + kind + "TIF\\")
        print(kind + ": Dirs are clear.\n")
        return

    if doRaster and doASC:
        if os.path.exists(path + kind + "TIF\\"):
            shutil.rmtree(path + kind + "TIF\\")
            os.mkdir(path + kind + "TIF\\")
        else:
            os.mkdir(path + kind + "TIF\\")
        if os.path.exists(path + kind + "ASC\\"):
            shutil.rmtree(path + kind + "ASC\\")
            os.mkdir(path + kind + "ASC\\")
        else:
            os.mkdir(path + kind + "ASC\\")

    print(kind + ": Dirs are clear.\n")
    return


def compress(Location):  # Compressing dirs into a zipped file.
    global path

    desPath = path + Location + "\\"
    zipName = path + Location + ".zip"

    if os.path.exists(desPath) and not os.path.exists(zipName):
        zip = zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)  # For large data
        for dirpath, dirnames, filenames in os.walk(desPath):
            fpath = dirpath.replace(desPath, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                zip.write(os.path.join(dirpath, filename), fpath + filename)
        zip.close()
        shutil.rmtree(path + Location + "\\")  # Wipe the original data to save space
        print(zipName + " has been compressed.\n")
    return


def compressAll(kind):  # Chossing which dirs to compress
    global doRaster, doPoints, doASC

    if doPoints:
        compress(kind + "XLS")
    if doRaster:
        compress(kind + "TIF")
    if doASC:
        compress(kind + "ASC")
    compress(kind + ".gdb")


def autoClean(kind):
    global doRaster, doPoints, doASC

    if doPoints:
        compress(kind + "XLS")
    if doRaster:
        compress(kind + "TIF")
    if doASC:
        compress(kind + "ASC")

    cleanDirs(kind)
    return


def projection(kind):  # Project points into map
    global x_field, y_field, input_format, output_format, id_field, spatial_ref, in_coor_system

    if doOverWrite:
        reconstruct(kind)

    des = path + kind + ".gdb\\"
    location = path + kind + "\\"
    dirs = os.listdir(location)

    for file in dirs:
        name = location + file
        new_file = file.rstrip('.csv')
        final = des + new_file
        input_table = name
        output_points = final
        arcpy.ConvertCoordinateNotation_management(input_table, output_points, x_field, y_field, input_format,output_format, id_field, spatial_ref, in_coor_system)


def output(kind, zField):  # Processing
    global cell_size, doPoints, doRaster, doASC

    if doOverWrite:
        cleanDirs(kind)

    env.workspace = path + kind + ".gdb"
    env.snapRaster = path + "Area\\Area.tif"
    env.extent = path + "Area\\Area.tif"
    env.parallelProcessingFactor = "0"
    points = path + "Area\\points.shp"
    locations = path + kind + "\\"
    dirs = os.listdir(locations)

    for file in dirs:
        in_point_features = file.rstrip('.csv')

        try:
            out = Kriging(in_point_features, zField, KrigingModelOrdinary(), cell_size)
        except Exception as e:
            out = Idw(in_point_features, zField, cell_size)
            pass
        midRaster = path + kind + "MID\\" + "MID_" + file.rstrip('.csv') + ".tif"
        out.save(midRaster)

        if doPoints:  # Different situations
            outPoint = path + kind + "MID\\Points\\" + file.rstrip(".csv") + ".shp"
            ExtractValuesToPoints(points, midRaster, outPoint)
            outExcel = path + kind + "XLS\\" + file.rstrip(".csv") + ".xls"
            arcpy.TableToExcel_conversion(outPoint, outExcel)
            pass

        if doRaster and not doASC:
            clipped = path + kind + "TIF\\" + file.rstrip(".csv") + ".tif"
            raster = ExtractByMask(midRaster, path + "Area\\Area.tif")
            raster.save(clipped)
            continue

        if doRaster and doASC:
            clipped = path + kind + "TIF\\" + file.rstrip(".csv") + ".tif"
            raster = ExtractByMask(midRaster, path + "Area\\Area.tif")
            raster.save(clipped)
            outASCII = path + kind + "ASC\\" + file.rstrip('.csv') + '.asc'
            arcpy.RasterToASCII_conversion(clipped, outASCII)
            continue

        if not doRaster and doASC:
            clipped = path + kind + "MID\\Raster\\" + file.rstrip(".csv") + ".tif"
            raster = ExtractByMask(midRaster, path + "Area\\Area.tif")
            raster.save(clipped)
            outASCII = path + kind + "ASC\\" + file.rstrip('.csv') + '.asc'
            arcpy.RasterToASCII_conversion(clipped, outASCII)
            continue
    return


if __name__ == "__main__":
    startTime = datetime.datetime.now()
    print("ArcPy Auto-Interpolating Analysis V1.0\n")
    print("Switches:\n")
    print("Do Ouput TIF Rasters:"+str(doRaster))
    print("Do Output ASC Rasters:"+str(doASC))
    print("Do Output Specific Points' Values(Please Check if Specific Points are Given):"+str(doPoints))
    print("Do Overwrite Existing Files to Avoid Conflicts:"+str(doOverWrite))
    print("Do Compress Files after Jobs are Done:"+str(doCompress))
    
    kind = ["Max", "Min"]  # Folders to process
    zField = ["MAX", "MIN"]  # Header for z value which means need to be interpolated

    processList = []
    for i in kind:
        p = Process(target=projection, args=(i,))
        p.start()
        processList.append(p)
    for i in processList:
        i.join()

    processList = []
    num = 0
    for i in kind:
        p = Process(target=output, args=(i, zField[num],))
        p.start()
        num = num + 1
        processList.append(p)
    for i in processList:
        i.join()

    processList = []
    if doCompress:
        for i in kind:
            p = Process(target=compressAll, args=(i,))
            p.start()
            processList.append(p)
        for i in processList:
            i.join()
    # Wipe mid data
    for i in kind:
        shutil.rmtree(path + i + "MID\\")
        
    endTime = datetime.datetime.now()
    elapsedSec = (endTime - startTime).total_seconds() / 3600
    print("Total Used:" + "{:.2f}".format(elapsedSec) + " hours.")