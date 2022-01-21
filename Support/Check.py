'''
File: Check.py
File Created: 2020-05-30 17:42:33
Author: IchinoseHimeki (darwinlee19980811@hotmail.com)
-----
Last Modified: 2022-01-21 14:33:51
Modified By: IchinoseHimeki (darwinlee19980811@hotmail.com>)
-----
Copyright 2022
Requisite: Python 3.10+
Description: This is to check that if 2 .asc files covers exactly the same area.
REMOVE THE HEADERS OF BOTH FILES FIRST!
I have supposed that you have got two same size(cols and rows), if you cannot do that, it will help by below steps.
1. Remove last lines till they are same
2. Uncomment the code as below
Since I had all files(res.txt & res.asc) in APPEND mode, please clear them if necessary.
Do not forget to add HEADERS back while using res.asc
'''

import os
import array

def readASC(FileName):
    data=[]
    with open(FileName,'r+') as f:
        data=[i[:-1].split(' ') for i in f.readlines()]
    return data

data2 = readASC("D://ToCheck//soillooked.asc")
data1 = readASC("D://ToCheck//dem.asc")
row = len(data1)
col = len(data1[0])
# Uncomment to remove the elements in each line
# for item in data2:
#     del item[3263]
b=data2
data3=list()
with open("D://ToCheck//res.txt",'a+') as f:
    for lines in range(row):
        for eles in range(col-1):
            if ((data1[lines][eles]!=data2[lines][eles]) and ((data1[lines][eles]=='-9999') or (data2[lines][eles]=='-9999'))):
            # if (((data1[lines][eles]!='-9999') & (data2[lines][eles]=='-9999'))): # That is an another way to judge
                print(str(lines)+","+str(eles))
                word = str(lines)+","+str(eles)+":  "+str(data1[lines][eles])+"  "+str(data2[lines][eles])+"\n"
                f.writelines(word)
                data3.clear()
                for i in range(20):
                    if(data2[lines+i][eles]!="-9999"):
                        data3.append(int(data2[lines+i][eles]))
                    if(data2[lines-i][eles]!="-9999"):
                        data3.append(int(data2[lines-i][eles]))
                    if(data2[lines+i][eles+i]!="-9999"):
                        data3.append(int(data2[lines+i][eles+i]))
                    if(data2[lines-i][eles-i]!="-9999"):
                        data3.append(int(data2[lines-i][eles-i]))
                    if(data2[lines][eles+i]!="-9999"):
                        data3.append(int(data2[lines][eles+i]))                        
                    if(data2[lines][eles-i]!="-9999"):
                        data3.append(int(data2[lines][eles-i]))
                b[lines][eles]=round(sum(data3)/len(data3)) # get int numbers while missing data.
                continue
            else:
                continue

with open("D://ToChck//res.asc",'a+') as f:
    for i in range(len(b)):
        for j in range(len(b[i])):
             f.write(str(b[i][j]))
             f.write(' ')
        f.write('\n')

#abandoned code below
    # data3=readASC("D://ToCheck//dd1.asc")
    # row = len(data3)
    # col = len(data3[0])
    # c=data3 
    # for lines in range(row):
    #     for eles in range(col):
    #         if((data3[lines][eles]!='-9999') & (data3[lines][eles]!='5')):
    #             c[lines][eles] ='0'
    #         elif( data3[lines][eles]=='5'):
    #             c[lines][eles]='1'
    #         else:
    #             continue


    # with open("D://ToCheck//DD2.asc",'a+') as f:
    #     for i in range(len(c)):
    #         for j in range(len(c[i])):
    #              f.write(str(c[i][j]))
    #              f.write(' ')
    #         f.write('\n')

    # data3=readASC("D://ToCheck//dd1.asc")
    # row = len(data3)
    # col = len(data3[0])
    # for item in data3:
    #     del item[352]
    #     del item[351]
    # c=data3

    # with open("D://ToCheck//DD2.asc",'a+') as f:
    #     for i in range(len(c)):
    #         for j in range(len(c[i])):
    #              f.write(str(c[i][j]))
    #              f.write(' ')
    #         f.write('\n')

