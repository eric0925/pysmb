"""Serial communication to ACU"""

import serial
import serial.tools.list_ports
import threading
import sys
import time
#argv1: Open,Close,Clear,SendAndRead
#argv2: comport
#argv3: baudrate
#argv4: 0 ,1, 2 or NULL; MEASURE; BUTTON_TEST
#argv5: getNumber or NULL; IV,LED; NULL
#argc6: timeout
def main(argv=None):
    if argv is None:
        argv = sys.argv
        #print(len(argv))
        #print(str(argv))
        if(len(argv) != 7):
            print("Results=FAIL")

    try:
        Function=str(sys.argv[1])
        Comport=str(sys.argv[2])
        baudrate=str(sys.argv[3])
        Command=str(sys.argv[4])
        Number=str(sys.argv[5])
        Timeout=str(sys.argv[6])

        if(Function=="Open"):
            ser_sock = AcuSerial(Comport, int(baudrate), "NULL", 1.5)
            print("{0} Opened".format(Comport))
            print("Results=PASS")

        elif(Function=="Clear"):
            ser_sock = AcuSerial(Comport, int(baudrate), "NULL", 1.5)
            ser_sock.flush()
            print("{0} Cleared".format(Comport))
            print("Results=PASS")

        elif (Function == "Close"):
            ser_sock = AcuSerial(Comport, int(baudrate), "NULL", 1.5)
            ser_sock.close()
            print("{0} Closed".format(Comport))
            print("Results=PASS")

        elif (Function == "SendAndRead"):
            if(Command=="0"):
                ser_sock = AcuSerial(Comport, int(baudrate), "i m CNwAccessWifi", float(Timeout))
                result=ser_sock.send_command()
                if result=="":
                    print("Results=FAIL")
                else:
                    print(result)
                    print("Results=PASS")
            elif(Command=="1"):
                ser_sock = AcuSerial(Comport, int(baudrate), "c {0} 65543 5".format(Number), float(Timeout))
                result=ser_sock.send_command()
                if result=="":
                    print("Results=FAIL")
                else:
                    print(result)
                    print("Results=PASS")
            elif(Command=="2"):
                ser_sock = AcuSerial(Comport, int(baudrate), "c {0} 65543 6".format(Number), float(Timeout))
                result=ser_sock.send_command()
                if result=="":
                    print("Results=FAIL")
                else:
                    print(result)
                    print("Results=PASS")
            elif(Command=="MEASURE"):
                ser_sock = AcuSerial(Comport, int(baudrate), "{0} {1}".format(Command,Number), float(Timeout))
                result=ser_sock.send_command()
                if result=="":
                    print("Results=FAIL")
                else:
                    print(result)
                    print("Results=PASS")

            elif(Command=="BUTTON_TEST"):
                ser_sock = AcuSerial(Comport, int(baudrate), "{0}".format(Command), float(Timeout))
                result=ser_sock.send_command()
                if result=="":
                    print("Results=FAIL")
                else:
                    print(result)
                    print("Results=PASS")
            elif(Command=="POWER_OFF" or "BAT_2V8" or "BAT_3V7" or "BAT_4V" or "USB_4V6" or "USB_5V" or "USB_5V3"):
                ser_sock = AcuSerial(Comport, int(baudrate), "{0}".format(Command), float(Timeout))
                result=ser_sock.send_command()
                if result=="":
                    print("Results=FAIL")
                else:
                    print(result)
                    print("Results=PASS")
        else:
            print("Results=FAIL")
    except Exception as e:
        print("Results=FAIL")



class AcuSerial(object):

    def __init__(self, Port="COM3",Baudrate=115200,Command="NULL",Timeout=1):

        """
        Initializes serial socket at given port and baud rate

        All other serial configuration is default: 8-N-1.
        Also uses a timeout for a read
        """
        try:
            self._port = Port
            self._baud = Baudrate
            self._lock = threading.Lock()
            self._command_timeout = Timeout
            self._serial_sock = serial.Serial(self._port, self._baud,
                                          timeout=1)
            self._command=Command+"\r\n"
            time.sleep(2)

            self._serial_sock.flushInput()
            self._serial_sock.flushOutput()
            self._serial_sock.flush()

        except Exception as e:
            print(e)
            print("Results=FAIL")

    def flush(self):
        try:
            self._serial_sock.flushInput()
            self._serial_sock.flushOutput()
            self._serial_sock.flush()
        except Exception as e:
            print(e)
            print("Results=FAIL")
    def send_command(self):
        """
        Sends command and waits for response

        Locks the socket for read/write for thread safe operation
        """
        try:
            with self._lock:
                return self._send_command(self._command)
        except Exception as e:
            print(e)
            print("Results=FAIL")
    def _send_command(self, data):
        """
        Sends command and waits for response
        """
        try:
            self._serial_sock.write(data.encode())

            return self._read_response()

        except Exception as e:
            print(e)
            print("Results=FAIL")

    def _read_response(self):
        """ Reads response after command has been sent"""
        try:
            start_time = time.time()
            received = ""
            while time.time() < start_time + self._command_timeout:
                received = received + self._serial_sock.read().decode(errors='ignore')
                if received.find("_RDY") !=-1:
                    break
            return received

        except Exception as e:
            print(e)
            print("Results=FAIL")

    def close(self):
        try:
            self.flush()
            self._serial_sock.close()

        except Exception as e:
            print(e)
            print("Results=FAIL")

# self test
if __name__ == "__main__":
    sys.exit(main())

