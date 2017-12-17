import visa
import sys
import time

def listResources():
    rm = visa.ResourceManager()
    return rm.list_resources()

class AFG3252:
    def __init__(self,id):
        self.id = id
        self.rm = visa.ResourceManager().open_resource(id)

    def setStatusCh1(self, state='Off'):
        if state=='On' or state==1:
            state_bit=1
        else:
            state_bit=0

        self.rm.write('output1:state '+str(state_bit))

    def getAmplitudeCh1(self):
        return float(self.rm.query('source1:voltage:level:immediate:amplitude?'))


    def setAmplitudeCh1(self, amplitude=0.1):
        self.rm.write('source1:voltage:level:immediate:amplitude %.6f' % (amplitude))

    def getPhaseCh1(self):
        return float(self.rm.query('source1:phase?'))

    def setPhaseCh1(self, phase=0.0):
        self.rm.write('source1:phase:adjust %.6f' % (phase))

    def setDelayCh1(self,delay):
        self.rm.write('SOURce1:PULSe:DELay %.6fns' %(delay))

    def getDelayCh1(self):
        return  float(self.rm.query('SOURce1:PULSe:DELay?'))*1000000000

    def setHighLevelCh1(self,High):
        self.rm.write('source1:VOLTage:LEVel:IMMediate:HIGH %.6f' % (High))

    def getHighLevelCh1(self):
        return float(self.rm.query('SOURce1:VOLTage:LEVel:IMMediate:HIGH?'))

    def setLowLevelCh1(self,Low):
        self.rm.write('source1:VOLTage:LEVel:IMMediate:Low %.6f' % (Low))

    def getLowLevelCh1(self):
        return float(self.rm.query('SOURce1:VOLTage:LEVel:IMMediate:Low?'))



    def setStatusCh2(self, state='Off'):
        if state=='On' or state==1:
            state_bit=1
        else:
            state_bit=0

        self.rm.write('output2:state '+str(state_bit))

    def getAmplitudeCh2(self):
        return float(self.rm.query('source2:voltage:level:immediate:amplitude?'))


    def setAmplitudeCh2(self, amplitude=0.1):
        self.rm.write('source2:voltage:level:immediate:amplitude %.6f' % (amplitude))

    def getPhaseCh2(self):
        return float(self.rm.query('source2:phase?'))

    def setPhaseCh2(self, phase=0.0):
        self.rm.write('source2:phase:adjust %.6f' % (phase))

    def setDelayCh2(self,delay):
        self.rm.write('SOURce2:PULSe:DELay %.6fns' %(delay))

    def getDelayCh2(self):
        return  float(self.rm.query('SOURce2:PULSe:DELay?'))*1000000000

    def setHighLevelCh2(self,High):
        self.rm.write('source2:VOLTage:LEVel:IMMediate:HIGH %.6f' % (High))

    def getHighLevelCh2(self):
        return float(self.rm.query('SOURce2:VOLTage:LEVel:IMMediate:HIGH?'))

    def setLowLevelCh2(self,Low):
        self.rm.write('source2:VOLTage:LEVel:IMMediate:Low %.6f' % (Low))

    def getLowLevelCh2(self):
        return float(self.rm.query('SOURce2:VOLTage:LEVel:IMMediate:Low?'))

    #Recall instrument setting from setup memory
    def Recall_setup(self,setup_Num=0):
        self.rm.write('*RCL %s' % (setup_Num))

    def setFrequencyCh1_Hz(self,frequency=1):
        self.rm.write("SOURCE1:FREQUENCY "+str(frequency))

    def setFrequencyCh2_Hz(self,frequency):
        self.rm.write("SOURCE2:FREQUENCY "+str(frequency))

    def setPeriodCh1_ms(self,period):
        self.rm.write("SOURce1:PULSe:PERiod "+str(period)+"ms")

    def setPeriodCh2_ms(self,period):
        self.rm.write("SOURce2:PULSe:PERiod "+str(period)+"ms")





if __name__ == '__main__':
    print(listResources())
    #AFG_Aid='USB0::0x0699::0x0345::C022594::INSTR'
    AFG_Aid='USB0::0x0699::0x0345::C021385::INSTR'
    AFG_A=AFG3252(AFG_Aid)
    AFG_A.setAmplitudeCh1(0.3)
    time.sleep(1)
    print(AFG_A.getAmplitudeCh1())
    #AFG_A.setPhaseCh1(10)
    AFG_A.setDelayCh1(20)
    time.sleep(1)
    print(str(AFG_A.getDelayCh1())+'ns')
    AFG_A.setHighLevelCh1(5)
    AFG_A.setLowLevelCh1(0)

    print(AFG_A.getHighLevelCh1())
    AFG_A.setLowLevelCh1(-5)
    AFG_A.setHighLevelCh1(0)

    def PMmeasureOneTime(v,pause=1):

        if v<0:
            AFG_A.setDelayCh1(10)
            AFG_A.setHighLevelCh1(0)
            AFG_A.setLowLevelCh1(v)
        else:
            AFG_A.setDelayCh1(0)
            AFG_A.setHighLevelCh1(v)
            AFG_A.setLowLevelCh1(0)

        AFG_A.setStatusCh1(1)

        time.sleep(pause)
        V=v

    v=5
    while v>=-5:
        PMmeasureOneTime(v)
        v=v-1

