from telescope import *
import threading
from Tool import *
from PIL import Image,ImageGrab
# import time

class camera:
    def __init__(self, com0='COM2',com1='COM9'):
        self.tele1 = Tele(com0)
        self.state_deg = self.tele1.get_Direction_Precise()
        self.state_urad = self.tele1.get_Direction_Precise_uRad()
        self.running = True
        self.subPictureSignal=TeleSerial(com1)


    def takePhoto(self,xNum, yNum,step_urad, photoTime,precision_urad=5):
        precision_deg=precision_urad/5   #in deg

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
                self.subPictureSignal.Send("GO")
                print(self.tele1.get_Direction_Precise_uRad())
                time.sleep(photoTime)

        self.tele1.point_At_uRad_Precise(oringnalS[0],oringnalS[1])
        print(self.tele1.get_Direction_Precise_uRad())

    def staticPhoto(self,photoT):
        self.subPictureSignal.Send("GO")
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
        xTarget=[-x for x in xTarget]
        yTarget=[-y for y in yTarget]
        return xTarget,yTarget



def stopFun():
        while True:
            inp = input("input")
            if(inp == 'q'):
                print(inp)
                cam1.tele1.isRunning=0


if __name__ == '__main__':

    cam1 = camera('COM7')                #望眼镜串口
    #pi无线蓝牙串口

    #state= cam1.tele1.get_Direction_Precise_uRad() #oringnalS
    #state=[217214.07640958784, -1887.8899296219522]
    state=[5631595.883441811, -17640.030046628286]
    print(state)
    time.sleep(1)
    state[0] +=0
    state[1] +=0
    cam1.tele1.point_At_uRad_Precise(state[0],state[1])

    threading._start_new_thread(stopFun,())
    cam1.takePhoto(5, 5,700, 12)
    # for i in range(5):
   # while True:
        #cam1.staticPhoto(12)

    cam1.tele1.slewing_Stop()

