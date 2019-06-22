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


    def getID(self):
        return self.rm.query('*IDN?')


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
        self.rm.write("SOURce1:PULSe:PERiod "+str(period)+" ms")

    def setPeriodCh2_ms(self,period):
        self.rm.write("SOURce2:PULSe:PERiod "+str(period)+" ms")

    def getPeriodCh1(self):
        return float(self.rm.query('SOURce1:PULSe:PERiod?'))

    def setCh1WaveTime_ms(self,period,user=1):
        IsOld = self.getID()[10:15] == 'AFG30'
        self.rm.write('SOURce1:FUNCtion:SHAPe PULse')
        self.rm.write("SOURce1:PULSe:PERiod " + str(period) + " ms")
        if IsOld:
            self.rm.write('SOURce1:FUNCtion:SHAPe USER{}'.format(user))
        else:
            self.rm.write('SOURce1:FUNCtion:SHAPe EMEMory1')


    def setCh2WaveTime_ms(self,period,user=2):
        IsOld = self.getID()[10:15] == 'AFG30'
        self.rm.write('SOURce2:FUNCtion:SHAPe PULse')
        self.rm.write("SOURce2:PULSe:PERiod " + str(period) + " ms")
        if IsOld:
             self.rm.write('SOURce2:FUNCtion:SHAPe USER{}'.format(user))
        else:
             self.rm.write('SOURce2:FUNCtion:SHAPe EMEMory2')


    # def setCh1WaveTime_ms_Old(self,period,user=1):
    #     self.rm.write('SOURce1:FUNCtion:SHAPe PULse')
    #     self.rm.write("SOURce1:PULSe:PERiod " + str(period) + " ms")
    #     self.rm.write('SOURce1:FUNCtion:SHAPe USER{}'.format(user))
    #
    #
    # def setCh2WaveTime_ms_Old(self,period,user=2):
    #     self.rm.write('SOURce2:FUNCtion:SHAPe PULse')
    #     self.rm.write("SOURce2:PULSe:PERiod " + str(period) + " ms")
    #     self.rm.write('SOURce1:FUNCtion:SHAPe USER{}'.format(user))


    def setCh1Time_ms(self,period,user=1):
        self.rm.write('SOURce1:FUNCtion:SHAPe PULse')
        self.rm.write("SOURce1:PULSe:PERiod " + str(period) + " ms")
        self.rm.write('SOURce1:FUNCtion:SHAPe USER{}'.format(user))

    def setCh2Time_ms(self,period,user=2):
        self.rm.write('SOURce2:FUNCtion:SHAPe PULse')
        self.rm.write("SOURce2:PULSe:PERiod " + str(period) + " ms")
        self.rm.write('SOURce2:FUNCtion:SHAPe USER{}'.format(user))

    def setCh1Time_ms_file(self,period,filename=''):
        self.rm.write('SOURce1:FUNCtion:SHAPe PULse')
        self.rm.write("SOURce1:PULSe:PERiod " + str(period) + " ms")
        self.rm.write('SOURce1:FUNCtion:SHAPe EFILe')
        s='SOURce1:FUNCtion:EFILe "/{}.TFW"'.format(filename)
        print(s)
        self.rm.write(s)

    def setCh2Time_ms_file(self,period,filename=''):
        self.rm.write('SOURce2:FUNCtion:SHAPe PULse')
        self.rm.write("SOURce2:PULSe:PERiod " + str(period) + " ms")
        self.rm.write('SOURce2:FUNCtion:SHAPe EFILe')
        s = 'SOURce2:FUNCtion:EFILe "/{}.TFW"'.format(filename)
        print(s)
        self.rm.write(s)

    def check_Max(self):
        print(0)
        print(self.rm.query('SOURce1:VOLTage:LIMit:HIGH?'))
        print(self.rm.query('SOURce2:VOLTage:LIMit:HIGH?'))
        # self.rm.write('source2:VOLTage:LEVel:IMMediate:HIGH %.6f' % (9))
        # print(self.rm.query('SOURce2:VOLTage:LEVel:IMMediate:HIGH?'))
        # return float(self.rm.query('source2:VOLTage:LIMit:High?'))
        # return float(self.rm.query('source2:VOLTage:LIMit:High?'))
    def set_usb_wave(self):
        # print('"s"set wave {}'.format(filename))
        # print(self.rm.query('MMEMory:CATalog?'))
        # s='source1:FUNCtion:EFILe {}'.format(filename)
        # print(s)
        # self.rm.write(s)
        s = 'source1:FUNCtion:EFILe?'
        print(self.rm.query(s))

    def get_wave_Data(self):
        s='DATA? EMEMory1'
        # return self.rm.query_toBytes(s)
        return self.rm.query_toBytes(s)

    def bytes2int(tb, order='big'):
        seq=[]
        if order == 'big':
            seq = [0, 1]
        elif order == 'little':
            seq = [1, 0]
        i = 0
        for j in seq:
            i = (i << 4) + tb[j]
        return i

    def feed_wave(self,channel,waveform,IsOld=False):

        IsOld = self.getID()[10:15] == 'AFG30'
        data=bytes(0)
        for a in waveform:
            data+=int.to_bytes(a, 2, "big")
        if IsOld:
            c = 'DATA EMEMORY,#{}{}'.format(len(str(len(waveform)*2)),len(waveform)*2).encode(encoding="utf-8")
        else:
            c = 'DATA EMEMory{},#{}{}'.format(channel, len(str(len(waveform) * 2)), len(waveform) * 2).encode(
                encoding="utf-8")
        command=c + bytes(data) + b'\n'
        # print(command)
        self.rm.write_raw(command)
        time.sleep(1+0.00003*len(waveform))
        if IsOld:
            command='DATA:COPY USER{},EMEM'.format(channel)
            self.rm.write(command)
            print(command)

    # def feed_wave(self, channel, waveform):
    #     data = bytes(0)
    #     for a in waveform:
    #         data += int.to_bytes(a, 2, "big")
    #     c = 'DATA EMEMORY{},#{}{}'.format(channel,len(str(len(waveform) * 2)), len(waveform) * 2).encode(
    #         encoding="utf-8")
    #     command = c + bytes(data) + b'\n'
    #     print(command)
    #     self.rm.write_raw(command)

    def writeWavelength(self, waveform):
        data = [0]*(len(waveform)*2)
        for i in range(0, len(waveform)):
            data[i*2] = int(i*10//256)
            data[i*2+1] = (i*0 % 256)
        print(data)
        data = b'DATA EMEMory1,#42000' + bytes(data) + b'\n'
        print(data)
        self.rm.write_raw(data)
        # self.rm.write('\n')

if __name__ == '__main__':
    print(listResources())
    AFG_Aid= 'USB::0x0699::0x034A::C010293::INSTR'
    AFG_A = AFG3252(AFG_Aid)
    Model=AFG_A.getID()[10:15]
    print(Model,Model=='AFG30')
    AFG_A.setStatusCh1(0)
    print(AFG_A.getDelayCh1())
    # s = AFG_A.get_wave_Data()
    # print(type(s))
    # data = []
    # OD = s[6:-1]
    # for i in range(0, int(len(OD)/2)):
    #     data.append(int(OD[i*2])*256+ int(OD[i*2+1]))

    # AFG_A.writeWavelength([100]*1000)
    AFG_A.feed_wave(3,[1000 for i in range(130000)],True)
    # print(AFG_A.get_wave_Data())

    # print(s)
    # print(len(s))
    # AFG_A.bytes2int(s)
    # print(int(s.encode('hex'), 16))

    # print(int(s.encode('hex'), 256))
    # print(bytes.hex(s))
    # print(s(2))

    # print(int.from_bytes(AFG_A.get_wave_Data(),byteorder='big'))

    #  getDelayCh1 Tvc1.SendEndEnabled = False
    # Tvc1.WriteString("TRACE:DATA EMEMORY1,#44000")
    # Tvc1.SendEndEnabled = True
    # Tvc1.WriteByteArray(wave)
    # 'Set CH1 output parameters

    #AFG_Aid='USB0::0x0699::0x0345::C022594::INSTR'
    # AFG_Aid='USB0::0x0699::0x0345::C021385::INSTR'
    # AFG_A=AFG3252(AFG_Aid)
    # # AFG_A.set_usb_wave('"64W2.TFW"')
    # AFG_A.setCh1Time_ms_file(10000,filename='64W1')
    # AFG_A.set_usb_wave()

    # AFG_A.check_Max()
    # AFG_A.setHighLevelCh1(3)
    # AFG_A.setPeriodCh1_ms(1000)
    # AFG_A.setU(40.96)
    #print(AFG_A.getPeriodCh1())

    # AFG_A.setAmplitudeCh1(0.3)
    # time.sleep(1)
    # print(AFG_A.getAmplitudeCh1())
    # #AFG_A.setPhaseCh1(10)
    # AFG_A.setDelayCh1(20)
    # time.sleep(1)
    # print(str(AFG_A.getDelayCh1())+'ns')
    # AFG_A.setHighLevelCh1(5)
    # AFG_A.setLowLevelCh1(0)
    #
    # print(AFG_A.getHighLevelCh1())
    # AFG_A.setLowLevelCh1(-5)
    # AFG_A.setHighLevelCh1(0)
    #
    # def PMmeasureOneTime(v,pause=1):
    #
    #     if v<0:
    #         AFG_A.setDelayCh1(10)
    #         AFG_A.setHighLevelCh1(0)
    #         AFG_A.setLowLevelCh1(v)
    #     else:
    #         AFG_A.setDelayCh1(0)
    #         AFG_A.setHighLevelCh1(v)
    #         AFG_A.setLowLevelCh1(0)
    #
    #     AFG_A.setStatusCh1(1)
    #
    #     time.sleep(pause)
    #     V=v
    #
    # v=5
    # while v>=-5:
    #     PMmeasureOneTime(v)
    #     v=v-1
    #
