import math
from MotionCom import Servotronix
import time
from Tool import *

class Tele:

    def __init__(self,com1,com2):
        self.A=Tele_Axis(com1,'A')
        self.E=Tele_Axis(com2,'E')

    def get_Direction_Precise_Deg(self):
        self.A_Pos_Deg=self.A.get_Direction_Precise_Deg()
        self.B_Pos_Deg=self.E.get_Direction_Precise_Deg()
        result = [self.A_Pos_Deg,self.B_Pos_Deg]
        print(result)
        return result

    def get_Direction_Precise_uRad(self):
        self.A_Pos_uRad = self.A.get_Direction_Precise_uRad()
        self.B_Pos_uRad = self.E.get_Direction_Precise_uRad()
        result = [self.A_Pos_uRad, self.B_Pos_uRad]
        return result

    def point_At_Deg_Precise(self, state):
        realState = [0, 0]
        realState[0] = self.A.point_At_Deg_Precise(state[0])
        realState[1] = self.E.point_At_Deg_Precise(state[1])
        return realState

    def point_At_uRad_Precise(self,state):
        realState=[0,0]
        realState[0]=self.A.point_At_uRad_Precise(state[0])
        realState[1]=self.E.point_At_uRad_Precise(state[1])
        return realState




class Tele_Axis:
    def __init__(self,com,type='A'):

        if type=='A':
            Max_count=16777216
        elif type =='E':
            Max_count=16777216
        else:
            print('Err!')
            while True:
                pass

        self.count_per_deg = 16777216/360   #count/Deg
        self.count_per_uRad = 16777216/2/math.pi/1000000  #count/urad
        self.uRad_per_Deg= 2*math.pi*1000000/360
        self.LastPos=''
        self.seri=Servotronix(com)
        self.Enable()
        self.set_Unit()

    def set_Unit(self,unit='count'):
        if unit == 'count':
            unit_val=1
        self.seri.cmd_return('UNITSROTPOS {}'.format(unit_val))

    def get_Direction_Precise_Deg(self):
        return self.get_Direction_Precise_uRad()/self.uRad_per_Deg

    def get_Direction_Precise_uRad(self):
        result = self.seri.cmd_return("PFB")
        result = float(result.split('\r\n')[1].split(' ')[0])
        return  result/self.count_per_uRad

    def point_At_Deg_Precise(self,abs_pos,speed=0.1,wait=True):
        return self.point_At_uRad_Precise(abs_pos*self.uRad_per_Deg)


    def point_At_uRad_Precise(self,abs_pos,speed=0.5,wait=True):
        print(abs_pos)
        judge = -1 if abs_pos<0 else 1
        abs=int(self.count_per_uRad*abs_pos)%(judge* 16777216) ##youcuo
        print(abs)
        cmd='MOVEABS {} {}'.format(abs,speed)
        self.seri.cmd_return(cmd)
        time.sleep(1)
        if wait:
            dif=self.wait_For_Point_At(abs_pos)
            if dif != 0:
                print('finished dif={}'.format(dif))
        return self.get_Direction_Precise_uRad()

    def is_Stopped(self):
        res=self.seri.cmd_return('STOPPED').split('\r\n')[1].split('<')[0]
        if res != '0' and res != '2':
            print("ERR! Movement is interrupted! {}".format(res))
            result = 0
        if res == '0':
            result = 0
        if res == '2':
            result = 1
        return result

    def wait_For_Point_At(self, xT, xprecision_urad=5, timeWait_s=15, time_Interval=0.5):

        state = self.get_Direction_Precise_uRad()
        xdiff = abs(diff_urad(xT, state))
        timeNow = time.time()
        timeOut = timeNow + timeWait_s
        # print('A_precision_urad={}'.format(xprecision_urad))

        while (not self.is_Stopped()):
            print(self.is_Stopped())
            time.sleep(time_Interval)

        while not (xdiff < xprecision_urad) and timeNow < timeOut:
            print(xdiff)
            time.sleep(time_Interval)
            state = self.get_Direction_Precise_uRad()
            xdiff = abs(diff_urad(xT, state))
            print('dif={}'.format(xdiff))
            timeNow = time.time()

        if timeNow > timeOut:
            print("timeOut")
            s = 0
        else:
            s = xdiff
        return s

    def Slewing_Inc(self,inc,speed=0.5):
        inc=round(inc*self.count_per_uRad)
        self.seri.cmd_return('MOVEINC {} {}'.format(inc,speed))



    def Slewing_Steps(self,level=2,time=1,speed=0.5):

        level_Dic=[1,10,50,250,1000,5000,200000,1000000]
        #          0 1  2  3   4    5    6      7
        self.seri.cmd_return('MOVEINC {} {}'.format(level_Dic[level]*2,speed))

    def Slewing_Steps_revers(self, level=2, time=1, speed=0.5):

        level_Dic = [-1, -10, -50, -250, -1000, -5000, -200000, -1000000]
        #          0 1  2  3   4    5    6      7
        self.seri.cmd_return('MOVEINC {} {}'.format(level_Dic[level] * 2, speed))

    def Enable(self):
        self.seri.cmd_return('EN')
        return 1
    def Disable(self):
        self.seri.cmd_return('K')
        return 1

    def slewing_Stop(self):
        self.seri.cmd_return("STOP")
        return 1

    # class Tele_Axis_E:

    # def wait_For_Point_At(self, xT, xprecision_urad=5, timeWait_s=15, time_Interval=1):
    #     state = self.get_Direction_Precise_uRad()
    #     xdiff = diff_urad(xT, state)
    #     timeNow = time.time()
    #     timeOut = timeNow + timeWait_s
    #     print('precision_urad={}'.format(xprecision_urad))
    #
    #     while not (((xdiff < xprecision_urad) and (ydiff < yprecision_urad)) or timeNow > timeOut):
    #         time.sleep(time_Interval)
    #         state = self.get_Direction_Precise_uRad()
    #         xdiff = abs(diff_urad(xT, state[0]))
    #         ydiff = abs(diff_urad(yT, state[1]))
    #         print(xdiff, ydiff)
    #         timeNow = time.time()
    #     if timeNow > timeOut:
    #         s = "timeOut"
    #     else:
    #         s = 1
    #     return s


    # def slewing_Varspeed_A_Up(self,time_s=1,speed=0.1):
    #     if angle>0:
    #         trackRateHigh=int((speed*4/256)%256)
    #         trackRateLow=int((speed*4)%256)
    #         command='P'+chr(3)+chr(16)+chr(6)+chr(trackRateHigh)\
    #                 +chr(trackRateLow)+chr(0)+chr(0)
    #         self.seri.Send(command)
    #         result=self.seri.res
    #         #self.seri.res=[]
    #     else:
    #         if angle<0:
    #             trackRateHigh=int((speed*4/256)%256)
    #             trackRateLow=int((speed*4)%256)
    #             command='P'+chr(3)+chr(16)+chr(7)+chr(trackRateHigh)\
    #                     +chr(trackRateLow)+chr(0)+chr(0)
    #             self.seri.Send(command)
    #             result=self.seri.res
    #             #self.seri.res=[]
    #         else:
    #             if angle==0:
    #                 self.slewing_Stop()
    #             else:
    #                 result='angle='+str(angle)
    #
    #     self.safe_Inquiry()
    #     return result
    #
    #
    # def slewing_Varspeed_A_Down(self,angle,speed):
    #     if angle>0:
    #         trackRateHigh=int((speed*4/256)%256)
    #         trackRateLow=int((speed*4)%256)
    #         command='P'+chr(3)+chr(17)+chr(6)+chr(trackRateHigh)\
    #                 +chr(trackRateLow)+chr(0)+chr(0)
    #         self.seri.Send(command)
    #         result=self.seri.res
    #         #self.seri.res=[]
    #     else:
    #         if angle<0:
    #             trackRateHigh=int((speed*4/256)%256)
    #             trackRateLow=int((speed*4)%256)
    #             command='P'+chr(3)+chr(17)+chr(7)+chr(trackRateHigh)\
    #                     +chr(trackRateLow)+chr(0)+chr(0)
    #             self.seri.Send(command)
    #             result=self.seri.res
    #             #self.seri.res=[]
    #         else:
    #             if angle==0:
    #                 self.slewing_Stop()
    #             else:
    #                 result='angle='+str(angle)
    #
    #     self.safe_Inquiry()
    #     return result

if __name__=='__main__':
    tele1=Tele('COM3','COM4')
    # print(tele1.point_At_uRad_Precise([0,1100]))
    #print(tele1.point_At_Deg_Precise([-1,-1]))
    print(tele1.A.Slewing_Steps(level=5))
    time.sleep(2)
    print(tele1.A.Slewing_Steps_revers(level=6))

    #print(tele1.get_Direction_Precise_uRad())
    time.sleep(1)
    # oringnalState=[3722.9743682546773, 554.2704018727414]
    #     #tele1.get_Direction_Precise_uRad()
    # tele1.point_At_uRad_Precise(oringnalState[0], oringnalState[1])
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






