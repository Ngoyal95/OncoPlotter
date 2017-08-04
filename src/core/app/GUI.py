#! python3

from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QTextEdit, QWidget, QSplitter, QFrame, QPushButton, QSizePolicy)
from PyQt5 import QtCore, QtGui

#plotting
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

#GUI 
import core.gui.mainwindow as mainwindow

#Dialogs
from core.dialogs.swimmer_dialog import Swimmer
from core.dialogs.spider_dialog import Spider
from core.dialogs.waterfall_dialog import Waterfall
from core.dialogs.plot_dialog import Plotter

import os
import sys
import ctypes

image_dir = os.path.dirname(os.path.abspath('../OncoPlot'))

class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.setup_window()

    def setup_window(self):
        #Dialogs
        
        self.Waterfall_Widget = QWidget()
        self.Waterfall_Box = QVBoxLayout()
        self.Waterfall_Splitter = QSplitter(QtCore.Qt.Horizontal)
        self.Waterfall_Plot = Plotter(self)
        self.Waterfall = Waterfall(self)
        self.Waterfall_Splitter.addWidget(self.Waterfall)
        self.Waterfall_Splitter.addWidget(self.Waterfall_Plot)
        self.Waterfall_Box.addWidget(self.Waterfall_Splitter)
        self.Waterfall_Widget.setLayout(self.Waterfall_Box)

        self.Spider_Widget = QWidget()
        self.Spider_Box = QVBoxLayout()
        self.Spider_Splitter = QSplitter(QtCore.Qt.Horizontal)
        self.Spider_Plot = Plotter(self)
        self.Spider = Spider(self)
        self.Spider_Splitter.addWidget(self.Spider)
        self.Spider_Splitter.addWidget(self.Spider_Plot)
        self.Spider_Box.addWidget(self.Spider_Splitter)
        self.Spider_Widget.setLayout(self.Spider_Box)

        self.Swimmer_Widget = QWidget()
        self.Swimmer_Box = QVBoxLayout()
        self.Swimmer_Splitter = QSplitter(QtCore.Qt.Horizontal)
        self.Swimmer_Plot = Plotter(self)
        self.Swimmer = Swimmer(self)
        self.Swimmer_Splitter.addWidget(self.Swimmer)
        self.Swimmer_Splitter.addWidget(self.Swimmer_Plot)
        self.Swimmer_Box.addWidget(self.Swimmer_Splitter)
        self.Swimmer_Widget.setLayout(self.Swimmer_Box)

        self.stackedWidget.addWidget(self.Waterfall_Widget) #0
        self.stackedWidget.addWidget(self.Spider_Widget) #1
        self.stackedWidget.addWidget(self.Swimmer_Widget) #2
        self.stackedWidget.hide()

        #Icon
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(image_dir,'images\spider.png'))))

        #Button appearances
        self.btn_data_import.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_discard_dataset.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.btn_data_import.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(image_dir,'images\Download.png'))))
        self.btn_discard_dataset.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(image_dir,'images\Rubbish.png'))))

        self.btn_data_import.setIconSize(QtCore.QSize(90,90))
        self.btn_discard_dataset.setIconSize(QtCore.QSize(90,90))

        self.btn_data_import.setFixedSize(190, 100)
        self.btn_discard_dataset.setFixedSize(190, 100)

        self.btn_waterfall.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_spider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_swimmer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.btn_waterfall.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(image_dir,'images\waterfall.png'))))
        self.btn_spider.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(image_dir,'images\spider.png'))))
        self.btn_swimmer.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(image_dir,'images\swimmer_stack.png'))))

        self.btn_waterfall.setIconSize(QtCore.QSize(370,250))
        self.btn_spider.setIconSize(QtCore.QSize(380,250))
        self.btn_swimmer.setIconSize(QtCore.QSize(380,250))

        self.btn_waterfall.setFixedSize(400,250)
        self.btn_spider.setFixedSize(400,250)
        self.btn_swimmer.setFixedSize(400,250)

        #Button connections
        self.btn_waterfall.clicked.connect(self.launch_waterfall)
        self.btn_spider.clicked.connect(self.launch_spider)
        self.btn_swimmer.clicked.connect(self.launch_swimmer)

    #Launch functions
    def launch_waterfall(self):
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget.show()

    def launch_spider(self):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget.show()

    def launch_swimmer(self):
        self.stackedWidget.setCurrentIndex(2)
        self.stackedWidget.show()

def main():
    myappid = u'OncoPlotter_V1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    app.setApplicationName('OncoPlotter')
    app.setStyle("plastique")
    app.setStyleSheet("QSplitter::handle { background-color: gray }")

    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    main()