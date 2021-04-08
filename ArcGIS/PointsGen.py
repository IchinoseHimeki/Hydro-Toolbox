# -*- coding=utf-8 -*-
'''
Please be advised that ArcPy is REQUIRED!
Assist generating points for Extract_Interpolation.py, or it could be separately used while generating some points.
By default, it shares the same dir structure.
'''
import csv
import os
import arcpy
from arcpy.sa import *

path=os.getcwd()+"\\"

startX=126.000 # REQUIRED! Please use 126.000 instead of 126, as 126 will be recognized as int while 126.000 will be float or dounble.
startY=41.000 # REQUIRED! as above.
endX=129.000 # REQUIRED! as above.
endY=43.700 # REQUIRED! as above.

PX=100 # REQUIRED! How many X per Y This should be int, so NO 100.00, leave it be 100.
PY=100 # REQUIRED! How many Y per X As above.
spatial_ref = arcpy.SpatialReference('WGS 1984 UTM Zone 51N')  # REQUIRED! Should be same
in_coor_system = arcpy.SpatialReference('WGS 1984 UTM Zone 51N') # REQUIRED! Should be same



if __name__ == "__main__":
    
    if endX-startX<=0 or endY-startY<=0:
        raise Exception("Inputs can not meet the requirements!")
    else:
        pass

    if not os.path.exists(str(path)+"Base\\") or not os.path.exists(str(path)+"Base\\Base.shp"):
        raise IOError("Mask is Required!")
    else:
        pass
    print("How many points: " +str(PX*PY))
    points=[]

    stepX=(endX-startX)/PX
    stepY=(endY-startY)/PY
    for i in range(PX):
        for j in range(PY):
            pointX=startX+(i+1)*stepX
            pointY=startY+(j+1)*stepY
            points.append([str(pointX),str(pointY)])

    with open(path+"Middle\\Points.csv",'a+b') as f:
        writer=csv.writer(f)
        writer.writerow(["X","Y"])
        for point in points:
            writer.writerow(point)
            
    arcpy.ConvertCoordinateNotation_management(str(path)+"Middle\\Points.csv", str(path)+"Points\\Points.shp", 'X', 'Y', 'DD_2','DD_2', '', spatial_ref, in_coor_system)
    arcpy.ErasePoint_edit(str(path)+"Points\\Points.shp", str(path)+"Base\\Base.shp", "OUTSIDE")
