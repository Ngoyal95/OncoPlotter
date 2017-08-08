# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(410, 800)
        MainWindow.setIconSize(QtCore.QSize(50, 50))
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_data_import = QtWidgets.QPushButton(self.centralwidget)
        self.btn_data_import.setText("")
        self.btn_data_import.setObjectName("btn_data_import")
        self.horizontalLayout_3.addWidget(self.btn_data_import)
        self.btn_discard_dataset = QtWidgets.QPushButton(self.centralwidget)
        self.btn_discard_dataset.setText("")
        self.btn_discard_dataset.setObjectName("btn_discard_dataset")
        self.horizontalLayout_3.addWidget(self.btn_discard_dataset)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.btn_waterfall = QtWidgets.QPushButton(self.centralwidget)
        self.btn_waterfall.setText("")
        self.btn_waterfall.setCheckable(True)
        self.btn_waterfall.setAutoExclusive(True)
        self.btn_waterfall.setObjectName("btn_waterfall")
        self.verticalLayout.addWidget(self.btn_waterfall)
        self.btn_spider = QtWidgets.QPushButton(self.centralwidget)
        self.btn_spider.setText("")
        self.btn_spider.setCheckable(True)
        self.btn_spider.setAutoExclusive(True)
        self.btn_spider.setObjectName("btn_spider")
        self.verticalLayout.addWidget(self.btn_spider)
        self.btn_swimmer = QtWidgets.QPushButton(self.centralwidget)
        self.btn_swimmer.setText("")
        self.btn_swimmer.setCheckable(True)
        self.btn_swimmer.setAutoExclusive(True)
        self.btn_swimmer.setObjectName("btn_swimmer")
        self.verticalLayout.addWidget(self.btn_swimmer)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.horizontalLayout.addWidget(self.stackedWidget)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 410, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionGeneral_Settings = QtWidgets.QAction(MainWindow)
        self.actionGeneral_Settings.setObjectName("actionGeneral_Settings")
        self.toolbar_quit = QtWidgets.QAction(MainWindow)
        self.toolbar_quit.setObjectName("toolbar_quit")
        self.menuFile.addAction(self.toolbar_quit)
        self.menuSettings.addAction(self.actionGeneral_Settings)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.toolbar_quit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OncoPlotter"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help"))
        self.menuSettings.setTitle(_translate("MainWindow", "&Settings"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionGeneral_Settings.setText(_translate("MainWindow", "General Settings"))
        self.toolbar_quit.setText(_translate("MainWindow", "Quit"))
        self.toolbar_quit.setShortcut(_translate("MainWindow", "Ctrl+Q"))

