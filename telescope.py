import math
from Telecom import TeleSerial
import time
import random
from Tool import *
class Tele:
    def __init__(self,com):
        self.A=''
        self.E=''
        self.state=[self.A,self.E]
        self.seri=TeleSerial(com)
        self.offTraking()
        self.isRunning=1

    def safe_Inquiry(self):
        if self.isRunning ==0:
            self.slewing_Stop()
            print("End q")
            exit(0)


    def get_Direction_Normal(self):
        self.seri.Send("Z")
        time.sleep(0.05)
        result=self.seri.res
        #self.seri.res=[]
        return result

    def get_Direction_Normal_uRad(self):
        return  [ x/360*2*math.pi*1000000 for x in self.get_Direction_Normal()]

    def get_Direction_Precise(self):
        self.seri.Send("z")
        time.sleep(0.05)
        result=self.seri.res
        #print(result)
        #self.seri.res=[]
        return result

    def get_Direction_Precise_uRad(self):
        const = 1/360 * 2 * math.pi * 1000000
        result = self.get_Direction_Precise()
        #print(result)

        while result == 'action':
            result = self.get_Direction_Precise()
            #print('precise',result)


        return  [i*const for i in result]

    def point_At_Deg_Normal(self,A,E):
        A=int(A*65536/360)%65536
        E=int(E*65536/360)%65536
        HexA=str(hex(A))[2:].zfill(4)
        HexE=str(hex(E))[2:].zfill(4)
        state=('B'+HexA+','+HexE+'#')
        #print('goto'+state)
        self.seri.Send(state)
        result=self.seri.res
        #self.seri.res=[]
        return result

    def point_At_Deg_Precise(self,A,E):
        A=int(A*16777216/360)%16777216
        E=int(E*16777216/360)%16777216
        HexA=str(hex(A))[2:].zfill(6)
        HexE=str(hex(E))[2:].zfill(6)
        state=('b'+HexA+'00,'+HexE+'00#')
        #print('goto'+state)
        self.seri.Send(state)
        result=self.seri.res
        #self.seri.res=[]
        return result

    def point_At_Rad_Normal(self,A,E):
        A=int(A*65536/2/math.pi)%65536
        E=int(E*65536/2/math.pi)%65536
        HexA=str(hex(A))[2:].zfill(4)
        HexE=str(hex(E))[2:].zfill(4)
        state=('B'+HexA+','+HexE+'#')
        #print('goto'+state)
        self.seri.Send(state)
        result=self.seri.res
        #self.seri.res=[]
        return result


    def point_At_uRad_Precise(self,A,E,wait=True):
        oringnalS=[A,E]
        A=int(A*16777216/2/math.pi/1000000)%16777216
        E=int(E*16777216/2/math.pi/1000000)%16777216
        HexA=str(hex(A))[2:].zfill(6)
        HexE=str(hex(E))[2:].zfill(6)
        state=('b'+HexA+'00,'+HexE+'00#')
        #print('goto'+state)
        self.seri.Send(state)
        result=self.seri.res
        #self.seri.res=[]
        time.sleep(1)
        if wait:
            self.wait_For_Point_At(oringnalS[0],oringnalS[1])
        return result

    def wait_For_Point_At(self,xT,yT,xprecision_urad=50,yprecision_urad=30,timeWait=15,time_Interval=1):
         state=self.get_Direction_Precise_uRad()
         xdiff=diff_urad(xT,state[0] )
         ydiff=diff_urad(yT,state[1] )
         timeNow=time.time()
         timeOut=timeNow+timeWait
         print(xprecision_urad,yprecision_urad)

         while  not ( ((xdiff < xprecision_urad) and (ydiff< yprecision_urad ) )or  timeNow>timeOut):
              time.sleep(time_Interval)
              state=self.get_Direction_Precise_uRad()
              xdiff=abs(diff_urad(xT,state[0]))
              ydiff=abs(diff_urad(yT,state[1]))
              print(xdiff,ydiff)
              timeNow=time.time()
         if timeNow>timeOut :
            s = "timeOut"
         else:
             s="1"
         return s


    def slewing_Varspeed_A(self,angle,speed):
        if angle>0:
            trackRateHigh=int((speed*4/256)%256)
            trackRateLow=int((speed*4)%256)
            command='P'+chr(3)+chr(16)+chr(6)+chr(trackRateHigh)\
                    +chr(trackRateLow)+chr(0)+chr(0)
            self.seri.Send(command)
            result=self.seri.res
            #self.seri.res=[]
        else:
            if angle<0:
                trackRateHigh=int((speed*4/256)%256)
                trackRateLow=int((speed*4)%256)
                command='P'+chr(3)+chr(16)+chr(7)+chr(trackRateHigh)\
                        +chr(trackRateLow)+chr(0)+chr(0)
                self.seri.Send(command)
                result=self.seri.res
                #self.seri.res=[]
            else:
                if angle==0:
                    self.slewing_Stop()
                else:
                    result='angle='+str(angle)

        self.safe_Inquiry()
        return result


    def slewing_Varspeed_E(self,angle,speed):
        if angle>0:
            trackRateHigh=int((speed*4/256)%256)
            trackRateLow=int((speed*4)%256)
            command='P'+chr(3)+chr(17)+chr(6)+chr(trackRateHigh)\
                    +chr(trackRateLow)+chr(0)+chr(0)
            self.seri.Send(command)
            result=self.seri.res
            #self.seri.res=[]
        else:
            if angle<0:
                trackRateHigh=int((speed*4/256)%256)
                trackRateLow=int((speed*4)%256)
                command='P'+chr(3)+chr(17)+chr(7)+chr(trackRateHigh)\
                        +chr(trackRateLow)+chr(0)+chr(0)
                self.seri.Send(command)
                result=self.seri.res
                #self.seri.res=[]
            else:
                if angle==0:
                    self.slewing_Stop()
                else:
                    result='angle='+str(angle)

        self.safe_Inquiry()
        return result

    def slewing_Fixedspeed_A(self,angle,rate):
        if rate<9:
            rate=int(rate)
            if angle>0:
                command='P'+chr(3)+chr(16)+chr(36)+chr(rate)\
                        +chr(0)+chr(0)+chr(0)
                self.seri.Send(command)
                result=self.seri.res
                #self.seri.res=[]
            else:
                if angle<0:
                    command='P'+chr(3)+chr(16)+chr(37)+chr(rate)\
                            +chr(0)+chr(0)+chr(0)
                    self.seri.Send(command)
                    result=self.seri.res
                    #self.seri.res=[]
                else:
                    if angle==0:
                        self.slewing_Stop()
                    else:
                        result='angle='+str(angle)
        else:
            result='rate='+rate

        self.safe_Inquiry()
        return result

    def slewing_Fixedspeed_E(self,angle,rate):
        if rate<9:
            rate=int(rate)
            if angle>0:
                command='P'+chr(3)+chr(17)+chr(36)+chr(rate)\
                        +chr(0)+chr(0)+chr(0)
                self.seri.Send(command)
                result=self.seri.res
                #self.seri.res=[]
            else:
                if angle<0:
                    command='P'+chr(3)+chr(17)+chr(37)+chr(rate)\
                            +chr(0)+chr(0)+chr(0)
                    self.seri.Send(command)
                    result=self.seri.res
                    #self.seri.res=[]
                else:
                    if angle==0:
                        self.slewing_Stop()
                    else:
                        result='angle='+str(angle)
        else:
            result='rate='+rate

        self.safe_Inquiry()
        return result


    def slewing_Stop(self):
        command=""

        command='P'+chr(3)+chr(16)+chr(6)+chr(0)\
                        +chr(0)+chr(0)+chr(0)
        self.seri.Send(command)

        command='P'+chr(3)+chr(17)+chr(6)+chr(0)\
                        +chr(0)+chr(0)+chr(0)
        self.seri.Send(command)

        command='P'+chr(3)+chr(16)+chr(36)+chr(0)\
                        +chr(0)+chr(0)+chr(0)
        self.seri.Send(command)

        command='P'+chr(3)+chr(17)+chr(36)+chr(0)\
                        +chr(0)+chr(0)+chr(0)
        self.seri.Send(command)


        #self.slewing_Varspeed_A(1,0)
        #self.slewing_Varspeed_E(1,0)
        #self.slewing_Fixedspeed_A(1,0)
        #self.slewing_Fixedspeed_E(1,0)
        result=self.seri.res
        print('safe')
        #self.seri.res=[]
        return result

    def A__urad_Cancelerror(self,destination,single_Direction=False,precision_urad=5):
        precision_deg=precision_urad/5
        speed=300
        count=0
        diff=0
        twoPi_urad=2 * math.pi * 1000000
        Pi_urad=math.pi * 1000000
        state=self.get_Direction_Precise_uRad()
        diff=(destination-state[0])
        if abs(diff)>Pi_urad:
           diff=(twoPi_urad-abs(diff))*(-1 if diff > 0 else 1)
        speed_deg=diff/3.5
        if (speed_deg>100000):
            self.point_At_uRad_Precise(destination,state[1])
        else:
            if (single_Direction==False):
                self.A_move_urad(destination-1000,300)


            state=self.get_Direction_Precise_uRad()
            diff=(destination-state[0])
            if abs(diff)>Pi_urad:
                diff=(twoPi_urad-abs(diff))*(-1 if diff > 0 else 1)
                #print(diff)
            speed_deg=(diff/5)

            while (speed_deg>precision_deg):
                gotime=0.35
                self.slewing_Varspeed_A(1,speed_deg)
                if speed_deg<50:
                    gotime=0.2
                time.sleep(gotime)
                state=self.get_Direction_Precise_uRad()
                diff=(destination-state[0])
                if abs(diff)>Pi_urad:
                    diff=(twoPi_urad-abs(diff))*(-1 if diff > 0 else 1)
                speed_deg=(diff/5)
                print(speed_deg)
                if (speed_deg < -precision_deg):
                    self.slewing_Varspeed_A(-1,1000)
                    time.sleep(0.5)
                    state=self.get_Direction_Precise_uRad()
                    diff=(destination-state[0])
                    if abs(diff)>Pi_urad:
                         diff=(twoPi_urad-abs(diff))*(-1 if diff > 0 else 1)
                    speed_deg=(diff/5)
                    #如果还是没有往回转
                    while speed_deg<precision_deg:
                        self.slewing_Varspeed_A(-1,1000)
                        time.sleep(0.5)
                        state=self.get_Direction_Precise_uRad()
                        diff=(destination-state[0])
                        if abs(diff)>Pi_urad:
                            diff=(twoPi_urad-abs(diff))*(-1 if diff > 0 else 1)
                        #print(diff)
                        speed_deg=(diff/5)
                    print(speed_deg)
            self.slewing_Stop()

    def E__urad_Cancelerror(self,destination,single_Direction=False,precision_urad=5):
        precision_deg=precision_urad/5
        speed=300
        count=0
        diff=0
        twoPi_urad=2 * math.pi * 1000000
        Pi_urad=math.pi * 1000000
        state=self.get_Direction_Precise_uRad()
        diff=(destination-state[1])
        if abs(diff)>Pi_urad:
           diff=(twoPi_urad-abs(diff))*(-1 if diff > 0 else 1)
        speed_deg=diff/3.5
        if (speed_deg>100000):
            self.point_At_uRad_Precise(state[0],destination)
        else:
            if (single_Direction==False):
                self.E_move_urad(destination-500,150)


            state=self.get_Direction_Precise_uRad()
            diff=(destination-state[1])
            if abs(diff)>Pi_urad:
                    diff=(twoPi_urad-abs(diff))*(-1 if diff > 0 else 1)
                #print(diff)
            speed_deg=(diff/5)

            while (speed_deg>precision_deg):
                gotime=0.2
                self.slewing_Varspeed_E(1,speed_deg)
                if speed_deg<50:
                    gotime=0.2
                time.sleep(gotime)
                state=self.get_Direction_Precise_uRad()
                diff=(destination-state[1])
                if abs(diff)>Pi_urad:
                    diff=(twoPi_urad-abs(diff))*(-1 if diff > 0 else 1)
                speed_deg=(diff/5)
                print(speed_deg)
                #如果过了
                if (speed_deg < -precision_deg):
                    self.slewing_Varspeed_E(-1,500)
                    time.sleep(0.5)
                    state=self.get_Direction_Precise_uRad()
                    diff=(destination-state[1])
                    if abs(diff)>Pi_urad:
                        diff=(twoPi_urad-abs(diff))*(-1 if diff > 0 else 1)
                    #print(diff)
                    speed_deg=(diff/5)
                    #如果还是没有往回转
                    while speed_deg<precision_deg:
                        self.slewing_Varspeed_E(-1,500)
                        time.sleep(0.5)
                        state=self.get_Direction_Precise_uRad()
                        diff=(destination-state[1])
                        if abs(diff)>Pi_urad:
                            diff=(twoPi_urad-abs(diff))*(-1 if diff > 0 else 1)
                        #print(diff)
                        speed_deg=(diff/5)

                    print(speed_deg)
            self.slewing_Stop()














    def A_move_urad (self,destination,precision_urad=300):
       precision_deg=precision_urad/5
       speed=400
       count=0
       diff=0
       twoPi_urad=2 * math.pi * 1000000
       Pi_urad=math.pi * 1000000
       while abs(speed)>precision_deg:
            gotime =0.35
            count=count+1
            state=self.get_Direction_Precise_uRad()
            # print('state is ',state[0])
            diff=(destination-state[0])
            if abs(diff)>Pi_urad:
                diff=(twoPi_urad-abs(diff))*(-1 if diff > 0 else 1)
                #print(diff)
            speed=(diff/3.5)
            if abs(speed)>10000:
                gotime=abs(speed/10000)*0.4
                if speed<0:
                    speed=-10000
                else:
                    speed=10000
            if speed>0:
                self.slewing_Varspeed_A(1,abs(speed))
                time.sleep(gotime)
            if speed<0:
                self.slewing_Varspeed_A(-1,abs(speed))
                time.sleep(gotime)

            #print(gotime)
            #print('speed is',speed*2.5)
       self.slewing_Stop()
       return 'Done!'+str(count)+'  '+str(count*gotime)

    def E_move_urad (self,destination,precision_urad=300):
       precision_deg=precision_urad/5
       twoPi_urad = 2 * math.pi * 1000000
       Pi_urad = math.pi * 1000000
       QPi_urad = twoPi_urad/4
       speed = 300
       count = 0
       diff = 0
       if abs(destination) < Pi_urad:
           while abs(speed)>precision_deg:
                gotime =0.35
                count=count+1
                state=self.get_Direction_Precise_uRad()
                #print('state is ',state[1])
                diff=(destination-state[1])
                if abs(diff)>Pi_urad:
                    diff=(twoPi_urad-abs(diff))*(-1 if diff > 0 else 1)
                    #print(diff)
                speed=(diff/3.5)
                if abs(speed)>5000:
                    gotime=abs(speed/5000)*0.4
                    if speed<0:
                        speed=-5000
                    else:
                        speed=5000
                if speed>0:
                    self.slewing_Varspeed_E(1,abs(speed))
                    time.sleep(gotime)
                if speed<0:
                    self.slewing_Varspeed_E(-1,abs(speed))
                    time.sleep(gotime)

                #print(gotime)
                #print('speed is',speed*2.5)
           self.slewing_Stop()
           return 'Done!'+str(count)+'  '+str(count*gotime)

    def offTraking(self):
        self.seri.res=''
        while self.seri.res!='action':
            self.seri.Send('T'+chr(0))
            time.sleep(0.05)




if __name__=='__main__':
    tele1=Tele('COM3')
    print(tele1.get_Direction_Precise_uRad())
    time.sleep(1)
    oringnalState=[3722.9743682546773, 554.2704018727414]
        #tele1.get_Direction_Precise_uRad()
    tele1.point_At_uRad_Precise(oringnalState[0], oringnalState[1])
    # tele1.point_At_uRad_Precise(oringnalState[0]+500000,oringnalState[1]+5000)
    #tele1.point_At_uRad_Precise( 25939.105793587714, 8015.199419513791)
    # while False:
    #         #dalte=random.randrange(-1000,1000)
    #         tele1.point_At_uRad_Precise(oringnalState[0],oringnalState[1])
    #         time.sleep(10)
    #         dalte=1000
    #         tele1.point_At_uRad_Precise(oringnalState[0]+dalte,oringnalState[1]+dalte)
    #         time.sleep(10)
    #         dalte=2000
    #         tele1.point_At_uRad_Precise(oringnalState[0]+dalte,oringnalState[1]+dalte)
    #         time.sleep(10)
    #         dalte=3000
    #         tele1.point_At_uRad_Precise(oringnalState[0]+dalte,oringnalState[1]+dalte)
    #         time.sleep(10)
    # while False:
    #     tele1.point_At_uRad_Precise(oringnalState[0],oringnalState[1])
    #     time.sleep(10)
    #     print("o")
    #     #delta= random.randint(-1000, 1000)
    #     tele1.A__urad_Cancelerror(oringnalState[0])
    #     tele1.E__urad_Cancelerror(oringnalState[1])
    #     dalte=1000
    #     tele1.A__urad_Cancelerror(oringnalState[0]+dalte)
    #     print("A")
    #     tele1.E__urad_Cancelerror(oringnalState[1]+dalte)
    #     print("E")
    #     time.sleep(10)
    #     dalte=2000
    #     tele1.A__urad_Cancelerror(oringnalState[0]+dalte)
    #     print("A")
    #     tele1.E__urad_Cancelerror(oringnalState[1]+dalte)
    #     print("E")
    #     time.sleep(10)
    #     dalte=3000
    #     tele1.A__urad_Cancelerror(oringnalState[0]+dalte)
    #     print("A")
    #     tele1.E__urad_Cancelerror(oringnalState[1]+dalte)
    #     print("E")
    #     time.sleep(10)
    #     dalte=4000
    #     tele1.A__urad_Cancelerror(oringnalState[0]+dalte)
    #     print("A")
    #     tele1.E__urad_Cancelerror(oringnalState[1]+dalte)
    #     print("E")
    #     time.sleep(10)


    #while True:

        # tele1.A_move_urad(oringnalState[0])
        # tele1.E_move_urad(oringnalState[1])
        # time.sleep(5)
        #
        # state=tele1.get_Direction_Precise_uRad()
        #
        # print(state)
        #
        #delta= random.randint(-3000, 3000)
        # tele1.point_At_uRad_Precise(oringnalState[0],oringnalState[1])
        # time.sleep(10)
        # tele1.A_move_urad(oringnalState[0]+10000)
        # time.sleep(5)
        # tele1.A_move_urad(state[0]+delta)
        # time.sleep(5)
        # tele1.A_move_urad(state[0])
        # time.sleep(5)
        # tele1.A_move_urad(state[0]+delta)
        # time.sleep(5)
        #
        # state=tele1.get_Direction_Precise_uRad()
        # print(state)

    #tele1.E_move_urad(-10000)






