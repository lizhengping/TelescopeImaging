import math


class wavexy:
    def __init__(self, xNum, yNum, step_urad, pixtime_ms,riseTime=0):
        self.xNum = xNum
        self.yNum = yNum
        self.step_urad = step_urad
        self.pixtime_ms = pixtime_ms
        self.Max = 10
        self.mid = 5
        self.Min = 0
        self.maxmrad = 10
        self.stepVoltage = (step_urad*14 / 1000) * (self.maxmrad / self.Max)
        self.stepTime = pixtime_ms #每一帧的时间5ms
        self.riseTime = riseTime   #每一step的riseTime
        self.startTime = 0  #每一帧开始的start time
        self.magnify = 1
        self.getPeriod()
        self.getFrequency()
        self.High1=self.stepVoltage*(self.xNum-1)
        self.High2=self.stepVoltage*(self.yNum-1)

    def getPeriod(self):
        self.period = ((self.riseTime + self.stepTime) * (self.xNum * self.yNum) + self.startTime) * self.magnify
        return self.period

    def getFrequency(self):
        self.frequency = 1000 / self.period
        return self.frequency

    def generate(self):
        w1 = []
        w2 = []
        V1 = 0
        V2 = 0

        for i in range(self.yNum):
            w2 += [i * self.stepVoltage] * (self.riseTime + self.stepTime) * self.xNum

        for j in range(self.xNum):
            w1 += [V1] * self.riseTime
            w1 += [V1] * self.stepTime
            V1 += self.stepVoltage

        c = [i for i in w1]
        c.reverse()
        w3 = w1 + c

        if (self.yNum % 2) == 0:
            w1 = w3 * int(self.yNum / 2)
        if (self.yNum % 2) == 1:
            w1 = w3 * (self.yNum / 2) + w1

        w1 = [0] * self.startTime + w1
        w2 = [0] * self.startTime + w2

        ##反向
        # w1=[x for x in w1]
        # w2=[y for y in w2]

        return [w1, w2]


if __name__ == '__main__':
    ##23urad!!!
    wave = wavexy(32, 32, 23, 5,5)
    w = wave.generate()
    print('Wave period is ' ,wave.period)
    print('Wave frequency is ',wave.frequency)
    print('High1 is ',wave.High1)
    print('High2 is ', wave.High2)

    import matplotlib.pyplot as plot
    b = [i for i in range(wave.period)]
    plot.scatter(b, w[0])
    plot.scatter(b, w[1])

    file1= open('./wave/tfw1.csv', 'w')
    for i in range(wave.period):
        file1.write(str(b[i]) + ',' + str(w[0][i])+'\n')
    file1.close()

    file2 = open('./wave/tfw2.csv', 'w')
    for i in range(wave.period):
        file2.write(str(b[i])+','+str(w[1][i])+'\n')
    file2.close()
    plot.show()

    file1 = open('./wave/tfw1.csv', 'r')
    for line in file1:
        s=file1.readline()
        print(s[:-1])
    file1.close()
