import os

globalPath=os.getcwd()
pipeDiameter=0.9
pipeDiameterFormat="            <Value>"+str(pipeDiameter)+"</Value>\n"
pipeDiameterIndex=[1373,1680,2025,1947]
leakDiameter=[0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.010,0.011,0.012,0.013,0.014,0.015,0.016,0.017,0.018,0.019,0.020]
leakDiameterFormat="            <Value>"+"</Value>\n"
leakDiameterIndex=[2993,2103,2458]
point=100
pointFormat="            <Value>"+"</Value>\n"
pointIndex=[1333,1640]
step=100

doPipeDiameter=True
doLeakDiameter=True
doPipeLength=True

def writeData(Index,Value,fileName):
    printData=[]
    with open(globalPath+"\\EDIF.FMedif","r",newline="") as f:
        readData=f.readlines()
    for i in range(len(readData)):
        if i in Index:
            loc=Index.index(i)
            printData.append([Value[loc]])
        else:
            printData.append([readData[i]])
    with open(globalPath+"\\Result\\"+str(fileName)+".FMedif","w",newline="") as f:
        for i in printData:
            f.write(i[0])

def constrctOneData(points,leakDiameter):
    index=[]
    value=[]
    if doPipeDiameter:
        for i in range(len(pipeDiameterIndex)):
            pipeDiameterFormat="            <Value>"+str(pipeDiameter)+"</Value>\n"
            index.append(pipeDiameterIndex[i])
            value.append(pipeDiameterFormat)
    if doLeakDiameter:
        for i in range(len(leakDiameterIndex)):
            leakDiameterFormat="            <Value>"+str(leakDiameter)+"</Value>\n"
            index.append(leakDiameterIndex[i])
            value.append(leakDiameterFormat)
    if doPipeLength:
        point=[points,4000-points]
        for i in range(len(pointIndex)):
            pointFormat="            <Value>"+str(point[i])+"</Value>\n"
            value.append(pointFormat)
            index.append(pointIndex[i])
    fileName="Sim_Leak_"+str(points)+"_Diameter_"+str(leakDiameter)
    return [index,value,fileName]

def constructLeak():
    points=[]
    pendingPoints=[]
    toWriteData=[]
    num=int((4000-point)/step)
    for i in range(num):
        points.append(i*step+point)
    for i in range(len(leakDiameter)):
        for j in range(len(points)):
            pendingPoints.append([points[j],leakDiameter[i]])
    for i in pendingPoints:
        toWriteData.append(constrctOneData(i[0],i[1]))
    for i in range(len(toWriteData)):
        writeData(toWriteData[i][0],toWriteData[i][1],toWriteData[i][2])

constructLeak()
prefix="D:\模拟\Args\\"
outputList=[]
fileList=os.listdir(globalPath+"\\Result")
for i in fileList:
    outputList.append(str(prefix)+str(i)+"\n")
with open(globalPath+"\\Res.txt","a+",newline="") as f:
    f.writelines(outputList)
