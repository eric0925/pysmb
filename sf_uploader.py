"""
Created on Tue Feb  6 15:42:19 2018

@author: simonlin
"""
import requests
import bs4
import sys
import csv

headers = {'Content-type':'text/xml'}


logfmt = "%(asctime)s [%(module)s] %(message)s"
timefmt = "%H:%M:%S" #"%Y-%m-%d %H:%M:%S"
#logging.basicConfig(level=logging.DEBUG, format=logfmt, datefmt=timefmt)

#print('__file__={0}'.format(__file__))

def SF_Upload_GET_MAC(strSN, strSiteName, strUserName, strSegment, strWeblink, strOperation):
    print("SF_Upload_GET_MAC")
    print("SF_CheckSNRoute:Enter")
    print("strSN:[{0}]".format(strSN))
    print("strSiteName:[{0}]".format(strSiteName))
    print("strUserName:[{0}]".format(strUserName))
    print("strSegment:[{0}]".format(strSegment))
    print("strWeblink:[{0}]".format(strWeblink))
    print("strOperation:[{0}]".format(strOperation))

    if strSiteName == ";" and strUserName == "":
        body = """<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
            <{1} xmlns="http://tempuri.org/">
              <strMsg>{0}</strMsg>
            </{1}>
          </soap:Body>
        </soap:Envelope>""".format(strSegment, strOperation)
    else:
      print("get here")
      body = """<?xml version="1.0" encoding="utf-8"?>
      <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
          <{4} xmlns="http://tempuri.org/">
            <strSN>{0}</strSN>
            <strSiteName>{1}</strSiteName>
            <strUserName>{2}</strUserName>
            <strMsg>{3}</strMsg>
          </{4}>
        </soap:Body>
      </soap:Envelope>""".format(strSN, strSiteName, strUserName, strSegment, strOperation)

    #logging.debug("body:[{0}]".format(body))
    print("---------------------------")
    try:
        print("---------------------------")
        response = requests.get(strWeblink, timeout=10)
        print("response:",response)
    except requests.ConnectTimeout as e:
        #print("requests:ConnectTimeout:[{0}]".format(e))
        return (-1, "requests:ConnectTimeout:[{0}]".format(e))
    except:
        #print("requests.get:Unexpected error:[{0}]".format(sys.exc_info()[0]))
        return (-2, "requests.get:Unexpected error:[{0}]".format(sys.exc_info()[0]))
        raise

    #print("response ok={0}".format(response.ok))
    if response.ok == False:
        #print("response.status_code:[{0}]".format(response.status_code))
        return (-3, "response.status_code:[{0}]".format(response.status_code))

    #print("response ok")

    try:
        response = requests.post(strWeblink, data=body, headers=headers)
    except (Exception,e):
        #print("requests.post:Unexpected error:[{0}]".format(str(e)))
        return (-4, "requests.post:Unexpected error:[{0}]".format(str(e)))
        raise

    #logging.debug("response:(response.content)=[{0}]".format(type(response.content)))

    #print("response:len=[{0}]".format(len(response.content)))
    if (len(response.content) > 425):
        #print("Error Response format")
        return (-5, "Error Response format")

    #logging.debug("SF_upload_result(response)=[{0}]".format(SF_upload_result(response, strOperation)))

    return SF_upload_result(response)

def SF_upload_result(response):
    #print("SF_upload_result:response.text:[{0}]".format(response.text))
    res = bs4.BeautifulSoup(response.text, 'xml')
    #print("SF_upload_result:res:[{0}]".format(res))
    result_str='Sajet_GET_MACResult'
    result = res.select(result_str)
    #print("SF_upload_result:result:[{0}]".format(result))
    #print("SF_upload_result:result[0].getText():[{0}]".format(result[0].getText()))
    if str(result[0].getText()) == "OK":
        return (1, "")
    else:
        return (0, "{0}".format(str(result[0].getText())))

def get_Bench_Default_Config(filename):
    config = dict()
    try:
        with open(filename, 'r', newline='') as f:
            reader = csv.reader(f)
            for line in reader:
                #print(line)
                for idx, item in enumerate(line):
                    if idx > 0: continue
                    #print(idx, item, line[idx + 1])
                    config[item] = line[idx + 1]
    except Exception as e:
        print(e)
    return config
    
def main(argv=None):
    if argv is None:
        argv = sys.argv
        #print(len(argv))
        print(str(argv))
        if(len(argv) != 5):
            print("Results=FAIL")
            return

    filename = 'c:\kazam\BenchCFG\Bench_Default_Config.csv'     #http://10.240.19.198:93/WebService.asmx
    site_info = get_Bench_Default_Config(filename)              #site_info["weblink"]
    print("weblink = {}".format(site_info["weblink"]))
    ret, result = SF_Upload_GET_MAC(argv[1], "", "", argv[1], site_info["weblink"], argv[2])
    print("ret = {}".format(ret))
    print("value = {}".format(result))

    if(result == argv[3]):
        print("Results=PASS")
        return
    print("Results=FAIL")
    return


    #if ret == 0 and len(result) == 12:
    #    result = ':'.join(result[i:i+2] for i in range(0,12,2))
    #    print("MAC compare {} to {}".format(result, argv[3]))
    #    if(result == argv[3]):
    #        print("Results=PASS")
    #        return
    #print("Results=FAIL")
    #return

if __name__ == "__main__":
    sys.exit(main())
