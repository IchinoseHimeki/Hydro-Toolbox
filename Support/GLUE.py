# -*- coding=utf-8 -*-
'''
File: GLUE.py
File Created: 2021-01-05 14:10:35
Author: IchinoseHimeki (darwinlee19980811@hotmail.com)
-----
Last Modified: 2022-01-21 14:53:18
Modified By: IchinoseHimeki (darwinlee19980811@hotmail.com>)
-----
Copyright 2022
Requisite: Python 3.10+
Description: GLUE is a way used in hydrology for quantifying the uncertainty of model predictions. 
Requirements:
-Model
--Extract.py(which could be found in this repo.)
-Controls
-Real.csv
-GLUE.py
GLUE.py will make Model dir copies according to the Controls dir's configs, then copy the config to the destination. Then, GLUE.py will call cmd commands to execute the model and the Extract.py to Extract results. Finally, GLUE.py will calculate the Likelihood function results, chosse the config which meets the conditions, then out put into the Results.csv, including config names and Likelihood function results, cleaning all instances.
'''

import csv
import os
import shutil
from multiprocessing import Pool
import re

path=os.getcwd()
def buildInstance(): # Copy Instances.
    global path
    print("Building instances...")
    controls=os.listdir(path+"\\Controls\\")
    
    for i in range(len(controls)):
        instance_path=path+"\\Instance"+str(i+1)+"\\"
        if os.path.exists(instance_path):
            shutil.rmtree(instance_path)
        shutil.copytree(path+"\\Model\\",instance_path)
        if os.path.exists(instance_path+"Control.dat"):
            shutil.remove(instance_path+"Control.dat")
        shutil.copyfile(path+"\\Controls\\"+controls[i],instance_path+"Control.dat")
    print("Instance are OK.")
    
def executionModel(instance): # Excuting the Model.
    print("Executing in "+instance+"\n")
    os.system(instance+"Model.exe >> "+instance+"\\log.txt")
    os.system("cd "+instance+" && python "+instance+"Extract.py >> "+instance+"\\log.txt") # Since Extract.py use os.getcwd() method, so a cd command does be required.
    print(instance+"has been executed.\n")

def cleanUp(): # Clean all instances.
    print("Sweeping the trash.")
    dirs=os.listdir(path)
    for dir in dirs:
        if re.match(r"Instance",dir):
            shutil.rmtree(path+"\\"+dir)
    print("Instances are cleared.")
    
    
def readResults(instance,raw): #Read Real results and Model Results into Lists.
    if raw:
        instancePath=os.getcwd()+"\\Real.csv"
    else:
        instancePath=instance+"\\Result\\p12.csv"
    with open(instancePath,'r') as csvfile:
        reader = csv.reader(csvfile)
        head =next(reader)
        data = []
        for line in reader:
            data.append(line)
    return data


def printSummary(lists): # Output the Results which meet the requirements.
    with open (path+"\\Result.csv",'wb') as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow(["Configs","L"])
        for i in lists:
            writer.writerow(i)
    print("Result Summaried.")

if __name__== "__main__":
    pool=Pool(8)
    buildInstance()
    instance_List=os.listdir(path+"\\Controls\\")
    process_List=[]
    for i in range(len(instance_List)):
        instance_path=path+"\\Instance"+str(i+1)+"\\"
        pool.apply_async(executionModel,(instance_path,))
    pool.close()
    pool.join()
    
    print("Calculating Results\n")
    instances=os.listdir(path+"\\Controls\\")
    stanard=readResults("",True)
    Result=[]
    for i in range(len(instances)): # Triple For? Kidding me? This is intolerable.
        instance_path=path+"\\Instance"+str(i+1)+"\\"
        data=readResults(instance_path,False)
        sums=[]
        for j in data:
            for k in stanard:
                if k[0] == j[0] and k[1] != "" and j[1] != "": # Only date matched then proceed, make the formats same.
                    sums.append(abs(float(k[1])-float(j[1]))) # Likelihood function
        if sum(sums)/len(sums)<=0.2:
            Result.append([instances[i],str(sum(sums)/len(sums))]) 
    
    printSummary(Result)        
    cleanUp()