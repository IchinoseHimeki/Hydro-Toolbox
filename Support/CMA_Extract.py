'''
File: CMA_Extract.py
File Created: 2021-05-19 14:03:33
Author: IchinoseHimeki (darwinlee19980811@hotmail.com)
-----
Last Modified: 2022-01-21 14:50:43
Modified By: IchinoseHimeki (darwinlee19980811@hotmail.com>)
-----
Copyright 2022
Requisite: Python 3.10+
Description: A Script to Extract data download from https://data.cma.cn to SWAT weather generator input csvs.
A further database generator for SWAT is https://www.researchgate.net/publication/294535100_SWAT_Weather_Database, where these csvs could be able to use. Again, thanks for his efforts.
If using SWAT+, SWAT+ do convert SWAT weather data into SWAT+ format. Cheers!
Data URL is http://data.cma.cn/data/cdcdetail/dataCode/SURF_CLI_CHN_MUL_DAY.html.
Normally it includes serveral essentinal parameters, average windspeed, average relative humidity, sunshine hours, 24hrs precipitation, maximum temperature and minimum temperature. And it could print specific csvs.
'''

import csv
import os
import shutil

path = os.getcwd()
doOverwrite=True
doCheckDuplicate=False

def check():
    if not os.path.exists(path+"\\Input") or not os.listdir(path+"\\Input"):
        raise IOError("Input Files are Missing!")
    if not os.path.exists(path+"\\Output"):
        os.mkdir(path+"\\Output")
    else:
        if doOverwrite:
            shutil.rmtree(path+"\\Output")
            os.mkdir(path+"\\Output")
    print("Checks passed.")
    pass

def dateConstructor(year,month,day):
    time=str(month)+"/"+str(day)+"/"+str(year)
    return str(time)

def readTxt(txt):
    output=[]
    header=[]
    pres=[]
    winds=[]
    rhs=[]
    shs=[]
    temps=[]
    with open(txt,'r') as f:
        header=f.readline().split()
        data=f.readlines()
        for line in data:
            output.append(line.split())
    year=header.index("V04001")
    month=header.index("V04002")
    day=header.index("V04003")
    id=header.index("V01301")
    pre=header.index("V13305")
    wind=header.index("V11291_701")
    rh=header.index("V13003_701")
    sh=header.index("V14032")
    max_temp=header.index("V12011")
    min_temp=header.index("V12012")
    for lines in output:
        date_id=[dateConstructor(lines[year],lines[month],lines[day]),lines[id]]
        if str(lines[pre])=="999990.0000": # For very small values.
            prei="0.0100"
        elif str(lines[pre])=="999999.0000": # For nodata values.
            prei="0.0000"
        else:
            prei=str(lines[pre])
        if str(lines[wind])=="999999.0000": # For nodata values.
            windi="0.0000"
        else:
            windi=str(lines[wind])
        pres.append([date_id[0],date_id[1],prei])
        winds.append([date_id[0],date_id[1],windi])
        rhs.append([date_id[0],date_id[1],str(lines[rh])])
        shs.append([date_id[0],date_id[1],str(lines[sh])])
        temps.append([date_id[0],date_id[1],str(lines[max_temp]),str(lines[min_temp])])
    return pres,winds,rhs,shs,temps

def checkDuplicate(list):
    target=[]
    for i in list:
        if i not in target:
            target.append(i)
    return target

def writeCsv(kind,data):
    if str(kind) == "pcp":
        header=["Date","Station","PCP"]
    elif str(kind) == "hmd":
        header=["Date","Station","HMD"]
    elif str(kind) == "tmp":
        header=["Date","Station","TMPmax","TMPmin"]
    elif str(kind) == "slr":
        header=["Date","Station","SLR"]
    elif str(kind) == "wnd":
        header=["Date","Station","WND"]
    else:
        raise Exception("Output type \""+str(kind)+"\" is not defined!")
    if not len(data[0]) == len(header):
        raise Exception("Wrong Data!")
    with open(path+"\\Output\\"+str(kind)+".csv","a+",newline="") as f:
        writer=csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

if __name__ == "__main__":
    check()
    prpData=[]
    wndData=[]
    slrData=[]
    hmdData=[]
    tmpData=[]
    for files in os.listdir(path+"\\Input"):
        prpData.extend(readTxt(path+"\\Input\\"+str(files))[0])
        wndData.extend(readTxt(path+"\\Input\\"+str(files))[1])
        hmdData.extend(readTxt(path+"\\Input\\"+str(files))[2])
        slrData.extend(readTxt(path+"\\Input\\"+str(files))[3])
        tmpData.extend(readTxt(path+"\\Input\\"+str(files))[4])       
    if doCheckDuplicate:
        prpData = checkDuplicate(prpData)
        wndData = checkDuplicate(wndData)
        hmdData = checkDuplicate(hmdData)
        slrData = checkDuplicate(slrData)
        tmpData = checkDuplicate(tmpData)
    writeCsv("pcp",prpData)
    writeCsv("hmd",hmdData)
    writeCsv("slr",slrData)
    writeCsv("wnd",wndData)
    writeCsv("tmp",tmpData)
    pass