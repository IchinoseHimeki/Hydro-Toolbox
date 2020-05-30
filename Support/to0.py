import os
# Becoming a 0 is never so easy than before, yeah
# Just joking, you cannot make rain back to the sky and evaporation back to the earth
# This is going to correct negative values which are interpolation by kriging method to 0
# Considering merging this to bullshitconverter.py
def being0(Target):
    Location=os.getcwd()+"\\"+Target
    Files = os.listdir(Location)
    Des=Target+"_MOD"
    for i in Files:
        Filename = Location+"\\"+i
        with open(Filename,'r+',newline='') as f:
            data=[i[:-1].split(' ') for i in f.readlines()]
            for col in range(6,len(data)):
                for row in range(len(data[7])):
                    if (data[col][row]!="-9999") and (data[col][row].startswith("-")):
                        data[col][row]="0"
        newDir(Target+"_MOD")
        with open(Location+"_MOD\\"+i,"a+",newline='')as f:
            f.writelines("ncols         351\nnrows         283\nxllcorner     21216938\nyllcorner     4950521\ncellsize      1000\nNODATA_value  -9999\n")
            for lines in range(6,len(data)):
                f.write(" ".join(map(str, data[lines]))+"\n")           

def newDir(Name):
    Location=os.getcwd()+"\\"+Name
    if not os.path.exists(Location):
        os.mkdir(Location)
    
if __name__ == "__main__":
    being0("ETo")
    pass