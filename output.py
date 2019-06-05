import os
import sys
import json
import time
alive = 0
count = 0
def gettime(timeStamp):
    timeArray = time.localtime(timeStamp)
    return  time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
def flush():
    global alive
    global count
    os.system("python check.py GET output.conf")
    result = []
    data = os.popen("ls -m "+os.getcwd()+"/*_output.conf").read().replace(" ","").replace("\n","").split(",")
    if alive > 0:
        print alive,len(data)
        if len(data)!=alive:
            count +=1
        if count>3600:
            print "REBUILD"
            os.system("python check.py MON")
            alive = 0
            count = 0
            return
    else:
         alive = len(data)
    for line in data:
        try:
            buf = json.loads(open(line,"r").read())
            print time.time()-buf['MON'],line,'DATA',len(buf['DATA']),'MON',gettime(buf['MON']),'SAVE',gettime(buf['SAVE'])
            if time.time()-buf['MON']>=3600 and buf['MON']!=0:
                ip = line.split("/")[-1]
                ip = ip.split('_')[0]
                print ip,"reloading"
                from check import reset
                reset(ip)
            result += buf['DATA']
            os.remove(line)
        except:
            print line,'error'
            continue
    print len(result)
    fo = open("output.conf","w")
    fo.write(json.dumps(result))
    fo.close()
while 1:
    flush()
    time.sleep(60)
