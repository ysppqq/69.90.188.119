#!python
import time,sys,json
import os
import paramiko
import socket
socket.setdefaulttimeout(5)
from dnsmonlib import *
id_rsa = '/root/.ssh/id_rsa'
def VPSM_GET(host,port,user,passwd,filename):
    import paramiko
    t = paramiko.Transport((host,port))
    t.connect(username=user,password=passwd)
    sftp = paramiko.SFTPClient.from_transport(t)
    remotepath = filename
    localpath= host+"_"+filename
    sftp.get(remotepath,localpath)
    t.close()
def VPSM_PUT(host,port,user,passwd,filename):
    t = paramiko.Transport((host,port))
    t.connect(username=user,password=passwd)
    remotepath = filename
    localpath= filename
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(localpath,remotepath)
    sftp.close()
    t.close()
def VPSM_CMD(host,port,user,passwd,cmd):
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host,username=user,password=passwd,port=port,timeout=10)
    stdin,stdout,stderr = ssh.exec_command(cmd)
    if cmd.find("&")!=-1:
        return "OK"
    return stdout.read()
def check_online(ip,port,passwd):
    try:
        data =  VPSM_CMD(ip,port,'root',passwd,"id")
        return 1
    except:
        return 0
def reset(dst):
    fi = open("remote_list","r")
    a = fi.read().split("\n") 
    for host in a:
        if host:
             user, ip, port , passwd = host.split(":")
             port = int(port)
             if ip == dst:
                 print VPSM_CMD(ip,port,user,passwd,"sh restart.sh&")
                 break
def MON(a):
    online = []
    for host in a.split("\n"):
        if host:
            user, ip, port , passwd = host.split(":")
            port = int(port)
            print "%s run:check " %(ip),
            if check_online(ip,port,passwd):
                online.append(host)
                print " ONLINE"
            else:
                print " DIE"
    size = len(online)
    names = buildnames(size)
    for i in range(0,size):
        fi = open("input.conf","w")
        fi.write(json.dumps(names[i]))
        fi.close()
        user, ip, port , passwd = online[i].split(":")
        port = int(port)
        print "LOADING",ip
        VPSM_CMD(ip,port,user,passwd,"killall -9 python")
        VPSM_PUT(ip,port,user,passwd,"webmon-ex.py")
        VPSM_PUT(ip,port,user,passwd,"dns.tar")
        VPSM_PUT(ip,port,user,passwd,"input.conf")
        VPSM_CMD(ip,port,user,passwd,"tar xf dns.tar")
        VPSM_CMD(ip,port,user,passwd,"nohup python webmon-ex.py&")

if __name__ == "__main__":
    file = open("remote_list", 'r')
    a = file.read()
    file.close()
    online = []

    if sys.argv[1] == "MON":
        MON(a)
        sys.exit()

    fun = eval('VPSM_'+sys.argv[1])
    cmd = sys.argv[2]
    for host in a.split("\n"):
        if host:
            user, ip, port, passwd = host.split(":")
            port = int(port)
            try:
                print fun( ip,port,'root',passwd,cmd)
            except:
                print ip,"die"
