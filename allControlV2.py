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
from create_Wave import *
from takephoto import camera
# import const
# from telescope import *
from TeleMotion import *
import signal
import psutil
import scanMirror
import MotionJog
import Camera_image_save




class control:
    def __init__(self, section="default"):
        keyboard=input('Turn on the devices press enter\n')
        deviceList=self.listResources()
        self.scanMode=getConfig("scanMode")
        print(self.scanMode)
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

        self.xSubPic = getConfig(['xSubPic'])
        self.ySubPic = getConfig(['ySubPic'])
        self.lineNum = getConfig(['linePixels'])
        self.subsize = self.lineNum*self.lineNum
        self.pixeltime_ms = getConfig(['pixeltime_ms'])
        self.pixel_waittime_ms = getConfig(['pixel_waittime_ms'])
        self.IsOld=getConfig(['IsOld'])
        self.telescopeCOM_A = getConfig(['telescopeCOM_A'])  # 望远镜串口
        self.telescopeCOM_E= getConfig(['telescopeCOM_E'])
        self.PiCOM = getConfig(['PiCOM'])  # pi无线蓝牙串口
        self.SignalID = getConfig(["SPI_ID"])
        self.Signal_regularID=getConfig('SL_ID')
        self.mode = getConfig(['mode'])
        self.SPI_CH1_High = getConfig('SPI_CH1_High')
        self.SPI_CH1_Low = getConfig('SPI_CH1_Low')
        self.SPI_CH2_High = getConfig('SPI_CH2_High')
        self.SPI_CH2_Low = getConfig('SPI_CH2_Low')
        self.three_D_display=getConfig('three_D_display')
        self.G_begin=getConfig('G_begin_ns')
        self.G_end=getConfig('G_end_ns')
        self.factor=getConfig('factor')
        self.step = getConfig(['step'])


    def device_init(self):
        self.get_config()
        self.Create_Wave()
        self.CamInit()
        self.SignalInit()
        # self.powerInit()

    def Create_Wave(self):
        self.wave=[0,0]
        if self.scanMode==2:
            w = wavexy(self.lineNum,self.lineNum,1,1,0)
        if self.scanMode==1:
            w = wavexy(self.lineNum,1,1,1,0)
        self.wave[0] = w.generate()[0]
        self.wave[1] = w.generate()[1]
        # print(self.wave)


    def get_subTakingtime(self):
        if self.scanMode==2:
            self.AFG_period = self.subsize * (self.pixeltime_ms + self.pixel_waittime_ms)
            self.subTakingtime = int(self.AFG_period / 1000 + 2)
        if self.scanMode==1:
            self.AFG_period = (self.lineNum + 1) * (self.pixeltime_ms)
            self.sublinetime = self.AFG_period / 1000 + 1

        print("AFG_period should be {}s".format(self.AFG_period/1000))
        # photoTime = int(getConfig(['subsize']) * (getConfig(['pixeltime_ms']) + getConfig(['pixel_waittime_ms']))/1000)+2
        #print("subTakingtime is {}".format( self.subTakingtime))

    def JTDCOpen(self):
        os.chdir('D:\\lidar\\program\\Dataprocess\\run')
        #shell_cmd = "run.bat"  -Xmx10000M
        shell_cmd='java  -classpath ../JTDC/target/classes;xchart-2.5.1.jar;jscience-4.3.1.jar com.hydra.test.groundtdcserver.AppFrame'
        #shell_cmd=shell_cmd+' {} {} {}'.format(4096,10,0)
        ms2ps=1000000000
        shell_cmd = shell_cmd + ' {} {} {} {}'.format(self.subsize, int(self.pixeltime_ms*ms2ps), self.pixel_waittime_ms,self.scanMode)
        print(shell_cmd)
        cmd = shlex.split(shell_cmd)
        print (cmd)
        #r = subprocess.check_output(["cmd.exe", "/c", "python try.py"])
        self.p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while self.p.poll() is None:
            line = self.p.stdout.readline()
            # line=str(line,'utf8')
            print(line)
            # if "4\r\n" in line:
            #     # print("JTDC is processing")
            #     self.TDC_state="JTDC is processing"
            # if "Connected"in line:
            #     print("TDC Connected")
            #     self.TDC_state="TDC Connected"
            # if  "folderName is"in line:
            #     self.folderName=line[14:]
            #     print("folderName is "+self.folderName)
            # if "Data output Num:"in line:
            #     Num=int(line[16:-2])
            #     print(Num)
            #     if Num==self.xSubPic*self.ySubPic:
            #         self.TDC_state="Photos are over"
            #         time.sleep(3)
            #         self.kill(self.p.pid)
            # if "TDC tube is open" in line:
            #     print("TDC tube is open")
            #     self.TDC_state="TDC tube is open"
            # if "pixelsTimes" in line:
            #     self.filepath=line



    def listResources(self):
        rm = visa.ResourceManager()
        return rm.list_resources()

    def wholePic(self,path):
        #,fileFoldName,xPictures,yPictures,subsize):
        os.chdir('D:\\lidar\\program\\Plot')
        shell_cmd = "python wholePicture.py {} {} {} {} {}".format(path,self.xSubPic,self.ySubPic,self.subsize,self.scanMode)
        cmd = shlex.split(shell_cmd)
        p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while p.poll() is None:
            line = p.stdout.readline()
            line=str(line,'utf8')
            print(line)

    def depth_online(self,path,G_begin,G_end):
        #,fileFoldName,xPictures,yPictures,subsize):
        os.chdir('D:\\lidar\\program\\Plot')
        shell_cmd = "python TreeD.py {} {} {} {} {}".format("./photos/"+path[:-6]+'_sub.csv',self.lineNum,self.G_begin*1000,self.G_end*1000,self.factor)
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
        self.Signal.setHighLevelCh1(self.SPI_CH1_High)
        self.Signal.setLowLevelCh1(self.SPI_CH1_Low)
        self.Signal.setHighLevelCh2(self.SPI_CH2_High)
        self.Signal.setLowLevelCh2(self.SPI_CH2_Low)
        # self.Signal_regular=AFG3252(self.Signal_regularID)
        # self.Signal_regular.setStatusCh1('On')
        # self.Signal_regular.setStatusCh2('On')
        # self.Signal_reflash()
        self.Signal_setPiwave()
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
        self.cam = camera(self.telescopeCOM_A,self.telescopeCOM_E,self.PiCOM)


    def Signal_setPiwave(self):
        self.Signal.feed_wave(1, self.wave[0],self.IsOld)
        self.Signal.feed_wave(2, self.wave[1],self.IsOld)
        if self.scanMode == 2:
            self.Signal.setCh1WaveTime_ms(self.subsize*self.pixeltime_ms)
            self.Signal.setCh2WaveTime_ms(self.subsize*self.pixeltime_ms)
        if self.scanMode == 1:
            # self.Signal.feed_wave(2, [i for i in self.wave[1]],self.IsOld)
            self.Signal.setCh1WaveTime_ms(self.lineNum * self.pixeltime_ms)
            self.Signal.setCh2WaveTime_ms(self.lineNum * self.pixeltime_ms)
        self.Signal.setStatusCh1('On')
        self.Signal.setStatusCh2('On')



    def Set_forGui(self):
        self.get_subTakingtime()
        self.Signal_setPiwave()

    def take_photo(self):
        if self.scanMode==2:
            if (self.mode==0):
                self.takephotos()
            elif(self.mode==1):
                self.takeSticphoto()
            if (self.mode==2):
                self.CoAxialscan()
        else:
            if self.scanMode==1:
                self.lineScan()

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
            if self.three_D_display==True:
                 try:
                     self.depth_online(self.filepath,self.G_begin,self.G_end)
                 except:
                     pass
            #time.sleep(1)
            #self.depth_online(self.filepath, self.G_begin, self.G_end)
            #1.8

    def CoAxialscan(self):
        self.Scaner=scanMirror.scaner()
        N=M=int(math.sqrt(self.subsize))
        Scanstep=getConfig('scanstep')
        while True:
            self.cam.subPictureSignal.Send("1\n\r")
            self.Scaner.scan(Scanstep,N,M,interval_ms=self.pixeltime_ms)

    def line_scan_Signal_reflash(self, ScanNum):
        print(self.SPI_CH2_High / self.lineNum  * ScanNum)
        self.Signal.setLowLevelCh2(self.SPI_CH2_High / (self.lineNum-1)  * ScanNum)

    def get_all_direction(self,xNum, yNum,step_urad):
        xDelta, yDelta = self.cam.relatedDirection(xNum, yNum, step_urad)
        print(xDelta,yDelta)
        return xDelta,yDelta


    def lineScan(self):
        os.chdir('D:\\lidar\\program\\Telescope')
        state = self.cam.tele1.get_Direction_Precise_uRad()
        print(state)
        time.sleep(1)

        if self.mode == 1:
            while True:
                for lineNow in range(self.lineNum):
                    self.line_scan_Signal_reflash(lineNow)
                    self.cam.staticPhoto(self.sublinetime)

        if self.mode==0:
            xDelta, yDelta = self.get_all_direction(self.xSubPic, self.ySubPic, self.step)
            # oringnalS = self.cam.tele1.get_Direction_Precise_uRad()  # oringnalS
            S=getConfig('oringnalS')
            if S=='None':
                oringnalS = self.cam.tele1.get_Direction_Precise_uRad()
            elif len(S)==2:
                oringnalS = S
            for i in range(self.xSubPic*self.ySubPic):
                xT = oringnalS[0] + xDelta[i]
                yT = oringnalS[1] + yDelta[i]
                print(xT,yT)
                self.cam.tele1.point_At_uRad_Precise(xT,yT)
                for lineNow in range(self.lineNum):
                    self.line_scan_Signal_reflash(lineNow)
                    self.cam.staticPhoto(self.sublinetime)
            self.cam.tele1.point_At_uRad_Precise(oringnalS[0], oringnalS[1])
        #TODO next subpicture

    def wait_For_TDC(self):
        while self.TDC_state != "JTDC is processing":
            pass
        while self.TDC_state != "TDC Connected":
            pass
        time.sleep(2)
        print("Please open TDC tube")
        while self.TDC_state != "TDC tube is open":
            pass
    def wait_For_TDC_New(self):
        while self.TDC_state != "TDC tube is open":
            pass


    def Go(self):
        # print(self.subsize, self.pixeltime_ms,self.pixel_waittime_ms)
        # while True:

            self.folderName = ''
            self.TDC_state = ''
            ###########Open JTDC##########
            threading._start_new_thread(self.JTDCOpen, ())
            self.wait_For_TDC_New()
            #time.sleep(2)
            #print(self.folderName)
            # Camera_image_save.try_to_save_image(self.folderName)
            # keyboard = input('Check the devices and press enter to image\n')
            # if keyboard=='im':
            threading._start_new_thread(self.wait_for_Keyboard_cmd, ())



    def wait_for_Keyboard_cmd(self):
        self.im_alrealy=0
        a = input('Your cmd\n')
        if a == 'im':
            if self.im_alrealy == 0:
                self.im_alrealy = 1
                self.take_photo()
                self.wholePic(self.folderName)
        if a == 'M':
            threading._start_new_thread(MotionJog.show, (self.cam.tele1.A,self.cam.tele1.E,False))
            # if self.TDC_state == 'Photos are over':
            #     print('waiting for the wholepicture')


def main_run():
    Control = control()
    Control.Go()
if __name__ == '__main__':

    # Control=control()
    # Control.Go()
    main_run()
    # threading._start_new_thread(main_run,())

    # print('start')
    while True:
        pass



        # keyboard=input('Image next photo?\n')


