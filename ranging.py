import sys
# sys.path.append('../Plot')
# import repid_range
# import string
# import configControl
from allControl import *

# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication , QMainWindow,QMessageBox
from  ranging_GUI import *
import sys




class ranging_Window(QMainWindow, Ui_MainWindow):

    _signal = QtCore.pyqtSignal(str)  # 定义信号,定义参数为str类型

    def __init__(self, parent=None):
        super(ranging_Window, self).__init__(parent)
        self.setupUi(self)
        self. fun_connect()
        self.listResources()
        self.integral_time_s=2
        self.J_Go()
        self.Signal_init()
        # threading._start_new_thread(self.calculate_range,())

    def fun_connect(self):
        self.pushButton.clicked.connect(self.connect)
        self.pushButton_2.clicked.connect(self.Measure1)
        self.pushButton_3.clicked.connect(self.Measure2)
        self.pushButton_4.clicked.connect(self.Measure3)
        # self.pushButton_5.clicked.connect(self.Measure4)
        self.pushButton_7.clicked.connect(self.calculate_range)
        self.pushButton_6.clicked.connect(self.AutoMeasure)
        # self.pushButton_7.clicked.connect(self.close)

    def connect(self):
        # 'USB0::0xFFFF::0x6300::602071010707420029::INSTR'
        id1=self.comboBox.currentText()
        id2=self.comboBox_2.currentText()
        self.Period_Index=5
        try:
            if id1 != '':
                self.AFG1=AFG3252(id1)
                print(self.AFG1.getID())
            if id2 != '':
                self.AFG2=AFG3252(id2)
                print(self.AFG2.getID())
        except:
            print('Open Erro!')
        # print('ad1',self.AFG1.getID())
        # print('ad2',self.AFG2.getID())
        # self.AFG=AFG3252(self.comboBox.currentText())

    def listResources(self):
        rm = visa.ResourceManager()
        com_devices=list(rm.list_resources())
        for i in com_devices:
             self.comboBox.addItem(i)
             self.comboBox_2.addItem(i)
        return

    # def Measure1(self):
    #     pass
        # self.AFG.setPeriodCh1_ms(0.011)
        # self.AFG.setPeriodCh2_ms(0.011)
        # self.AFG.setStatusCh1(1)
        # self.AFG.setStatusCh1(1)

    def Measure1(self):
        self.Measure_Period(float(self.lineEdit.text()),0)
        self.Period_Index=0
    def Measure2(self):
        self.Measure_Period(float(self.lineEdit_2.text()),1)
        self.Period_Index = 1
    def Measure3(self):
        self.Measure_Period(float(self.lineEdit_3.text()),2)
        self.Period_Index = 2
    def Measure4(self):
        self.Measure_Period(float(self.lineEdit_4.text()),3)
        self.Period_Index = 3

    def AutoMeasure(self):
        self.Measure1()
        time.sleep(self.integral_time_s+0.5)
        self.Measure2()
        time.sleep(self.integral_time_s + 0.5)
        self.Measure3()
        time.sleep(self.integral_time_s + 0.5)
        self.calculate_range()

    def Measure_Period(self,Period_us,Index):
        if self.Period_Index != Index:
            Period_ms=Period_us/1000
            # print(Period_ms)
            self.AFG1.setStatusCh1(0)
            self.AFG1.setStatusCh2(0)
            self.AFG1.setPeriodCh1_ms(Period_ms)
            self.AFG1.setPeriodCh2_ms(Period_ms)
            CH1dely=round(self.AFG1.getDelayCh1_s() * 1000000000)
            CH2dely=round(self.AFG1.getDelayCh2_s() * 1000000000)
            # print(CH1dely,CH2dely)
            Dely_ns=CH2dely-CH1dely
            self.AFG1.set_CH2dely=(CH1dely+Dely_ns)%(Period_us * 1000)
            self.AFG1.InitiatePhase()
            print(self.AFG1.getDelayCh1_s() * 1000000000)
            print(self.AFG1.getDelayCh2_s() * 1000000000)

            self.AFG1.setStatusCh1(1)
            self.AFG1.setStatusCh2(1)
        self.is_right = 1
        # self.Period_Index=Index

    def JTDCOpen(self):
        lineEdit_Num=[10,11,12,13]
        self.Period_Index=0
        os.chdir('D:\\lidar\\program\\Dataprocess\\run_for_range')
        # shell_cmd = "run.bat"
        shell_cmd = 'java -Xmx20000M -classpath ../Range_JTDC/JTDC/target/classes;xchart-2.5.1.jar;jscience-4.3.1.jar com.hydra.test.groundtdcserver.AppFrame {}'.format(self.integral_time_s)
        # # shell_cmd=shell_cmd+' {} {} {}'.format(4096,10,0)
        # ms2ps = 1000000000
        # shell_cmd = shell_cmd + ' {} {} {} {}'.format(self.subsize, int(self.pixeltime_ms * ms2ps),
        #                                               self.pixel_waittime_ms, self.scanMode)
        cmd = shlex.split(shell_cmd)
        print(cmd)
        self.is_right=0
        # r = subprocess.check_output(["cmd.exe", "/c", "python try.py"])
        self.p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while self.p.poll() is None:
            line = self.p.stdout.readline()
            print(line)
            try:
                line = str(line, 'utf8')
            except:
                pass
            print(line)
            if "4\r\n" in line:
                # print("JTDC is processing")
                self.TDC_state = "JTDC is processing"
            if "Connected" in line:
                print("TDC Connected")
                self.TDC_state = "TDC Connected"
            if "TDC tube is open" in line:
                print("TDC tube is open")
                self.TDC_state = "TDC tube is open"

            if self.is_right == 1:
                if "Max index:" in line:
                    max= line[10:]
                    exec('self.lineEdit_{}.setText(str({}))'.format(lineEdit_Num[self.Period_Index], max))
                    self.is_right=0
    def wait_For_TDC(self):
        while self.TDC_state != "JTDC is processing":
            pass
        while self.TDC_state != "TDC Connected":
            pass
        time.sleep(2)
        # print("Please open TDC tube")
        # while self.TDC_state != "TDC tube is open":
        #     pass

    # def wait_For_TDC_New(self):
    #     while self.TDC_state != "TDC tube is open":
    #         pass

    def J_Go(self):
        self.TDC_state = ''
        ###########Open JTDC##########
        threading._start_new_thread(self.JTDCOpen, ())
        # self.wait_For_TDC_New()

    def Signal_init(self):
       # self.AFG.Recall_setup(1)
       pass

    def calculate_range(self):
         if (self.lineEdit_10.text() != '') and (self.lineEdit_11.text() != '') and (self.lineEdit_12.text() != ''):
             range_result=self.calculate(float(self.lineEdit.text()),float(self.lineEdit_10.text()), float(self.lineEdit_2.text()),
                          float(self.lineEdit_11.text()), float(self.lineEdit_3.text()),
                          float(self.lineEdit_12.text()))
             self.lineEdit_9.setText(str(range_result))



             # if self.lineEdit_13.text() != None:
             #     self.check_range()
    def Log(self,data):
            # with open('Log.csv', "r+") as f:
                f = open('Log.csv', "r+")
                old = f.read()
                # print('old',old)
                f.seek(0)
                f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '    ' + data + '\n')
                f.write(old)
                f.close()

    def calculate(self,T1,t1,T2,t2,T3,t3,delta_delta=0.001):
            n_1s=[]
            n_2s=[]
            delta2=[]
            Max_range_time=Least_common_multiple(T1, T2, T3)
            Max_range=Max_range_time * 0.15
            self.lineEdit_15.setText(str(Max_range))
            #求出一个值，然后n1加上【T1，T2】/T1*n就是nn
            Max_n_1=int(Max_range_time/T1+0.5)
            for i in range(Max_n_1):
            #for i in range(32):
                t_1=i*T1*1000+ t1
                n_2_cache=(t_1-t2)/(float(T2)*1000)
                delta2_cache=abs(round(n_2_cache)-n_2_cache)
                if delta2_cache<delta_delta:
                    n_2s.append(round(n_2_cache))
                    delta2.append(delta2_cache)
                    n_1s.append(i)
            # print(n_2s)
            count=0
            index=0
            for j in range(len(n_2s)):
                n_3_cache=(T2*1000*n_2s[j]+ t2-t3)/(T3*1000)
                delta3=abs(round(n_3_cache)-n_3_cache)
                print(delta3)
                if delta3 < delta_delta:
                    count += 1
                    n_1=n_1s[j]
                    n_2=n_2s[j]
                    n_3=round(n_3_cache)
                    print(n_3)
                    range_result=(n_3*T3*1000+t3) * 0.00015

            if count==0:
                n_1 = None
                n_2 = None
                n_3 = None
                range_result=None

            self.lineEdit_5.setText(str(n_1))
            self.lineEdit_6.setText(str(n_2))
            self.lineEdit_7.setText(str(n_3))
            self.lineEdit_14.setText(str(count))
            data = 'T1={}us, t1={}ns, n1={},   T2={}us, t2={}ns, n2={},   T3={}us, t3={}ns, n3={},   range={}km'.format(T1,t1,n_1,T2,t2,n_2,T3,t3,n_3,range_result)
            print(data)
            self.Log(data)
            return range_result

    def Least_common_multiple(self,*args):
        Max_decimal_digits = count_float(args)
        # print(Max_decimal_digits)
        size = len(args)
        args = list(args)
        for i in range(size):
            args[i] = int(args[i] * int(math.pow(10, Max_decimal_digits)))
        # print(args)
        idx = 1
        i = int(args[0])
        # i = int(i * math.pow(10,Max_decimal_digits))
        while idx < size:
            j = args[idx]
            # j=int(j * math.pow(10,Max_decimal_digits))
            # print(j)
            # 用辗转相除法求i,j的最大公约数m
            b = i if i < j else j  # i，j中较小那个值
            a = i if i > j else j  # i,j中较大那个值
            r = b  # a除以b的余数
            while (r != 0):
                r = a % b
                if r != 0:
                    a = b
                    b = r
            f = i * j / b  # 两个数的最小公倍数
            i = f
            idx += 1
        return f / math.pow(10, Max_decimal_digits)

    def count_float(args):
        Max = 0
        size = len(args)
        idx = 0
        while idx < size:
            # print(idx)
            s = str(args[idx])
            if s.count('.') == 1:  # 小数有且仅有一个小数点
                left = s.split('.')[0]  # 小数点左边（整数位，可为正或负）
                right = s.split('.')[1]  # 小数点右边（小数位，一定为正）
                if Max < len(right):
                    Max = len(right)
            idx += 1
        # print(Max)
        return Max


def show():
    app = QApplication(sys.argv)
    mainWindow = ranging_Window()
    mainWindow.show()
    sys.exit(app.exec_())




if __name__ == "__main__":
    threading._start_new_thread(show,())
    while True:
        print(1)
        time.sleep(1)
