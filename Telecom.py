from serial import *
import threading
import re
import time
class TeleSerial:
    def __init__(self,com='COM2'):
        #串口初始化配置
        #串口设置相关变量

        self.ser = Serial()
        self.port = com
        self.baudrate =9600
        self.res=''
        self.defalt_init()

    def defalt_init(self):
        #self.port = 'COM2'
        #self.baudrate =9600
        self.ser.setPort(self.port)
        self.ser.baudrate=self.baudrate
        self.ser.open()
        print (self.ser.isOpen())
        print (self.ser)
        threading._start_new_thread(self.read_Data,())

    def read_Data(self):
        message=''
        char=''
        response=[]
        while True:
            try:
                while char !='#':
                   char=str(self.ser.read(),encoding = "utf-8")
                   message +=char
                char=''
            except e:
                print('error',e)
                continue
            if message != '':
                lenght=len(message)
                if lenght==1:
                    if message=='#':
                        self.res='action'

                if (lenght==10) or (lenght==18):
                    message=message[:-1]
                    response = re.split(',', message)
                    response = list(map(lambda x: int(x, 16), response))
                    if lenght==10:
                        A = response[0] * (1 / 65536 * 360)
                        E = response[1] * (1 / 65536 * 360)
                        if E >= 180 :
                            E = -(360-E)
                    if lenght==18:
                        A = response[0] * (1 / 4294967296 * 360)
                        E = response[1] * (1 / 4294967296 * 360)
                        if E >= 180 :
                            E = -(360-E)
                    response = [A, E]
                    self.res = response
            message = ''
            #(self.res)

    def read_data(self):
        message=''
        char=''
        response='action'
        E=None
        A=None
        while True:
            try:
               char+=str(self.ser.read(),encoding = "utf-8")

            except:
                char=''
                getchar=''
                while getchar!='#':
                    try:
                        getchar=str(self.ser.read(), encoding = "utf-8")
                    except:
                        pass
            continue
            #print('char',char)
            if char != '':
                message+=char
                if char=='#':
                    message=message[:-1]
                    if message !='':
                        response=re.split(',',message)
                        response=list(map(lambda x: int(x, 16), response))
                        if len(message)==9:
                            E=response[0]*(1/65536*360)
                            A=response[1]*(1/65536*360)
                        if len(message)==17:
                            E=response[0]*(1/4294967296*360)
                            A=response[1]*(1/4294967296*360)
                        response=[E,A]
                        self.res=response
                        #print(response)
                        message=''
                    else:
                        self.res='action'
                char=''


    def Send(self,context):
        #print(str.encode(context1))
        n = self.ser.write( bytes(context, encoding = "utf8"))


    def Send_signal(self,width=1):
        self.ser.write(b'\x80')


    def open(self):
        self.ser.open()
        if self.ser.isOpen() == True:
            return True

    def close(self):
        self.ser.close()
        if self.ser.isOpen() == False:
            return True

if __name__=='__main__':
   # TS1=TeleSerial('COM2')
    subPitureSignal=TeleSerial("COM9")
    while True:
       subPitureSignal.Send("GO")
       time.sleep(0.5)