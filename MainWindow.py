
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication , QMainWindow,QMessageBox
from  LidarGUI import *
import sys
sys.path.append('../Plot')
import repid_range
import string
import configControl
from allControl import *



class sainWindow(QMainWindow, Ui_sainWindow):

    _signal = QtCore.pyqtSignal(str)  # 定义信号,定义参数为str类型

    def __init__(self, parent=None):
        super(sainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.myButton.clicked.connect(self.myPrint)
        self._signal.connect(self.mySignal)  # 将信号连接到函数mySignal
        # self.pushButton.clicked.connect(self.msg)
        self.TeleLoadButton.clicked.connect(self.Telescope_load)
        self.peridTime=10
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(50)
        self.system_Init()

    def system_Init(self):
        self.system=control()

    def Telescope_load(self):
        state=configControl.getConfig('state',section='GUI')
        print(state)
        self.TeleAElineEdit.setText(str(state)[1:-1])

    def Telescope_Save_botton(self):
        state=self.TeleAElineEdit.text()
        configControl.setConfig('state',state,section='GUI')

    def Telescope_bottonClick(self):
        #control the telescope
        AE=self.TeleAElineEdit.text()
        AE_list=AE.split(',')
        A=float(AE_list[0])
        E = float(AE_list[1])
        self.system.cam.tele1.point_At_uRad_Precise(A,E)

    def Takephotos_Set_bottom(self):
        T_pix=self.Tpix_lineEdit.text()
        #setConfig('pixeltime_ms',T_pix)
        self.system.pixeltime_ms=int(T_pix)

        T_wait = self.Twait_lineEdit.text()
        #setConfig('pixel_waittime_ms', T_wait)
        self.system.pixel_waittime_ms=int(T_wait)

        Size=self.Size_comboBox.currentText()
        self.system.subsize=int(Size)*int(Size)
        #setConfig('subsize', str(int(Size)*int(Size)))
        subpic=self.SP_lineEdit.text()
        self.system.xSubPic=int(subpic)
        self.system.ySubPic = int(subpic)
        #setConfig('xsubpic',subpic)
        #setConfig('ysubpic',subpic)

        self.peridTime=int(Size)*int(Size)*(int(T_pix)+int(T_wait))/1000
        self.period.setText(str(self.peridTime))
        self.period.show()

        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(self.peridTime)
        self.progressBar.setValue(0)

        if self.Stic_checkBox.isChecked():
            mode='Stic'
            self.system.mode=1
            # setConfig('mode',0)
        else:
            mode='D'
            self.system.mode=0
            # setConfig('mode',1)

        self.SateInfo.setText('size:{0}X{1} T_pix:{2} mode:{3}'.format(Size,Size,T_pix,mode))
        self.system.Set_forGui()

    def Takephoto_Start_Button(self):
        threading._start_new_thread(self.system.take_photo(),())

    def Takephoto_Go_botton(self):
        self.system.Go()
        #threading._start_new_thread(self.progressBarShow, ())

    def progressBarShow(self):
        while True:
            t=0
            while t < 50:
                time.sleep(self.peridTime/50)
                t +=1
                self.progressBar.setValue(t-1)

            self.progressBar.setValue(0)

    def kill(proc_pid):
        process = psutil.Process(proc_pid)

        for proc in process.children(recursive=True):
            proc.kill()
            process.kill()

    def Takephoto_Stop_botton(self):
        print('here')
        # threading._start_new_thread(self.kill(self.system.p.pid))
        self.system.kill(self.system.p.pid)

    def Process_Go1_botton(self):
        path=self.Puzzle_lineEdit.text()
        self.system.wholePic(path=path)

    def Process_Go2_botton(self):
        path=self.ThreeD_Draw_lineEdit.text()
        repid_range.threeD(path)



        # path=self.
        #self._signal.emit("你妹，打印结束了吗，快回答！")



    def msg(self):
        reply = QMessageBox.information(self,  # 使用infomation信息框
                                        "标题",
                                        "The picture has been taken!",
                                        QMessageBox.Yes | QMessageBox.No)

    def mySignal(self, string):
        print(string)
        # self.tb.append("打印结束")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = sainWindow()
    mainWindow.show()
    sys.exit(app.exec_())