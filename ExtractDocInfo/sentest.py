from os import listdir
from os.path import isfile, join

mypath='/home/.../indexbuildingtest/.../FACTS/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
cnt = 0
sinceList=[]
for fi in onlyfiles:
    f=open(mypath+fi,'r')
    try:
        data=f.readlines()
    except:
        print("Exception occured for" + fi)
    for d  in data:
        if(' see ' in d):
            if(d not in sinceList):
                x=d.replace(',','').replace('\n','')+','+str(fi)
                print(x)
                sinceList.append(x)
            cnt+=1
        else:
            cnt+=1
    #print(str(cnt) +' files processed ')
    f.close()


fout=open('sentence2.csv','a')
for s in sinceList:
    fout.write(s+'\n')
fout.close()

