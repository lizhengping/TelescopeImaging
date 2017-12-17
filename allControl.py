import os
import time
import subprocess
import shlex
import threading
import visa
import sys
sys.path.append('./Device/devicelib')
sys.path.append('../Plot')
from Device.AFG3252 import AFG3252
from configControl import *
from Device.ITECH_IT6322 import IT6322
from takephoto import camera
#import const
from telescope import *
import signal
import psutil

def kill(proc_pid):
    process = psutil.Process(proc_pid)

    for proc in process.children(recursive=True):
        proc.kill()
        #process.kill()

class control:
    def __init__(self, section="default"):
        keyboard=input('Turn on the devices press enter')
        deviceList=self.listResources()
        print(deviceList)
        self.TDC_state=''
        self.FlodName=''
        #self.device_init()

    def device_init(self):
        #self.SignalInit()
        self.powerInit()
        self.CamInit()


    def JTDCOpen(self):
        os.chdir('D:\\lidar\\Dataprocess\\run')
        shell_cmd = "run.bat"
        cmd = shlex.split(shell_cmd)
        #r = subprocess.check_output(["cmd.exe", "/c", "python try.py"])
        p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while p.poll() is None:
            line = p.stdout.readline()
            line=str(line,'utf8')
            print(line)
            if "4\r\n" in line:
                print("JTDC is processing")
                self.TDC_state="JTDC is processing"
            if "Connected"in line:
                print("TDC Connected")
                self.TDC_state="TDC Connected"
            if  "folderName is"in line:
                self.folderName=line[14:]
                print("folderName is "+Control.folderName)
            if "Data output Num:"in line:
                print(line[15:])
                print(len(line[17:-3]))
                Num=int(line[16:-2])
                print(Num)
                if Num==Control.xSubPic*Control.ySubPic:
                    self.TDC_state="Photos are over"
                    time.sleep(3)
                    kill(p.pid)
            if "TDC tube is open" in line:
                print("TDC tube is open")
                self.TDC_state="TDC tube is open"



    def listResources(self):
        rm = visa.ResourceManager()
        return rm.list_resources()

    def wholePic(self,fileFoldName,xPictures,yPictures):
        os.chdir('C:\\lidar\\program\\Plot')
        shell_cmd = "python wholePicture.py "+fileFoldName+" %d %d" %(xPictures,yPictures)
        cmd = shlex.split(shell_cmd)
        p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while p.poll() is None:
            line = p.stdout.readline()
            line=str(line,'utf8')
            print(line)

    def setSignal(self,ID,CH1_V,CH1_F,CH2_V,CH2_F):
        #############暂时只能设置频率，不能用周期设置，原因未知，先放弃周期的设置############
        Signal=AFG3252(ID)
        Signal.Recall_setup(1)

        Signal.setHighLevelCh1(CH1_V[0])
        Signal.setLowLevelCh1(CH1_V[1])
        #Signal.setFrequencyCh1_Hz(CH1_F)
        #Signal.setPeriodCh1_ms(CH_P# )
        Signal.setStatusCh1(1)

        Signal.setHighLevelCh2(CH2_V[0])
        Signal.setLowLevelCh2(CH2_V[1])
        #Signal.setFrequencyCh2_Hz(CH2_F)
        #Signal.setPeriodCh2_ms(1)
        Signal.setStatusCh2(1)

    def SignalInit(self):
        ID=getConfig(["SPI_ID"])
        CH1_V=getConfig(["SPI_CH1_High","SPI_CH1_Low"])
        CH1_F=getConfig(["SPI_CH1_Frequency"])
        CH2_V=getConfig(["SPI_CH2_High","SPI_CH2_Low"])
        CH2_F=getConfig(["SPI_CH2_Frequency"])

        self.setSignal(ID,CH1_V,CH1_F,CH2_V,CH2_F)

        # ID=getConfig(["SL_ID"])
        # CH1_V=getConfig(["SL_CH1_High","SL_CH1_Low"])
        # CH1_F=getConfig(["SL_CH1_Frequency"])
        # CH2_V=getConfig(["SL_CH2_High","SL_CH2_Low"])
        # CH2_F=getConfig(["SL_CH2_Frequency"])
        #
        # setSignal(ID,CH1_V,CH1_F,CH2_V,CH2_F)

        print('Signal is OK')

    def powerInit(self):

        ID=getConfig(["PowerID"])
        power=IT6322(ID)
        V=getConfig(["V"])
        for i in range(3):
            power.setVoltage(i,V[i])
        OutChennel=getConfig(['OutChennel'])
        power.setOutputStatuses(OutChennel)
        time.sleep(1)
        Vnow=power.measureVoltages()
        print(Vnow)
        for i in range(3):
            if abs(Vnow[i]-V[i]*OutChennel[i])>0.01:
                print("WARNING!: Chennel%s is Error!!",i)
                while(True):
                    pass
        print('Power is OK')

    def CamInit(self):
        telescopeCOM = getConfig(['telescopeCOM']) #望远镜串口
        PiCOM = getConfig(['PiCOM'])    #pi无线蓝牙串口
        self.cam = camera(telescopeCOM,PiCOM)

    def take_photo(self):
        os.chdir('C:\\lidar\\program\\Telescope')
        state=self.cam.tele1.get_Direction_Precise_uRad()
        print(state)
        time.sleep(1)
        self.xSubPic=getConfig(['xSubPic'])
        self.ySubPic=getConfig(['ySubPic'])
        step=getConfig(['step'])
        photoTime=getConfig(['photoTime'])


        self.cam.tele1.point_At_uRad_Precise(state[0],state[1])
        self.cam.takePhoto(self.xSubPic,self.ySubPic,step,photoTime)
        #self.cam.tele1.slewing_Stop()

    def wait_For_TDC(self):
        while self.TDC_state != "JTDC is processing":
            pass
        while self.TDC_state != "TDC Connected":
            pass
        time.sleep(2)
        print("Please open TDC tube")
        while self.TDC_state != "TDC tube is open":
            pass


if __name__ == '__main__':

    Control=control()

    while True:

        Control.folderName=''
        Control.TDC_state=''
        ###########Open JTDC##########
        threading._start_new_thread(Control.JTDCOpen,())

        Control.wait_For_TDC()
        time.sleep(1)
        keyboard=input('Check the devices and press enter to image\n')

        Control.take_photo()

        if Control.TDC_state=='Photos are over':
             Control.wholePic(Control.folderName,Control.xSubPic,Control.ySubPic)

        keyboard=input('Image next photo?/n')

