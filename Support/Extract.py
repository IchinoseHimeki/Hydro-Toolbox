import csv
import os
import time
from datetime import datetime as dt
# This will help while extracting data from a file to station-sperated csvs. Just to make it easier while tweaking models.
# Sorry due to copyrights of the model, I will NEVER provide ANY details of this model, only a soultion for problems while dealing.
# This contains some good ways, it will be applied into other files while possible.

Location = os.getcwd()
def readResult():
    t=0
    with open(Location+'\\Obs_Total_River_Flow.dat','r+') as f:
        next(f)
        data=[i[:-1].split(' ') for i in f.readlines()]
    newFolder()
    for i in range(3,len(data[0])-1):
        t=t+1
        number = 'p'+str(t)
        writeHead=["date","value"]        
        with open(Location+'\\Result\\'+number+'.csv','a+',newline='') as f:
            writer=csv.writer(f)
            writer.writerow(writeHead)
            for j in range(len(data)):           
                year = int(data[j][0])
                month = int(data[j][1])
                day = int(data[j][2])
                convertTime = dt(year,month,day)
                date=time.strftime("%y/%m/%d",convertTime.timetuple())
                writeData=[date,data[j][i]]
                writer.writerow(writeData)
                
        

def newFolder():
    if not os.path.exists(Location+'\\Result'):
        os.mkdir(Location+'\\Result')


if __name__ == "__main__":
    readResult()
    pass