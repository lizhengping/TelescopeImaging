__author__ = 'Benli'
__version__ = 'v1.0.20160105'

import sys
sys.path.append('devicelib')
import visa
from SCPI import SCPI
from InstrumentServers import InstrumentServer
from Instruments import DeviceException,VISAInstrument
from Utils import SingleThreadProcessor
import math



class IT6322(VISAInstrument):
    manufacturer = 'ITECH Ltd.'
    model = 'IT6322'

    def __init__(self, resourceID):
        super().__init__(resourceID, 3)
        self.__remote()
        self.voltageSetpoints = self.getVoltageSetpoints()
        self.currentLimits = self.getCurrentLimits()
        self.outputStatuses = self.getOutputStatuses()

    def getIdentity(self):
        idn = self.scpi._IDN.query()
        if idn is None:
            return [''] * 4
        if len(idn) is 0:
            return [''] * 4
        idns = idn.split(',')
        idns = [idn.strip(' ') for idn in idns]
        while len(idns) < 4:
            idns.append('')
        return idns[:4]

    def getVersion(self):
        return self.scpi.SYSTem.VERSion.query()

    def beeper(self):
        self.scpi.SYSTem.BEEPer.write()
        self.getIdentity()


    def measureVoltages(self):
        voltageString = self.scpi.MEAS.VOLT.ALL.query().split(', ')
        voltages = [float(vs) for vs in voltageString]
        return voltages

    def measureCurrents(self):
        currentString = self.scpi.MEAS.CURR.ALL.query().split(', ')
        currents = [float(vs) for vs in currentString]
        return currents

    def getVoltageSetpoints(self):
        vs = self.scpi.APP.VOLT.query()
        vs = vs.split(', ')
        self.voltageSetpoints = [float(v) for v in vs]
        return self.voltageSetpoints

    def getCurrentLimits(self):
        cs = self.scpi.APP.CURR.query()
        cs = cs.split(', ')
        self.currentLimits = [float(v) for v in cs]
        return self.currentLimits

    def setVoltages(self, voltages):
        if len(voltages) is not self.channelCount:
            raise DeviceException('Length of voltages do not match the channel number.')
        outputCodeString = ['{}'.format(v) for v in voltages]
        outputCode = ', '.join(outputCodeString)
        self.scpi.APP.VOLT.write(outputCode)
        setted = self.getVoltageSetpoints()
        same = [math.fabs(voltages[i]-setted[i])<0.001  for i in range(self.channelCount)]
        if sum(same) is not self.channelCount:
            raise DeviceException('Voltage out of range.')

    def setVoltage(self, channel, voltage):
        self.checkChannel(channel)
        voltages = self.voltageSetpoints.copy()
        voltages[channel] = voltage
        self.setVoltages(voltages)

    def setCurrentLimits(self, currents):
        if len(currents) is not self.channelCount:
            raise DeviceException('Length of currents do not match the channel number.')
        outputCodeString = ['{}'.format(v) for v in currents]
        outputCode = ', '.join(outputCodeString)
        self.scpi.APP.CURR.write(outputCode)
        setted = self.getCurrentLimits()
        same = [math.fabs(currents[i]-setted[i])<0.001  for i in range(self.channelCount)]
        if sum(same) is not self.channelCount:
            raise DeviceException('Current out of range.')

    def setCurrentLimit(self, channel, currentLimit):
        self.checkChannel(channel)
        currentLimits = self.currentLimits.copy()
        currentLimits[channel] = currentLimit
        self.setCurrentLimits(currentLimits)

    def getOutputStatuses(self):
        os = self.scpi.APP.OUT.query()
        os = os.split(', ')
        self.outputStatuses = [o == '1' for o in os]
        return self.outputStatuses

    def setOutputStatuses(self, outputStatuses):
        if len(outputStatuses) is not self.channelCount:
            raise DeviceException('Length of outputStatuses do not match the channel number.')
        outputCodeString = ['{}'.format(1 if v else 0) for v in outputStatuses]
        outputCode = ', '.join(outputCodeString)
        self.scpi.APP.OUT.write(outputCode)
        setted = self.getOutputStatuses()
        same = [outputStatuses[i]==setted[i] for i in range(self.channelCount)]
        if sum(same) is not self.channelCount:
            raise DeviceException('OutputStatus error.')

    def setOutputStatus(self, channel, outputStatus):
        self.checkChannel(channel)
        outputStatuses = self.outputStatuses.copy()
        outputStatuses[channel] = outputStatus
        self.setOutputStatuses(outputStatuses)

    def reset(self):
        self.scpi._RST.write()

    def __remote(self):
        return self.scpi.SYSTem.REMote.write()


if __name__ == '__main__':
    print('BKPrecision_IT6322')
    pm = IT6322('ASRL12::INSTR')
    print(pm.getIdentity())
    pm.setVoltage(0,2)
    #pm.setOutputStatuses([False]*3)
    #pm.beeper()
    print(pm.getVoltageSetpoints())
    pm.setOutputStatuses([True,True,False])
    print(pm.measureVoltages())
    import time
    time.sleep(1000)

