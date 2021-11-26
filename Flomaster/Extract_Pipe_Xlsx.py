import csv
import os
import openpyxl

globalPath=os.getcwd()
csvData=[]
def readXlsx(path,pos,leak):
    xlsx=openpyxl.load_workbook(path)
    sheet=xlsx.active
    Q_Left='{:.10f}'.format(float(str(sheet["D2"].value))*60000)
    Q_Right='{:.10f}'.format(float(str(sheet["D3"].value))*60000)
    Q_Leak='{:.10f}'.format(abs(float(str(sheet["D4"].value))*60000))
    v_Left='{:.10f}'.format(float(sheet["E2"].value))
    v_Right='{:.10f}'.format(float(sheet["E3"].value))
    v_Leak='{:.10f}'.format(abs(float(sheet["E4"].value)))
    result=[pos,leak,Q_Left,v_Left,Q_Right,v_Right,Q_Leak,v_Leak]
    return result

def printCsv():
    with open(globalPath+"\\Result.csv","a+",newline="") as f:
        csvWriter=csv.writer(f)
        csvWriter.writerow(["Pos <m>","Leak <mm>","Q_Left <L/min>","v_Left <m3/s>","Q_Right <L/min>","v_Right <m3/s>","Q_Leak <L/min>","v_Leak <m3/s>"])
        csvWriter.writerows(csvData)
        
if __name__ == '__main__':
    firstLayer=os.listdir(globalPath)
    firstLayer.remove("Extract.py")
    for i in firstLayer:
        pos=int(str(i).split(",")[1])
        secondLayer=os.listdir(globalPath+"\\"+str(i)+"\\")
        for j in secondLayer:
            leak=int(str(j).rstrip("mm.xlsx"))
            csvData.append(readXlsx(globalPath+"\\"+str(i)+"\\"+str(j),pos,leak))
    printCsv()