# from telescope import *
from TeleMotion import *
from MotionCom import *
import threading
from Tool import *
from PIL import Image,ImageGrab
# import time

class camera:
    def __init__(self, com0='COM4',com1='COM3',com2='COM5'):
        self.tele1 = Tele(com0,com1)
        self.state_deg = self.tele1.get_Direction_Precise_Deg()
        self.state_urad = self.tele1.get_Direction_Precise_uRad()
        self.running = True
        self.subPictureSignal=Servotronix(com2)


    def takePhoto(self,xNum, yNum,step_urad, photoTime,precision_urad=5):
        precision_deg=precision_urad/5   #in deg
        print(xNum, yNum,step_urad, photoTime)
        xTarget,yTarget =self.relatedDirection (xNum,yNum,step_urad)
        print(xTarget,yTarget)

        oringnalS = self.tele1.get_Direction_Precise_uRad() #oringnalS
        for i in range(xNum*yNum):
                xT=oringnalS[0] + xTarget[i]
                yT=oringnalS[1] + yTarget[i]
                self.tele1.point_At_uRad_Precise(xT,yT)
                #im = ImageGrab.grab()
                #im.save("1.png")
                print('NO.: ',i+1,' done')
                self.subPictureSignal.Send("1\n\r")
                print(self.tele1.get_Direction_Precise_uRad())
                time.sleep(photoTime)

        self.tele1.point_At_uRad_Precise(oringnalS[0],oringnalS[1])
        print(self.tele1.get_Direction_Precise_uRad())




    def staticPhoto(self,photoT):
        self.subPictureSignal.Send("1\n\r")
        time.sleep(photoT)



    def relatedDirection(self,xNum,yNum,step):
        xTarget = []
        yTarget = []
        x=[]
        V1 = 0
        V2 = 0

        for i in range(yNum):
            yTarget += [i * step] * xNum

        for j in range(xNum):
            x.append(step*j)

        r = [i for i in x]
        r.reverse()
        x2 =x + r

        if (yNum % 2) == 0:
             xTarget = x2 * int(yNum / 2)
        if (yNum % 2) == 1:
             xTarget = x2 * int(yNum / 2) + x
        # xNonCenter=int(step*(xNum-1)/2)
        xNonCenter =0
        yNonCenter = 0
        # yNonCenter = int(step * (yNum - 1) / 2)
        xTarget=[-x+xNonCenter for x in xTarget]
        yTarget=[-y+yNonCenter for y in yTarget]
        return xTarget,yTarget



def stopFun():
        while True:
            inp = input("input")
            if(inp == 'q'):
                print(inp)
                cam1.tele1.isRunning=0


if __name__ == '__main__':

    cam1 = camera('COM3',"COM5")                #望眼镜串口
    while True:
       cam1.staticPhoto(6)
    #pi无线蓝牙串口
    # while True:
    #     state = cam1.tele1.get_Direction_Precise_uRad()
    #     state1=float(input())
    #     state2=float(input())
    # state =    [6278348.1744021615-750, 6021.324000885092-1500]
    # state=[0,0]
    # [6252517.30113975, 7335.4691631630985]

    #[190869.37950435947, -105037.23721111084]  21km
    # state=[6254186.478964849, 7270.304940240222]
    # state= [129039.3926543703, -6276.363287152211] #trees
    # state=[7698.366473578427, -9661.906822915444] #trees
    # state=[283207.45789310354, -6283.85342771806] #other trees
    # state = [6253068.2009783685, 7842.92618649929] #k11
    # state =[6278267.655391078, 5910.095413482251] #jinzhong
    # state = [6263978.714233611, 4816.534890868465] #libao
    # state = [108999.89607747264, 11788.35772955965]  #dongf
    # state = [130593.59682178372, 19818.911937233428] # qizi
     # cam1.tele1.point_At_uRad_Precise(state[0]+state1, state[1]+state2)


    # state =[6277802.143154911, 145486.6178158873]   #A building
    # [6278109.238918111, 144099.44378309228]
    # state = [6187355.6997660715, 143585.24563324684]
    # [6114804.325710128, 13562.772029609006]#juminglou
    # state=[6114727.1772623, 13760.51174054739]
    # state=[6092040.665009432, 13621.569633050913]

    # state=[183700.56596878648, 148310.40080921195]#dongfangmingzu
    # state=[6185086.936188676, 142963.56396628145] #Hotel
    #state=[82667.18339714962, 146737.0967833556]#dingbiao
    # state=[157152.51174719536, 143566.5202818322]#new dingbiao 100/s
    #state=[138914.01946935582, 142947.83467109318]#new2 dingbiao 80/s weiyena

    # # state=[6276685.434184469, 146913.48959368133] #A building01
    state=[6275570.153518115, 145080.6190799887]#A new
    #146045.48165378853
    # state=[6275621.014222136, 144958.93741302332]
    #state=[6275935.434184469,146913.48959368133]#Abuilding02
    # state=[6275935.434184469,146163.48959368133]#abuliding03
    # state=[6276685.434184469,146163.48959368133]#abuliding04
    # state= [6275390.317892708, 145006.12529858816]#0808
    # state=[6275590.317892708,145406.12529858816]
    # state=[0,0]
    #
    # state = cam1.tele1.get_Direction_Precise_uRad()  # oringnalS
    # print(state)
    #
    cam1.tele1.point_At_uRad_Precise(state[0], state[1])

    # while True:
    #     state = cam1.tele1.get_Direction_Precise_uRad()  # oringnalS
    #     print(state)
    #     cam1.tele1.point_At_uRad_Precise(state[0], state[1])
    #     time.sleep(2)

    #     print(state)
    #     time.sleep(1)

    # #state=[4755783.484259957, 504892.399206446]
    # state = [5709636.032504409, 61210.92673222186]

    # time.sleep(1)
    # state[0] +=0
    # state[1] +=0
    #
    #
    # threading._start_new_thread(stopFun,())
    #cam1.takePhoto(5, 5,700, 12)
    # for i in range(5):
    # while True:
    #     pass
    #     cam1.staticPhoto(12)
        #cam1.staticPhoto(12)
