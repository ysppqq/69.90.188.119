import time
import random
import socket
import threading
result = {'MON':0,'SAVE':0,'DATA':[]}
names = []
dnss = [
'4.2.2.6 ',
'8.8.8.8',
'8.8.4.4'
]
import DNS
import json
import os
lock = threading.Lock()
def checkdns(name,dns):
    try:
        reqobj = DNS.Request()
        answerobj = reqobj.req(name = name,server = dns,timeout=3)
        if len(answerobj.answers):
            return 1
    except:
        pass
    return 0
def dnslookup(name,dns):
    global lock
    global result
    if checkdns(name,dns):
        lock.acquire()
        if name not in result['DATA']:
            result['DATA'].append(name)
        lock.release()
    else:
        return
def resultthread():
    global result
    global lock
    while 1:
        lock.acquire()
        try:
            fo = open("output.conf","w")
            fo.write(json.dumps(result))
            fo.close()
            result['SAVE'] = time.time()
        except:
            pass
        lock.release()
        time.sleep(10)
    return
def getdns():
    return dnss[random.randrange(0,len(dnss))]
def dnsthread(pool):
    for name in pool:
        dnsServer = getdns()
        dnslookup(name,dnsServer)
    return
def main():
    global result
    global names
    if os.access("input.conf",os.R_OK):
        tmp = json.loads(open("input.conf","r").read())
    for line in tmp:
        if line not in names:
            names.append(line)
    pools = []
    NUM = 3
    each = len(names) / NUM
    for i in range(0,NUM):
        pools.append(names[i*each:(i+1)*each])
    pools[0] = pools[0] + names[(i+1)*each:]
    th = []
    for i in range(0,NUM):
        print len(pools[i])
        a = threading.Thread(target=dnsthread,args=[pools[i]])
        a.start()
        th.append(a)
    for i in th:
        i.join()
th = threading.Thread(target=resultthread,args=[])
th.start()
while 1:
    main()
    print "--sleep--"
    lock.acquire()
    result['MON'] = time.time()
    lock.release()
    time.sleep(20)
