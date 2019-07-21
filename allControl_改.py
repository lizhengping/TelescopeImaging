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
import scanMirror




class control:
    def __init__(self, section="default"):
        keyboard=input('Turn on the devices press enter\n')
        deviceList=self.listResources()
        print(deviceList)
        self.TDC_state=''
        self.FlodName=''
        self.device_init()

    def kill(proc_pid):
        process = psutil.Process(proc_pid)

        for proc in process.children(recursive=True):
            proc.kill()
            #process.kill()

    def get_config(self):
        self.mode = getConfig(['mode'])
        self.xSubPic = getConfig(['xSubPic'])
        self.ySubPic = getConfig(['ySubPic'])
        self.subsize = getConfig(['subsize'])
        if self.mode==3:
            self.linePixels=getConfig('linePixels')
            self.subsize=self.linePixels
        self.pixeltime_ms = getConfig(['pixeltime_ms'])
        self.pixel_waittime_ms = getConfig(['pixel_waittime_ms'])
        self.telescopeCOM = getConfig(['telescopeCOM'])  # 望远镜串口
        self.PiCOM = getConfig(['PiCOM'])  # pi无线蓝牙串口
        self.SignalID = getConfig(["SPI_ID"])
        self.step = getConfig(['step'])


    def device_init(self):
        self.get_config()
        self.CamInit()
        self.SignalInit()
        # self.powerInit()

    def get_subTakingtime(self):
        self.AFG_period = self.subsize * (self.pixeltime_ms + self.pixel_waittime_ms)
        print("AFG_period should be {}s".format(self.AFG_period/1000))
        self.subTakingtime = int(self.AFG_period/1000 + 2)
        # photoTime = int(getConfig(['subsize']) * (getConfig(['pixeltime_ms']) + getConfig(['pixel_waittime_ms']))/1000)+2
        #print("subTakingtime is {}".format( self.subTakingtime))

    def get_lineTakingtime(self):
        self.AFG_period = 2 * self.linePixels* (self.pixeltime_ms + self.pixel_waittime_ms)
        print("AFG_period should be {}s".format(self.AFG_period/1000))
        self.lineTakingtime = int(self.AFG_period/1000 + 0.5)



    def JTDCOpen(self):
        os.chdir('D:\\lidar\\program\\Dataprocess\\run')
        #shell_cmd = "run.bat"
        shell_cmd='java -classpath ../JTDC/target/classes;xchart-2.5.1.jar;jscience-4.3.1.jar com.hydra.test.groundtdcserver.AppFrame'
        #shell_cmd=shell_cmd+' {} {} {}'.format(4096,10,0)
        ms2ps=1000000000
        shell_cmd = shell_cmd + ' {} {} {}'.format(self.subsize, int(self.pixeltime_ms*ms2ps), self.pixel_waittime_ms)
        cmd = shlex.split(shell_cmd)
        print (cmd)
        #r = subprocess.check_output(["cmd.exe", "/c", "python try.py"])
        self.p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while self.p.poll() is None:
            line = self.p.stdout.readline()
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
                print("folderName is "+self.folderName)
            if "Data output Num:"in line:
                Num=int(line[16:-2])
                print(Num)
                if Num==self.xSubPic*self.ySubPic:
                    self.TDC_state="Photos are over"
                    time.sleep(3)
                    self.kill(self.p.pid)
            if "TDC tube is open" in line:
                print("TDC tube is open")
                self.TDC_state="TDC tube is open"



    def listResources(self):
        rm = visa.ResourceManager()
        return rm.list_resources()

    def wholePic(self,path):
        #,fileFoldName,xPictures,yPictures,subsize):
        os.chdir('D:\\lidar\\program\\Plot')
        shell_cmd = "python wholePicture.py {} {} {} {}".format(path,self.xSubPic,self.ySubPic,self.subsize)
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
        self.Signal=AFG3252(self.SignalID)
        self.Signal_reflash()



    # def SignalInit_detail(self):
    #     ID=getConfig(["SPI_ID"])
    #     CH1_V=getConfig(["SPI_CH1_High","SPI_CH1_Low"])
    #     CH1_F=getConfig(["SPI_CH1_Frequency"])
    #     CH2_V=getConfig(["SPI_CH2_High","SPI_CH2_Low"])
    #     CH2_F=getConfig(["SPI_CH2_Frequency"])
    #
    #     self.setSignal(ID,CH1_V,CH1_F,CH2_V,CH2_F)

        # ID=getConfig(["SL_ID"])
        # CH1_V=getConfig(["SL_CH1_High","SL_CH1_Low"])
        # CH1_F=getConfig(["SL_CH1_Frequency"])
        # CH2_V=getConfig(["SL_CH2_High","SL_CH2_Low"])
        # CH2_F=getConfig(["SL_CH2_Frequency"])
        #
        # setSignal(ID,CH1_V,CH1_F,CH2_V,CH2_F)
        #
        # print('Signal is OK')

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
        self.get_subTakingtime()
        if self.mode==3:
            self.get_lineTakingtime()
        self.cam = camera(self.telescopeCOM,self.PiCOM)

    def Signal_reflash(self):
        ######?????????????????????
        # if self.subsize == 4096:
        #     self.Signal.Recall_setup(getConfig('PI_short_mode'))
        # # if self.subsize == 4096:
        # #     self.Signal.Recall_setup(getConfig('PI_long_mode'))
        # if self.subsize == 16384:
        #     self.Signal.Recall_setup(1)
        if self.subsize == 4096:
            # self.Signal.Recall_setup(3)
            self.Signal.setCh1Time_s(self.subsize*self.pixeltime_ms)
            self.Signal.setCh2Time_s(self.subsize*self.pixeltime_ms)
        if self.subsize == 1024:
            # self.Signal.Recall_setup(3)
            self.Signal.setCh1Time_s(self.subsize * self.pixeltime_ms,user=3)
            self.Signal.setCh2Time_s(self.subsize * self.pixeltime_ms,user=4)

        if self.mode==3:
            self.Dual_line_Signal_Set()



        self.Signal.setStatusCh1('On')
        self.Signal.setStatusCh2('On')

        self.Signal.setStatusCh1('On')
        self.Signal.setStatusCh2('On')

    def Dual_line_Signal_Set(self):
        ##一次两行
        self.signal_max = getConfig('signal_max_V')
        self.linesNum=self.signal_max
        if self.linePixels==32:
            self.Signal.setCh1Time_s(2*self.subsize * self.pixeltime_ms)
            self.Signal.setHighLevelCh2(self.signal_max/self.linePixels*2)
            self.Signal.setLowLevelCh2(0)
        if self.linePixels==64:
            self.Signal.setCh1Time_s(2*self.subsize * self.pixeltime_ms)
            self.Signal.setHighLevelCh2(self.signal_max/self.linePixels*2)
            self.Signal.setLowLevelCh2(0)

    def Dual_line_Signal_reflash(self,ScanNum):
        print(self.signal_max / self.linePixels * 2* ScanNum)
        self.Signal.setHighLevelCh2(self.signal_max / self.linePixels * 2* ScanNum)
        self.Signal.setLowLevelCh2(self.signal_max / self.linePixels * (2 * ScanNum-1))


    def Set_forGui(self):
        self.get_subTakingtime()
        self.Signal_reflash()

    def take_photo(self):

        if (self.mode==0):
            self.takephotos()
        elif(self.mode==1):
            self.takeSticphoto()
        if (self.mode==2):
            self.CoAxialscan()
        elif(self.mode==3):
            self.take_line_photo()

    def takephotos(self):
        os.chdir('D:\\lidar\\program\\Telescope')
        state=self.cam.tele1.get_Direction_Precise_uRad()
        print(state)
        time.sleep(1)

        #self.cam.tele1.point_At_uRad_Precise(state[0],state[1])
        self.cam.takePhoto(self.xSubPic,self.ySubPic,self.step,self.subTakingtime)
        #self.cam.tele1.slewing_Stop()

    def takeSticphoto(self):

        os.chdir('D:\\lidar\\program\\Telescope')
        state = self.cam.tele1.get_Direction_Precise_uRad()
        print(state)
        time.sleep(1)
        while True:

            self.cam.staticPhoto(self.subTakingtime)
            #1.8

    def CoAxialscan(self):
        self.Scaner=scanMirror.scaner()
        N=M=int(math.sqrt(self.subsize))
        Scanstep=getConfig('scanstep')
        while True:
            self.cam.subPictureSignal.Send("GO")
            self.Scaner.scan(Scanstep,N,M,interval_ms=self.pixeltime_ms)


    def take_line_photo(self):
        os.chdir('D:\\lidar\\program\\Telescope')
        #self.linesNum=getConfig('linesNum')
        self.linesNum=self.linePixels
        self.scanNum=self.linesNum // 2
        state = self.cam.tele1.get_Direction_Precise_uRad()
        print(state)
        time.sleep(1)
        for i in range(self.scanNum):
            print (i)
            self.Dual_line_Signal_reflash(i+1)
            self.cam.staticPhoto(self.lineTakingtime)



    def wait_For_TDC(self):
        while self.TDC_state != "JTDC is processing":
            pass
        while self.TDC_state != "TDC Connected":
            pass
        time.sleep(2)
        print("Please open TDC tube")
        while self.TDC_state != "TDC tube is open":
            pass

    def Go(self):
        # print(self.subsize, self.pixeltime_ms,self.pixel_waittime_ms)
        # while True:

            self.folderName = ''
            self.TDC_state = ''
            ###########Open JTDC##########
            threading._start_new_thread(self.JTDCOpen, ())
            self.wait_For_TDC()
            time.sleep(2)

            keyboard = input('Check the devices and press enter to image\n')

            self.take_photo()


            # if self.TDC_state == 'Photos are over':
            #     print('waiting for the wholepicture')
            #     self.wholePic(self.folderName)


if __name__ == '__main__':

    Control=control()
    Control.Go()


        # keyboard=input('Image next photo?\n')


