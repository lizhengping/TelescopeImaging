# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'firstUi.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from function import *

class Ui_sainWindow(object):
    def setupUi(self, sainWindow):
        sainWindow.setObjectName("sainWindow")
        sainWindow.resize(240, 320)
        self.centralwidget = QtWidgets.QWidget(sainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(60, 140, 113, 32))
        self.pushButton.setObjectName("pushButton")
        sainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(sainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 240, 22))
        self.menubar.setObjectName("menubar")
        sainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(sainWindow)
        self.statusbar.setObjectName("statusbar")
        sainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(sainWindow)
        self.pushButton.clicked.connect(sbottonClick)
        self.pushButton.released.connect(sbottonClick)
        QtCore.QMetaObject.connectSlotsByName(sainWindow)

    def retranslateUi(self, sainWindow):
        _translate = QtCore.QCoreApplication.translate
        sainWindow.setWindowTitle(_translate("sainWindow", "MainWindow"))
        self.pushButton.setText(_translate("sainWindow", "Go"))

    def sbottonClick(self):
        QtWidgets.QMessageBox.information(self.pushButton, "标题", "这是第一个PyQt5 GUI程序")

