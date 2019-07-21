# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication , QMainWindow
from  firstUi import  *
#from LidarGUI import *

if __name__ == '__main__':
    '''
    主函数
    '''

    app = QApplication(sys.argv)
    sainWindow = QMainWindow()
    ui = Ui_sainWindow()
    ui.setupUi(sainWindow)
    sainWindow.show()
    sys.exit(app.exec_())