
# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication , QMainWindow,QMessageBox
from  Motion_GUI import *
import sys
import threading
import visa
import serial.tools.list_ports
from serial import *
import threading
import TeleMotion




class ranging_Window(QMainWindow, Ui_MainWindow):

    _signal = QtCore.pyqtSignal(str)  # 定义信号,定义参数为str类型

    def __init__(self, parent=None,Axis1=None,Axis2=None,Independ=True):
        self.Independ = Independ
        self.Moto1=Axis1
        self.Moto2=Axis2
        super(ranging_Window, self).__init__(parent)
        self.setupUi(self)
        self.fun_connect()
        self.step_size_change()


        self.listResources()
        self.integral_time_s = 2
        # self.J_Go()
        # self.Signal_init()
        # threading._start_new_thread(self.calculate_range,())

    def fun_connect(self):

        self.pushButton.clicked.connect(self.connect)
        self.pushButton_8.clicked.connect(self.Enable)
        self.pushButton_9.clicked.connect(self.Disable)
        self.pushButton_10.clicked.connect(self.STOP)
        self.pushButton_7.clicked.connect(self.get_State)
        self.comboBox_3.currentTextChanged.connect(self.step_size_change)
        self.pushButton_2.clicked.connect(self.UP)
        self.pushButton_3.clicked.connect(self.LEFT)
        self.pushButton_4.clicked.connect(self.RIGHT)
        self.pushButton_5.clicked.connect(self.DOWN)
        self.pushButton_6.clicked.connect(self.SEND1)
        self.pushButton_11.clicked.connect(self.SEND2)
        self.pushButton_12.clicked.connect(self.GoTo)

    def Enable(self):
        self.Moto1.Enable()
        self.Moto2.Enable()

    def Disable(self):
        self.Moto1.Disable()
        self.Moto2.Disable()

    def STOP(self):
        self.Moto1.slewing_Stop()
        self.Moto2.slewing_Stop()

    def get_State(self):

         while True:
            self.lineEdit_5.setText(str(self.Moto1.get_Direction_Precise_uRad()))
            self.lineEdit_6.setText(str(self.Moto2.get_Direction_Precise_uRad()))
            isMoto1_Ok=self.Moto1.is_Stopped()
            isMoto2_Ok=self.Moto2.is_Stopped()

            if isMoto1_Ok == 1 and isMoto2_Ok == 1:
                self.label_7.setStyleSheet("background-color:green;")
                break
            else:
                self.label_7.setStyleSheet("background-color:red;")
                time.sleep(0.5)


    def UP(self):
        stepsize=int(self.comboBox_3.currentText())
        self.Moto1.Slewing_Inc(stepsize)
        self.get_State()

    def LEFT(self):
        stepsize = int(self.comboBox_3.currentText())
        self.Moto2.Slewing_Inc(stepsize)
        self.get_State()
    def RIGHT(self):
        stepsize = int(self.comboBox_3.currentText())
        self.Moto2.Slewing_Inc(-stepsize)
        self.get_State()
    def DOWN(self):
        stepsize = int(self.comboBox_3.currentText())
        self.Moto1.Slewing_Inc(-stepsize)
        self.get_State()

    def GoTo(self):
        A=float(self.lineEdit_7.text())
        E=float(self.lineEdit_8.text())
        self.Moto1.point_At_uRad_Precise(A)
        self.Moto2.point_At_uRad_Precise(E)

    def connect(self):
        if self.Independ==True:
            id1 = self.comboBox.currentText()
            id2 = self.comboBox_2.currentText()
            try:
                self.Moto1=TeleMotion.Tele_Axis(id1)
                self.Moto2=TeleMotion.Tele_Axis(id2)
                self.label_3.setStyleSheet("background-color:green;")
                # threading._start_new_thread(self.get_State, ())
            except:
                print('Open Erro!')
        else:
            self.label_3.setStyleSheet("background-color:green;")



        # print('ad1',self.AFG1.getID())
        # print('ad2',self.AFG2.getID())
        # self.AFG=AFG3252(self.comboBox.currentText())

    def listResources(self):
        port_list = list(serial.tools.list_ports.comports())
        for i in port_list:
            self.comboBox.addItem(i[0])
            self.comboBox_2.addItem(i[0])
        return


   # 串口初始化配置


        # threading._start_new_thread(self.show_isFinished, ())
        # self.ser.setBaudrate(self.baudrate)
        # self.ser.open()
        # print self.ser.isOpen()
        # print self.ser

    # def Choice(self, event):
    #     context = self.boxValue.get()
    #     list = ["COM1", 'COM2', 'COM3', 'COM4']
    #     if context in list:
    #         self.port = context
    #         self.ser.setPort(self.port)
    #     print
    #     self.port

    # def ChoiceBaudrate(self, event):
    #     self.baudrate = self.boxValueBaudrate.get()
    #     self.ser.setBaudrate(self.baudrate)
    #     print
    #     self.baudrate

    def SEND1(self):

        cmd = self.lineEdit.text()
        output=self.Moto1.seri.cmd_return(cmd)
        self.textBrowser.moveCursor(1)
        self.textBrowser.insertPlainText(output)

    def SEND2(self):

        cmd = self.lineEdit_2.text()
        output = self.Moto2.seri.cmd_return(cmd)
        self.textBrowser_2.moveCursor(1)
        self.textBrowser_2.insertPlainText(output)


    def step_size_change(self):
        self.step_size = self.comboBox_3.currentText()
        return self.step_size

    def open(self):
        pass
        t = threading.Thread(target=run)
        t.setDaemon(True)
        t.start()
        # Frame.after(100,self.run())
        # self.ser.open()
        # if self.ser.isOpen() == True:
        #     self.showSerial.delete(0.0, END)
        #     self.showSerial.insert(0.0, "Serial has been opend!")

    def close(self):
        global a
        a= a * -1
        # self.ser.close()
        if self.ser.isOpen() == False:
            self.showSerial.delete(0.0, END)
            self.showSerial.insert(0.0, "Serial has been closed!")

    def show_isFinished(self):
        global  a
        while True:
            if a == -1:
                self.lab5.configure(bg='green')
            else:
                self.lab5.configure(bg='red')


def show(Axis1=None,Axis2=None,Independ=True):
    app = QApplication(sys.argv)
    mainWindow = ranging_Window(None,Axis1,Axis2,Independ)
    mainWindow.show()
    sys.exit(app.exec_())



def wait_for_open():
    a=input('GUI for Motion please input Mo\n')
    if a == 'Mo':
        threading._start_new_thread(show, ())

if __name__ == "__main__":
    threading._start_new_thread(wait_for_open,())
    while True:
        pass