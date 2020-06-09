
from smb import *
from smb.SMBConnection import SMBConnection
import time
import os

def upload_pysmb(upload_file_name):
    host="192.168.55.116"
    username=""
    password=""
    port=445

    try:
        conn=SMBConnection(username,password,"","",use_ntlm_v2 = True)
        result = conn.connect(host, port,timeout=5)   #default : 445
        f=open(upload_file_name,'w')

        data=[  "host:%s\n"%host , \
                "username:%s\n"%username, \
                "password:%s\n"%password, \
                "port:%s\n"%port,\
                "result:%s\n"%result ]

        f.writelines(data)
        localFile=open("%s"%upload_file_name,"rb")     
        conn.storeFile("sharefold","/path/file-%s.dat"%time.strftime('%m%d-%H%M%S', time.localtime(time.time())),localFile) 
    except Exception as e:
        print(str(e))

def download_pysmb(download_file_name):
    host="0.0.0.0"
    username=""
    password=""
    port=445
    try:
        conn=SMBConnection(username,password,"","",use_ntlm_v2 = True)
        result = conn.connect(host, port)   #default : 445
    
        localFile=open("%s"%download_file_name,"wb")      

        conn.retrieveFile("sharefold","/path/file-%s.dat"%time.strftime('%m%d-%H%M%S', time.localtime(time.time())),localFile) 
        localFile.close()
    except Exception as e:
        print(str(e))

if __name__ == "__main__":

    upload_pysmb("filename")
    print("finish")
