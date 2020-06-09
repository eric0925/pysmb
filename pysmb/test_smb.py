
from smb import *
from smb.SMBConnection import SMBConnection
import time
import os


def upload_pysmb(upload_file_name):
    host="127.0.0.1"
    username=""
    password=""
    port=445
    conn=SMBConnection(username,password,"","",use_ntlm_v2 = True)
    result = conn.connect(host, port)   #default : 445
    f=open(upload_file_name,'w')

    data=[  "host:%s\n"%host , \
            "username:%s\n"%username, \
            "password:%s\n"%password, \
            "port:%s\n"%port,\
            "result:%s\n"%result ]

    f.writelines(data)
    f.close()
    localFile=open("%s"%upload_file_name,"rb")

    conn.storeFile("shared2","/eric-%s.dat"%time.strftime('%m%d-%H%M%S', time.localtime(time.time())),localFile) 


def download_pysmb(download_file_name):
    host="127.0.0.1"
    username=""
    password=""
    port=445
    conn=SMBConnection(username,password,"","",use_ntlm_v2 = True)
    result = conn.connect(host, port)   #default : 445
   
    localFile=open("%s"%download_file_name,"wb")

    conn.retrieveFile("shared2","/eric-%s.dat"%time.strftime('%m%d-%H%M%S', time.localtime(time.time())),localFile) 

    localFile.close()

upload_pysmb("example.txt")
