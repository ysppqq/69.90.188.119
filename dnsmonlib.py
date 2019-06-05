import time
import random
import socket
import threading
import DNS
buildresult = []
def getwww(wwws):
    for i in wwws:
        yield i
def getdic(dics):
    for i in dics:
        yield i
def getcom(coms):
    for i in coms:
        yield i
def getarray():
    for i in range(ord('0'),ord('9')+1)+range(ord('a'),ord('z')+1)+[ord("-")]+[ord("_")]:
        yield chr(i)

def buildstr(string):
    if string.find("[L]") ==-1:
        buildresult.append(string)
    else:
        for i in getarray():
            tmp = string.replace("[L]",i,1)
            buildstr(tmp)
def getdns():
    return dnss[random.randrange(0,len(dnss))]
def print_r(dic):
    for i in dic:
        print "-",i

def buildnames(server):
    global buildresult
    output = []
    dnss = [
    '4.2.2.6 ',
    '8.8.8.8',
    '8.8.4.4'
    ]
    wwws = [
    "www.",
    "wap.",
    ""
    ]
    dics = [
    "cmbc[L][L]",
    "[L]95555",
    "[L]95555[L]",
    "95555[L]",
    "[L][L]95555",
    "95555[L][L]",
    "[L]cmbchina",
    "[L]cmbchina[L]",
    "[L][L]cmbchina",
    "cmbchina[L][L]",
    "cmbchina[L]",
    "[L][L]cmb",
    "[L]cmb",
    "[L]cmb[L]",
    "cmb[L][L]",
    "cmb[L]"
    ]
    coms = [
    '.com',
    '.net',
    '.cn',
    '.com.cn',
    '.tk',
    '.pw',
    '.cc'
    ]
    print "WWWS = "
    print_r(wwws)
    print "DICS = "
    print_r(dics)
    print "COMS = "
    print_r(coms)
    print "Building.."
    for i in getwww(wwws):
        for j in getdic(dics):
            for k in getcom(coms):
                buildstr(i+j+k)
    print "Building complete,total domain = ",  len(buildresult)
    size = len(buildresult)/server
    for i in range(0,server):
        output.append(buildresult[size*i:size*(i+1)])
    output[0]+=buildresult[size*server:]
    return output

if __name__=='__main__':
    buildnames(1)
