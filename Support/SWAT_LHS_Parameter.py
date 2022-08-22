# -*- coding: utf-8 -*-
'''
File: SWAT_LHS_parameter.py
File Created: 2022-05-01 13:48:33
Author: IchinoseHimeki (darwinlee19980811@hotmail.com)
-----
Last Modified: 2022-07-27 16:53:24
Modified By: IchinoseHimeki (darwinlee19980811@hotmail.com)
-----
Copyright 2022
Requisite: Python 3.10+, pyDOE2, numpy
Description: A programs which calinbrate SWAT 2012 rev. 682 in a far more stupid way than SWAT-CUP by using LHS method. Details are on https://naive514.top/371 (only in Chinese, if want to hear further bullshit, just contact my email on github.)
'''
from multiprocessing import cpu_count
from multiprocessing.pool import Pool
from posixpath import join
import shutil
import pyDOE2
import csv
import os
import datetime
import numpy as np
from math import sqrt
from math import pow

globalPath=os.getcwd()
ratio=0
basinCount=0
hruCount=0
warmup=0
hruList=[]
basinParameters=[]
subbasinParameters=[]
hruParameters=[]
observedFile=[]
extractionType=[]
calibrationOrder=[]
activeCalibration=[]
activeHrulist=[]
observedData=[]
sample=[]
soilType=[]
soilParameters=[]
singleTest=False

class ProcessSWAT(object):
    'SWAT Parameter, including parameter name, value and file.'
    def __init__(self,instanceID,paraList,observedData,bsnList,hruList,bsnParameter,hruParameter,subbsnParameter,warmup,extractList,soilType,soilParameter):
        self.__id=instanceID
        self.__paraList=paraList
        self.__observedData=observedData
        self.__bsnList=bsnList
        self.__hruList=hruList
        self.__bsnParameter=bsnParameter
        self.__hruParameter=hruParameter
        self.__subbsnParameter=subbsnParameter
        self.__warmup=warmup
        self.__extractList=extractList
        self.__soilType=soilType
        self.__soilParameter=soilParameter
        self.__workingDir=globalPath+"//Instance//ID"+str(self.__id)
        self.__simulatedData=[]
        self.r2=0.0
        self.nse=1.0
        self.__hruH=0
        self.__hruS=0
        self.__hruG=0
        self.__subS=0
        self.__subG=0
        
        for i in self.__hruParameter:
            if i[5]=="h":
                self.__hruH+=1
            elif i[5]=="s":
                self.__hruS+=1
            elif i[5]=="g":
                self.__hruG+=1
        for i in self.__subbsnParameter:
            if i[5]=="s":
                self.__subS+=1
            elif i[5]=="g":
                self.__subG+=1
        shutil.copytree(globalPath+"//RawModel//",globalPath+"//Instance//ID"+str(self.__id))
        shutil.copyfile(globalPath+"//Exes//debug.exe",globalPath+"//Instance//ID"+str(self.__id)+"//debug_"+str(self.__id)+".exe")

    def __modifyParameters(self):
        'Modify Parameters According to its Location'
        bsnFile=[]
        hruFile=[]
        hruFileHeader=[]
        subbasinFile=[]
        subbasinHeader=[]
        tmp_soilList=[]
        for i in self.__soilParameter:
            tmp_soilList.append(i[0])
        with open (self.__workingDir+"//basins.bsn",'r') as f:
            bsnFile=f.readlines()
        for i in range(len(bsnFile)):
            for j in range(len(self.__bsnParameter)):
                if self.__bsnParameter[j][1] in bsnFile[i]:
                    if self.__bsnParameter[j][4]=="v":
                        tmp_string="{:.8g}".format(self.__paraList[0][j])
                    elif self.__bsnParameter[j][4]=="r":
                        tmp_rawValue=float(bsnFile[i].split("|")[0])
                        tmp_string="{:.8g}".format((1.0+self.__paraList[0][j])*tmp_rawValue) # TODO
                    bsnFile[i]=tmp_string.rjust(16," ")+bsnFile[i][16:]
        with open (self.__workingDir+"//basins.bsn",'w',newline="") as f: # Replacing bsn parameters
            f.writelines(bsnFile)
        for i in range(len(self.__bsnList)): # Constructing hru to be replacced.
            for j in range(self.__hruList[i]):
                hruFileHeader.append(str(int(self.__bsnList[i])).rjust(5,"0")+str(j+1).rjust(4,"0"))
        for i in range(len(self.__bsnList)):
                subbasinHeader.append(str(int(self.__bsnList[i])).rjust(5,"0")+"0000") # Subbsn parameters stored in 000010000.rte and so on

        for i in range(len(hruFileHeader)):
            for j in range(len(self.__soilParameter)):
                with open(self.__workingDir+"//"+hruFileHeader[i]+".sol", 'r') as f:
                    soilFile=f.readlines()
                    tmp_string=""
                    tmp_soilName=str(soilFile[1].split(":")[1]).strip()
                    tmp_soilIndex=self.__soilType.index(tmp_soilName)
                    for k in range(len(soilFile)):
                        if self.__soilParameter[j][0] in soilFile[k]:
                            tmp_rawValue=soilFile[k][29:].strip().split()
                            tmp_paraIndex=tmp_soilList.index(str(soilFile[k].split(":")[0]).strip().split("[")[0].strip())
                            if self.__soilParameter[j][3]=="v":
                                for l in range(len(tmp_rawValue)):
                                    tmp_join="{:.8g}".format(self.__paraList[3][tmp_soilIndex][tmp_paraIndex]).rjust(12,)
                                    tmp_string+=tmp_join
                            elif self.__soilParameter[j][3]=="r":
                                for l in range(len(tmp_rawValue)):
                                    tmp_join="{:.8g}".format((1.0+self.__paraList[3][tmp_soilIndex][tmp_paraIndex])*float(tmp_rawValue[l])).rjust(12,)
                                    tmp_string+=tmp_join
                            soilFile[k]=soilFile[k][:27]+tmp_string+"\n"
                    with open(self.__workingDir+"//"+hruFileHeader[i]+".sol", 'w') as f:
                        f.writelines(soilFile)
                        
        for i in range(len(hruFileHeader)): # Replacing hru parameters TODO: FOR SOL need another one to modify.
            tmp_scaleHRU=0
            tmp_scaleSub=0
            tmp_scaleGbl=0
            for j in range(len(self.__hruParameter)):
                with open(self.__workingDir+"//"+hruFileHeader[i]+"."+self.__hruParameter[j][0], 'r') as f:
                    hruFile=f.readlines()
                for k in range(len(hruFile)):
                    if len(hruFile[k].split())<3:
                        continue
                    if self.__hruParameter[j][1] == hruFile[k].split()[2].rstrip(":") :
                        if self.__hruParameter[j][5]=="h":
                            if self.__hruParameter[j][4]=="v":
                                tmp_string="{:.8g}".format(self.__paraList[1][0][i*self.__hruH+tmp_scaleHRU])
                            elif self.__hruParameter[j][4]=="r":
                                tmp_rawValue=float(hruFile[k].split("|")[0])
                                tmp_string="{:.8g}".format((1.0+self.__paraList[1][0][i*self.__hruH+tmp_scaleHRU])*tmp_rawValue)
                            tmp_scaleHRU+=1
                            if tmp_scaleHRU==self.__hruH:
                                tmp_scaleHRU=0
                        elif self.__hruParameter[j][5]=="s":
                            if self.__hruParameter[j][4]=="v":
                                tmp_string="{:.8g}".format(self.__paraList[1][1][self.__bsnList.index(int(hruFileHeader[i][:5]))*self.__hruS+tmp_scaleSub])
                            elif self.__hruParameter[j][4]=="r":
                                tmp_rawValue=float(hruFile[k].split("|")[0])
                                tmp_string="{:.8g}".format((1.0+self.__paraList[1][1][self.__bsnList.index(int(hruFileHeader[i][:5]))*self.__hruS+tmp_scaleSub])*tmp_rawValue)
                            tmp_scaleSub+=1
                            if tmp_scaleSub==self.__hruS:
                                tmp_scaleSub=0
                        elif self.__hruParameter[j][5]=="g":
                            if self.__hruParameter[j][4]=="v":
                                tmp_string="{:.8g}".format(self.__paraList[1][2][tmp_scaleGbl])
                            elif self.__hruParameter[j][4]=="r":
                                tmp_rawValue=float(hruFile[k].split("|")[0])
                                tmp_string="{:.8g}".format((1.0+self.__paraList[1][2][tmp_scaleGbl])*tmp_rawValue)
                            tmp_scaleGbl+=1
                            if tmp_scaleGbl==self.__hruG:
                                tmp_scaleGbl=0
                        hruFile[k]=tmp_string.rjust(16," ")+hruFile[k][16:]
                with open(self.__workingDir+"//"+hruFileHeader[i]+"."+self.__hruParameter[j][0], 'w',newline="") as f:
                    f.writelines(hruFile)

        for i in range(len(subbasinHeader)):
            tmp_scaleSub=0
            tmp_scaleGbl=0
            for j in range(len(self.__subbsnParameter)):
                with open(self.__workingDir+"//"+subbasinHeader[i]+"."+self.__subbsnParameter[j][0], 'r') as f:
                    subbasinFile=f.readlines()
                for k in range(len(subbasinFile)):
                    if len(subbasinFile[k].split())<3:
                        continue
                    if self.__subbsnParameter[j][1] == subbasinFile[k].split()[2].rstrip(":"):
                        if self.__subbsnParameter[j][5]=="s":
                            if self.__subbsnParameter[j][4]=="v":
                                tmp_string="{:.8g}".format(self.__paraList[2][0][i*self.__subS+tmp_scaleSub])
                            elif self.__subbsnParameter[j][4]=="r":
                                tmp_rawValue=float(hruFile[k].split("|")[0])
                                tmp_string="{:.8g}".format((1.0+self.__paraList[2][0][i*self.__subS+tmp_scaleSub])*tmp_rawValue)
                            tmp_scaleSub+=1
                            if tmp_scaleSub==self.__subS:
                                tmp_scaleSub=0
                        elif self.__subbsnParameter[j][5]=="g":
                            if self.__subbsnParameter[j][4]=="v":
                                tmp_string="{:.8g}".format(self.__paraList[2][1][tmp_scaleGbl])
                            elif self.__subbsnParameter[j][4]=="r":
                                tmp_rawValue=float(hruFile[k].split("|")[0])
                                tmp_string="{:.8g}".format((1.0+self.__paraList[2][1][tmp_scaleGbl])*tmp_rawValue)
                            tmp_scaleGbl+=1
                            if tmp_scaleGbl==self.__subG:
                                tmp_scaleGbl=0
                        subbasinFile[k]=tmp_string.rjust(16," ")+subbasinFile[k][16:]
                with open(self.__workingDir+"//"+subbasinHeader[i]+"."+self.__subbsnParameter[j][0], 'w',newline="") as f:
                    f.writelines(subbasinFile)
                pass
            pass
        pass
    pass
    def __executeModel(self):
        'Execute Model and get Outputs'
        if "nt" in os.name:
            cmd="powershell cd "+self.__workingDir+" ; "+self.__workingDir+"//debug_"+str(self.__id)+".exe > "+self.__workingDir+"//null"
        elif "posix" in os.name:
        # TODO: LINUX
            cmd=""
        os.system(cmd)
        splitedList=[]
        with open (self.__workingDir+"//output.rch","r") as f: # ONLY rch has been extracted. TODO: other samples & daily
            rawResults=f.readlines()
            rawResults=rawResults[9:]
        for i in rawResults:
            splitedList.append(i[:64].strip().split())
        for i in splitedList:
            if i[1]==str(self.__extractList[2]) and len(i[3])<=2:
                self.__simulatedData.append(float(i[6]))
        pass
    pass                
    def __calcStatus(self):
        'Calc R2 and NSE.'
        sumObserve=0.0
        sumSim=0.0
        sum1=0.0
        sum2=0.0
        sum3=0.0
        sum4=0.0
        sum5=0.0
        averageObserve=0.0
        averageSim=0.0
        simulatedData=self.__simulatedData[int(self.__warmup):]
        if not len(simulatedData)==len(self.__observedData):
            raise ValueError("The length of sim and observe are not match!")
        else:
            for i in self.__observedData:
                sumObserve+=i
            averageObserve=sumObserve/len(self.__observedData)
            for i in simulatedData:
                sumSim+=i
            averageSim=sumSim/len(simulatedData)
            for i in range(len(simulatedData)):
                sum1+=(float(self.__observedData[i])-float(averageObserve))*(float(simulatedData[i])-float(averageSim))
                sum2+=pow(float(self.__observedData[i])-float(averageObserve),2.0)
                sum3+=pow((float(simulatedData[i])-float(averageSim)),2.0)
                sum4+=pow(float(self.__observedData[i])-float(simulatedData[i]),2.0)
                sum5+=pow(float(self.__observedData[i])-float(averageObserve),2.0)
        self.r2=pow(sum1/(sqrt(sum2)*sqrt(sum3)),2.0)
        self.nse=1.0-(sum4/sum5)
        
    def run(self):
        'Perform the whole process & Return results.'
        output=[]
        self.__modifyParameters()
        self.__executeModel()
        self.__calcStatus()
        shutil.rmtree(self.__workingDir) # comment this to debug
        for i in self.__paraList:
            for j in i:
                if isinstance(j,list):
                    for k in j:
                        output.append(k)
                else:
                    output.append(j)
        output.append(self.r2)
        output.append(self.nse)
        return(output)

def check(): # The longest check() ever. Initializing the config file.
    do_testRun=False
    global ratio,basinCount,hruList,hruCount,basinParameters,subbasinParameters,hruParameters,observedFile,extractionType,calibrationOrder,activeCalibration,activeHrulist,warmup,observedData,soilType
    tmp_basinParameters=[]
    tmp_subbasinParameters=[]
    tmp_hruParameters=[]
    tmp_soilParameters=[]
    tmp_calibrationOrder=[]
    tmp_activeCalibration=[]
    checkOrder=[]
    uniqueOrder=[]
    soilExists=False
    
    if not os.path.exists(globalPath+"//RawModel") or not os.listdir(globalPath+"//RawModel"):
        raise(IOError("SWAT Model simulating data not exists!"))
    if not os.path.exists(globalPath+"//Exes//debug.exe") and not os.path.exists(globalPath+"//Exes//rel.exe"):
        raise(IOError("SWAT Model exectuables are not found!"))
    if not os.path.exists(globalPath+"//Instance//"):
        os.mkdir(globalPath+"//Instance")
    else:
        shutil.rmtree(globalPath+"//Instance")
        os.mkdir(globalPath+"//Instance")
    if not os.path.exists(globalPath+"//Parameters.txt"):
        raise(IOError("Model parameters file not found!"))
    with open(globalPath+"//Parameters.txt","r") as f: # Reading config file, there should be a better way to achieve this TODO: daily data
        parameters=f.readlines()
        for i in range(len(parameters)):
            if "--RATIO OF SAMPLE AGAINST PARAMETERS--" in parameters[i]:
                ratio=int(parameters[i+1].rstrip(" ").lstrip(" "))
                if ratio <= 0:
                    raise(Exception("Ratio shall never be negative or zero!"))
            if "--BSN--" in parameters[i]:
                basinCount=int(parameters[i+1].rstrip(" ").lstrip(" "))
                if basinCount <= 0:
                    raise(Exception("Basin numbers shall never be negative or zero!"))  
            if "--HRU LIST--" in parameters[i]:
                tmp_hruList=parameters[i+1].rstrip(" ").lstrip(" ").rstrip("\n").split(" ")
                for j in tmp_hruList:
                    hruList.append(int(j))
                    hruCount+=int(j)
                if len(hruList) != basinCount:
                    raise(Exception("HRU count is not matched with Basins!"))
            if "--CALIBRATE STRUCTURE WITH ORDER--" in parameters[i]:
                for j in range(i+1,len(parameters)):
                    if parameters[j].lstrip(" ").startswith("-") or parameters[j].lstrip(" ").startswith("="):
                        break
                    else:
                        tmp_calibrationOrder.append(parameters[j].rstrip(" ").lstrip(" ").split())
                if len(tmp_calibrationOrder[0]) == 0 or len(tmp_calibrationOrder) == 0:
                    raise(Exception("The calibration order should be speified!"))
                for j in tmp_calibrationOrder:
                    tmp_list=[]
                    for k in j:
                        tmp_list.append(int(k))
                    calibrationOrder.append(tmp_list)
                for j in calibrationOrder:
                    for k in j:
                        checkOrder.append(k)
                uniqueOrder=set(checkOrder)
                if len(uniqueOrder) != basinCount:
                    raise(Exception("Not all subbasin are used or some subbasin are missing!\n"))
                for j in uniqueOrder:
                    if not j in range(1,basinCount+1):
                        raise(Exception("Some subbasins are not in defined subbasin sets."))
            if "--ACTIVE CALIBRATION ORDER--" in parameters[i]:
                tmp_activeCalibration=parameters[i+1].rstrip(" ").lstrip(" ").rstrip("\n").split(" ")
                for j in tmp_activeCalibration:
                    activeCalibration.append(int(j))
                for j in activeCalibration:
                    if j not in range(1,len(calibrationOrder)+1):
                        raise(Exception("Invaild calibration Order!"))    
            if "--BSN PARAMETERS--" in parameters[i]:
                for j in range(i+1,len(parameters)):
                    if parameters[j].lstrip(" ").startswith("-") or parameters[j].lstrip(" ").startswith("="):
                        break
                    else:
                        tmp_basinParameters.append(parameters[j].strip().split("|"))
                if len(tmp_basinParameters) == 0:
                    continue
                for j in range(len(tmp_basinParameters)):
                    if str(tmp_basinParameters[j][4]).lower() != "r" and str(tmp_basinParameters[j][4]).lower() != "v":
                        raise(Exception("Unsupport changing type! Only v__ and r__ are currently Support!"))
                    basinParameters.append([tmp_basinParameters[j][1],tmp_basinParameters[j][0],float(tmp_basinParameters[j][2]),float(tmp_basinParameters[j][3]),str(tmp_basinParameters[j][4])])
            if "--SUB PARAMETERS--" in parameters[i]:
                for j in range(i+1,len(parameters)):
                    if parameters[j].lstrip(" ").startswith("-") or parameters[j].lstrip(" ").startswith("="):
                        break
                    else:
                        tmp_subbasinParameters.append(parameters[j].strip().split("|"))
                if len(tmp_subbasinParameters[0]) == 0:
                    continue
                for j in range(len(tmp_subbasinParameters)):
                    if str(tmp_subbasinParameters[j][4]).lower() != "r" and str(tmp_subbasinParameters[j][4]).lower() != "v":
                        raise(Exception("Unsupport changing type! Only v__ and r__ are currently Support!"))
                    if not str(tmp_subbasinParameters[j][5]).lower() in ["g","s"]:
                        raise(Exception("Unsupport scale! Only g(global) and s(subbasin) are supported in sub basin parameter!"))
                    subbasinParameters.append([tmp_subbasinParameters[j][1],tmp_subbasinParameters[j][0],float(tmp_subbasinParameters[j][2]),float(tmp_subbasinParameters[j][3]),str(tmp_subbasinParameters[j][4]),str(tmp_subbasinParameters[j][5])])
            if "--HRU PARAMETERS--" in parameters[i]:
                for j in range(i+1,len(parameters)):
                    if parameters[j].lstrip(" ").startswith("-") or parameters[j].lstrip(" ").startswith("="):
                        break
                    else:
                        tmp_hruParameters.append(parameters[j].strip().split("|"))
                if len(tmp_hruParameters) == 0:
                    continue
                for j in range(len(tmp_hruParameters)):
                    if str(tmp_hruParameters[j][4]).lower() != 'r' and str(tmp_hruParameters[j][4]).lower() != "v":
                        raise(Exception("Unsupport changing type! Only v__ and r__ are currently Support!"))
                    if not str(tmp_hruParameters[j][5]).lower() in ["g","s","h"]:
                        raise(Exception("Unsupport scale! Only g(global),s(subbasin),and h(hru) are supported in HRU parameter!"))
                    hruParameters.append([tmp_hruParameters[j][1],tmp_hruParameters[j][0],float(tmp_hruParameters[j][2]),float(tmp_hruParameters[j][3]),str(tmp_hruParameters[j][4]),str(tmp_hruParameters[j][5])])
            if "--SOIL PARAMETERS--" in parameters[i]:
                for j in range(i+1,len(parameters)):
                    if parameters[j].lstrip(" ").startswith("-") or parameters[j].lstrip(" ").startswith("="):
                        break
                    else:
                        tmp_soilParameters.append(parameters[j].strip().split("|"))
                if len(tmp_soilParameters[0]) == 0:
                    continue
                soilExists=True
                for j in range(len(tmp_soilParameters)):
                    if str(tmp_soilParameters[j][4]).lower() != "r" and str(tmp_soilParameters[j][4]).lower() != "v":
                        raise(Exception("Unsupport changing type! Only v__ and r__ are currently Support!"))
                    soilParameters.append([tmp_soilParameters[j][0],float(tmp_soilParameters[j][2]),float(tmp_soilParameters[j][3]),str(tmp_soilParameters[j][4])])
            if "--OBSERVED FILE--" in parameters[i]:
                for j in range(i+1,len(parameters)):
                    if parameters[j].lstrip(" ").startswith("-") or parameters[j].lstrip(" ").startswith("="):
                        break
                    else:
                        observedFile.append(parameters[j].strip().split("|"))
                if len(observedFile[0]) == 0 or len(observedFile) == 0:
                    raise(Exception("Observed data is not specified!"))
                for j in observedFile:
                    if not os.path.exists(globalPath+"//"+str(j[1])):
                        raise(IOError("Observed file "+j[1]+" is missing!"))
            if "--WARMUP MONTH--" in parameters[i]:
                warmup=int(parameters[i+1].strip(" "))
                if warmup < 0:
                    raise(Exception("Warmup months shall never be negative!"))            
            if "--SIMULATION DATA TO EXTRACT WITH ID--" in parameters[i]:
                for j in range(i+1,len(parameters)):
                    if parameters[j].lstrip(" ").startswith("-") or parameters[j].lstrip(" ").startswith("="):
                        break
                    else:
                        extractionType.append(parameters[j].strip(" ").split("|"))
                if len(extractionType[0]) == 0 or len(observedFile) == 0:
                    raise(Exception("Extraction data is not specified!"))
                if len(extractionType) != len(observedFile):
                    raise(Exception("Observed data and extraction data are not matched!"))
            if "--SOIL CSV FILE--" in parameters[i]:
                with open(globalPath+"//"+str(parameters[i+1]).strip(),'r') as f:
                    csvReader=csv.reader(f)
                    for k in csvReader:
                        soilType.append(k[0])
                soilType=soilType[1:]
    if soilExists and not soilType:
        raise(Exception("Soil types are not specified!"))
    if len(activeCalibration) != len(extractionType):
        raise(Exception("Calibration and Extraction are not mathced!"))
    activeHrulist=[]
    for i in range(len(activeCalibration)):
        tmp_activeHrulist=[]
        for j in range(len(calibrationOrder[activeCalibration[i]-1])):
            tmp_activeHrulist.append(hruList[calibrationOrder[activeCalibration[i]-1][j]-1])
        activeHrulist.append(tmp_activeHrulist)    
    print("Parameters are gathered. Total %d subbasins, %d HRUs, and %d observed stations to calibrate.\n" %(basinCount,hruCount,len(observedFile)))
    print("The Calibration will have %d steps.\n" %(len(calibrationOrder)))
    for i in calibrationOrder:
        print(i)
    print("And %d steps will be calibrated.\n" %(len(activeCalibration)))
    for i in activeCalibration:
        print(i)
    print("Reading observed data.\n")
    for i in observedFile:
        tmp_observedData=[]
        with open(globalPath+"//"+i[1],'r')as f:
            rawData=f.readlines()
            for j in rawData:
                tmp_observedData.append(float(j.strip().split()[1]))
        observedData.append(tmp_observedData)
    print("Observed data has been scanned.\n")
    if do_testRun: # Setting up a test run to verify original model
        print("Setting up a test run to verify SWAT Model.\n Remove fin.fin FIRST!")
        startTime = datetime.datetime.now()
        if os.path.exists(globalPath+"//TestRun//"):
            shutil.rmtree(globalPath+"//TestRun//")
        shutil.copytree(globalPath+"//RawModel//",globalPath+"//TestRun//")
        shutil.copyfile(globalPath+"//Exes//debug.exe",globalPath+"//TestRun//debug.exe")
        if "nt" in os.name:
            cmd="powershell cd "+globalPath+"//TestRun// ; "+globalPath+"//TestRun//debug.exe > null"
        elif "posix" in os.name:
            cmd=""
        # TODO: LINUX 
        os.system(cmd)
        if not os.path.exists(globalPath+"//TestRun//fin.fin"):
            raise(Exception("SWAT Model has failed, check the RawModel."))
        executeResult=False
        with open (globalPath+"//TestRun//fin.fin",'r') as f:
            text=f.readlines()
            for i in text:
                if "Execution successful" in i:
                    executeResult=True
                    
        if not executeResult:
            raise(Exception("SWAT Model did not make it, check the RawModel."))
        shutil.rmtree(globalPath+"//TestRun//")
        endTime = datetime.datetime.now()
        elapsedMin = (endTime - startTime).total_seconds() / 60
        print("The RawModel is okay to go. Single simulation ETA time is: "+"{:.2f}".format(elapsedMin)+" m.\n")
    pass

def sampleGeneration(): # Generating Samples
    global sample
    bsnBound=[]
    hruBound=[]
    subBound=[]
    soilBound=[]
    bsnSample=[]
    soilSample=[]
    activeSubbasin=[]
    activeHRU=0
    scaleHRU=0
    scaleSub=0
    scaleGbl=0
    tmp_list=[]
    HRUSampleH=[]
    HRUSampleS=[]
    HRUSampleG=[]
    subSampleS=[]
    subSampleG=[]
    for i in range(len(activeCalibration)):
        tmp_list.append(calibrationOrder[activeCalibration[0]-1]) # TODO: Only the first Line of activeCalibration is considered!
    for i in range(len(tmp_list)):
        tmp_subbasin=0
        for j in range(len(tmp_list[i])):
            activeHRU+=int(hruList[tmp_list[i][j]-1])
            tmp_subbasin+=int(hruList[tmp_list[i][j]-1])
        activeSubbasin.append(tmp_subbasin)
        
    for i in basinParameters:
        bsnBound.append([abs(i[3]-i[2]),i[2]])
    listHRU=[]
    listSub=[]
    listGbl=[]
    for i in hruParameters:
        if i[5] == "h":
            listHRU.append([abs(i[3]-i[2]),i[2]])
        elif i[5] == "s":
            listSub.append([abs(i[3]-i[2]),i[2]])
        elif i[5] == "g":
            listGbl.append([abs(i[3]-i[2]),i[2]])
    hruBound.append([listHRU,listSub,listGbl])
    tmp_listSub=[]
    tmp_listGbl=[]
    for i in subbasinParameters:
        if i[5] == "s":
            tmp_listSub.append([abs(i[3]-i[2]),i[2]])
        elif i[5] == "g":
            tmp_listGbl.append([abs(i[3]-i[2]),i[2]])
    subBound.append([tmp_listSub,tmp_listGbl])
    for i in range(len(soilType)):
        tmp_soilBound=[]
        for i in soilParameters:
            tmp_soilBound.append([abs(i[2]-i[1]),i[1]])
        soilBound.append(tmp_soilBound)        
    bsnLHS=pyDOE2.lhs(len(basinParameters),int(ratio)*activeHRU).tolist()
    soilLHS=pyDOE2.lhs(len(soilParameters)*len(soilType),int(ratio)*activeHRU).reshape((int(ratio)*activeHRU,len(soilType),len(soilParameters))).tolist()
    for i in hruParameters:
        if i[5] == "h":
            scaleHRU+=1
        elif i[5] == "s":
            scaleSub+=1
        elif i[5] == "g":
            scaleGbl+=1

    hruLHSH=pyDOE2.lhs(scaleHRU*activeHRU,int(ratio)*activeHRU).tolist()
    hruLHSS=pyDOE2.lhs(scaleSub*len(tmp_list[0]),int(ratio)*activeHRU).tolist()
    hruLHSG=pyDOE2.lhs(scaleGbl,int(ratio)*activeHRU).tolist()
    for i in range(len(hruLHSH)):
        tmp_HRU=[]
        for j in range(len(hruLHSH[i])):
            tmp_HRU.append(hruLHSH[i][j]*hruBound[0][0][j%scaleHRU][0]+hruBound[0][0][j%scaleHRU][1])
        HRUSampleH.append(tmp_HRU)
    for i in range(len(hruLHSS)):
        tmp_HRU=[]
        for j in range(len(hruLHSS[i])):
            tmp_HRU.append(hruLHSS[i][j]*hruBound[0][1][j%scaleSub][0]+hruBound[0][1][j%scaleSub][1])
        HRUSampleS.append(tmp_HRU)
    for i in range(len(hruLHSG)):
        tmp_HRU=[]
        for j in range(len(hruLHSG[i])):
            tmp_HRU.append(hruLHSG[i][j]*hruBound[0][2][j%scaleGbl][0]+hruBound[0][2][j%scaleGbl][1])
        HRUSampleG.append(tmp_HRU)

    scaleSub=0
    scaleGbl=0
    for i in subbasinParameters:
        if i[5] == "s":
            scaleSub+=1
        elif i[5] == "g":
            scaleGbl+=1
    subLHSS=pyDOE2.lhs(scaleSub*len(tmp_list[0]),int(ratio)*activeHRU).tolist()
    subLHSG=pyDOE2.lhs(scaleGbl,int(ratio)*activeHRU).tolist() 
    for i in range(len(subLHSS)):
        tmp_sub=[]
        for j in range(len(subLHSS[i])):
            tmp_sub.append(subLHSS[i][j]*subBound[0][0][j%scaleSub][0]+subBound[0][0][j%scaleSub][1])
        subSampleS.append(tmp_sub)
    for i in range(len(subLHSG)):
        tmp_sub=[]
        for j in range(len(subLHSG[i])):
            tmp_sub.append(subLHSG[i][j]*subBound[0][1][j%scaleGbl][0]+subBound[0][1][j%scaleGbl][1])
        subSampleG.append(tmp_sub)

    for i in range(len(bsnLHS)):
        tempBsn=[]
        for j in range(len(bsnLHS[i])):
            tempBsn.append(bsnLHS[i][j]*bsnBound[j][0]+bsnBound[j][1])
        bsnSample.append(tempBsn)
    for i in range(len(soilLHS)):
        tempSoil=[]
        for j in range(len(soilLHS[i])):
            tempSoilj=[]
            for k in range(len(soilLHS[i][j])):
                tempSoilj.append(soilLHS[i][j][k]*soilBound[j][k][0]+soilBound[j][k][1])
            tempSoil.append(tempSoilj)
        soilSample.append(tempSoil)
    for i in range(ratio*activeHRU):
        sample.append([bsnSample[i],[HRUSampleH[i],HRUSampleS[i],HRUSampleG[i]],[subSampleS[i],subSampleG[i]],soilSample[i]])
    print("There are currently %d HRUs, %d Subbasins and %d Soil Types pending to calibrate.\n Generated %d Samples, with %d parameters are changed per Sample: %d (global) %d (subbasin) Subbasin Parameters, %d (global) %d (Subbasin) %d (HRU) HRU Parameters, %d Basin Parameters and %d Soil Parameters.\n" %(activeHRU,len(activeHrulist[0]),len(soilType),ratio*activeHRU,(len(subSampleG[0])+len(subSampleS[0])+len(HRUSampleG[0])+len(HRUSampleS[0])+len(HRUSampleH[0])+len(bsnSample[0])+(len(soilSample[0])*len(soilParameters))),len(subSampleG[0]),len(subSampleS[0])/len(activeHrulist[0]), len(HRUSampleG[0]),len(HRUSampleS[0])/len(activeHrulist[0]),len(HRUSampleH[0])/activeHRU,len(bsnSample[0]),len(soilSample[0][0])))
    pass

def runModel(instance): # Provide a method to building instances
    locals()["instance_"+str(instance)]=ProcessSWAT(instance[0],instance[1],instance[2],instance[3],instance[4],instance[5],instance[6],instance[7],instance[8],instance[9],instance[10],instance[11])
    res=locals()["instance_"+str(instance)].run()
    return res

def printRes(results): # Write results into results.csv
    with open (globalPath+"//results.csv","a",newline="") as f:
        write=csv.writer(f)
        head=[]
        activeHru=0
        for i in activeHrulist[0]:
            activeHru+=i
        for i in basinParameters:
            head.append(i[1])
        for i in range(activeHru):
            for j in hruParameters:
                if j[5]=="h":
                    head.append("HRU_HRU"+str(i+1)+"_"+j[1])
        for i in range(len(calibrationOrder[0])):
            for j in hruParameters:
                if j[5]=="s":
                    head.append("HRU_BSN"+str(calibrationOrder[0][i])+"_"+j[1])
        for i in hruParameters:
            if i[5]=="g":
                head.append("HRU_GBL"+"_"+i[1])
        for i in range(len(calibrationOrder[0])):
            for j in subbasinParameters:
                if j[5]=="s":
                    head.append("BSN_BSN"+str(calibrationOrder[0][i])+"_"+j[1])
        for i in subbasinParameters:
            if i[5]=="g":
                head.append("BSN_GBL"+"_"+i[1])
        for i in soilType:
            for j in soilParameters:
                head.append("SOL_"+i+str(j[0]))
        head.append("R2")
        head.append("NSE")
        write.writerow(head)
        if singleTest:
            write.writerows([results])
        else:
            write.writerows(results)
        
if __name__=="__main__":
    check()
    sampleGeneration()
    poolList=[]
    pool0=Pool(int(cpu_count()/4))
    for i in range(1):
        poolList.append([i,sample[i],observedData[0],calibrationOrder[activeCalibration[0]-1],activeHrulist[0],basinParameters,hruParameters,subbasinParameters,warmup,extractionType[0],soilType,soilParameters]) # Avoid using global varibles while applying multiprocessing.
    if singleTest:
        printRes(runModel(poolList[0]))
    else:
        results=pool0.map_async(runModel,poolList).get() 
        printRes(results)
    pass