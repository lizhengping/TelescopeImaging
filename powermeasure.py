
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication , QMainWindow,QMessageBox
from  powerMeasureGUI import *
import sys
sys.path.append('..')
import repid_range
import string
import configControl
from allControl import *
import Telecom
from Device.ITECH_IT6322 import IT6322


class MainWindow(QMainWindow, Ui_MainWindow):

    _signal = QtCore.pyqtSignal(str)  # 定义信号,定义参数为str类型

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.Connect_Power)
        self.pushButton_2.clicked.connect(self.buttom_clicked_Power)
        self.pushButton_3.clicked.connect(self.Laser_Power_Off)
        self.pushButton_4.clicked.connect(self.Laser_Power_On)
        self.Flipper_channel=2
        self.Laser_channel=1
        # # self.myButton.clicked.connect(self.myPrint)
        # self._signal.connect(self.mySignal)  # 将信号连接到函数mySignal
        # # self.pushButton.clicked.connect(self.msg)
        # self.TeleLoadButton.clicked.connect(self.Telescope_load)
        #
        # self.Init()

    # def Connect(self):
    #     comstr='{}'.format(self.lineEdit.text())
    #     print(comstr)
    #     self.pushButton_2.setDisabled(1)
    #     Signal = Telecom.TeleSerial(com=comstr)
    #
    # def buttom_clicked(self):
    #     Signal.Send_signal()
    #     print('Out Put already')

    def buttom_clicked_Power(self):
        comstr = '{}'.format(self.lineEdit.text())
        print(comstr)

        try:
            self.TTL_Signal = IT6322(comstr)
            print(self.TTL_Signal.getIdentity())
        except:
            print('It cant be found')
        else:
            self.pushButton_2.setDisabled(True)

    def Connect_Power(self):
        # print(self.TTL_Signal.getIdentity())
        # print(self.TTL_Signal.getOutputStatuses()[self.Laser_channel])
        self.TTL_Signal.setOutputStatus(self.Flipper_channel,not(self.TTL_Signal.getOutputStatuses()[self.Flipper_channel]))

    def Laser_Power_On(self):
        # print(self.TTL_Signal.getOutputStatus(self.Laser_channel))
         self.TTL_Signal.setOutputStatus(self.Laser_channel,1)
         self.checkBox.setCheckState(1)

    def Laser_Power_Off(self):
        # self.TTL_Signal.setOutputStatus(self.Laser_channel, 1)
        self.TTL_Signal.setOutputStatus(self.Laser_channel,0)
        self.checkBox.setCheckState(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())