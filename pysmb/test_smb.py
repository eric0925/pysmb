
from smb import *
from smb.SMBConnection import SMBConnection
import time
import os


def upload_pysmb(upload_file_name):
    #print("upload_pysmb file_name:",upload_file_name)

    host="127.0.0.1"
    username="ericlee"
    password="1234"
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
    localFile=open("%s"%upload_file_name,"rb")      #打開本地文件，注意如果是二進制文件，比如zip包，需要加上參數b，即binary模式，默認是t模式，即text文本模式。

    conn.storeFile("shared2","/eric-%s.dat"%time.strftime('%m%d-%H%M%S', time.localtime(time.time())),localFile) 


def download_pysmb(download_file_name):
    #print("upload_pysmb file_name:",upload_file_name)

    host="127.0.0.1"
    username="ericlee"
    password="1234"
    port=445
    conn=SMBConnection(username,password,"","",use_ntlm_v2 = True)
    result = conn.connect(host, port)   #default : 445
   
    localFile=open("%s"%download_file_name,"wb")      #打開本地文件，注意如果是二進制文件，比如zip包，需要加上參數b，即binary模式，默認是t模式，即text文本模式。

    conn.retrieveFile("shared2","/eric-%s.dat"%time.strftime('%m%d-%H%M%S', time.localtime(time.time())),localFile) 

    localFile.close()

upload_pysmb("text_1.txt")  #執行擋在桌面   遇上傳的檔案在與執行檔的相對路徑

##download_pysmb("1650/eric1")