# -*- coding: utf-8 -*-
"""
@Author: Darwin Lee (darwinlee19980811@hotmail.com) 
@Date: 2021-09-10 11:20:12 
@Last Modified by:   Darwin Lee (darwinlee19980811@hotmail.com) 
@Last Modified time: 2021-09-10 11:20:12 

Fix missing header of specific .asc/.txt file, which could be recongized as TIF.
"""
import os
import shutil
from multiprocessing import Pool,cpu_count

startX="60"
startY="15"
noData="-1"
cellSize="0.25"
globalPath=os.getcwd()
files=os.listdir(globalPath)

def check():
    if os.path.exists(globalPath + "\\Results\\"):
        shutil.rmtree(globalPath + "\\Results\\")
        os.mkdir(globalPath + "\\Results\\")
    else:
        os.mkdir(globalPath + "\\Results\\")
    pass

def constructHeader(list):
    header=[]
    header.append("ncols "+str(len(list[0]))+"\n")
    header.append("nrows "+str(len(list))+"\n")
    header.append("xllcenter "+startX+"\n")
    header.append("yllcenter "+startY+"\n")
    header.append("cellsize "+cellSize+"\n")
    header.append("NODATA_value "+noData+"\n")
    return header

def operation(file):
    if not str(file).endswith(".txt"):
        return
    inputFile=globalPath+"\\"+file
    outputPath=globalPath+"\\Results\\"+file
    headerExists=False
    with open (inputFile,mode="r") as f:
        raw=f.readlines()
        if "ncols " in raw[0]:
            headerExists=True
    if not headerExists:
        # Add Header
        data=[]
        for i in raw:
            data.append(i.split())
        header=constructHeader(data)
        with open (outputPath,"w")as f:
            f.writelines(header)
            f.writelines(raw)
        pass
    else:
        # Copy Raw
        shutil.copyfile(inputFile,outputPath)
        pass
    pass

if __name__ == "__main__":
    check()
    print("Checked!")
    pool=Pool(cpu_count())
    pool.map_async(operation,files)
    pool.close()
    pool.join()