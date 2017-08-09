#! python3

import ctypes
import os
import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QFrame,
                             QMainWindow, QPushButton, QSizePolicy, QSplitter,
                             QTextEdit, QVBoxLayout, QWidget)

#GUI 
import core.gui.mainwindow as mainwindow
#Support functions
from core.app.support_functions import import_plot_data
from core.dialogs.spider_dialog import Spider, SpiderPlotter
#Dialogs
from core.dialogs.swimmer_dialog import Swimmer, SwimmerPlotter
from core.dialogs.waterfall_dialog import Waterfall, WaterfallPlotter

image_dir = os.path.dirname(os.path.abspath('../OncoPlot'))

class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):

    waterfall_data_signal = QtCore.pyqtSignal(list)

    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.setup_window()

    def setup_window(self):
        #Dialogs
        self.Waterfall_Plot = WaterfallPlotter(self)
        self.Waterfall = Waterfall(self)
        self.Waterfall_Widget = QWidget()
        self.Waterfall_Box = QVBoxLayout()
        self.Waterfall_Splitter = QSplitter(QtCore.Qt.Horizontal)
        self.Waterfall_Splitter.addWidget(self.Waterfall)
        self.Waterfall_Splitter.addWidget(self.Waterfall_Plot)
        self.Waterfall_Box.addWidget(self.Waterfall_Splitter)
        self.Waterfall_Widget.setLayout(self.Waterfall_Box)

        self.Spider_Widget = QWidget()
        self.Spider_Box = QVBoxLayout()
        self.Spider_Splitter = QSplitter(QtCore.Qt.Horizontal)
        self.Spider_Plot = SpiderPlotter(self)
        self.Spider = Spider(self)
        self.Spider_Splitter.addWidget(self.Spider)
        self.Spider_Splitter.addWidget(self.Spider_Plot)
        self.Spider_Box.addWidget(self.Spider_Splitter)
        self.Spider_Widget.setLayout(self.Spider_Box)

        self.Swimmer_Widget = QWidget()
        self.Swimmer_Box = QVBoxLayout()
        self.Swimmer_Splitter = QSplitter(QtCore.Qt.Horizontal)
        self.Swimmer_Plot = SwimmerPlotter(self)
        self.Swimmer = Swimmer(self)
        self.Swimmer_Splitter.addWidget(self.Swimmer)
        self.Swimmer_Splitter.addWidget(self.Swimmer_Plot)
        self.Swimmer_Box.addWidget(self.Swimmer_Splitter)
        self.Swimmer_Widget.setLayout(self.Swimmer_Box)

        self.stackedWidget.addWidget(self.Waterfall_Widget) #0
        self.stackedWidget.addWidget(self.Spider_Widget) #1
        self.stackedWidget.addWidget(self.Swimmer_Widget) #2
        self.stackedWidget.hide()

        #Set up toolBar
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        importAction = QAction(QtGui.QIcon(os.path.join(image_dir,'images\Download.png')), 'Import date template', self)
        importAction.triggered.connect(self.import_data)
        importAction.setIconText("Import")
        self.toolBar.addAction(importAction)
        self.toolBar.addSeparator()

        dumpAction = QAction(QtGui.QIcon(os.path.join(image_dir,'images\Rubbish.png')), 'Import date template', self)
        #dumpAction.triggered.connect(self.dump_data)
        dumpAction.setIconText("Dump data")
        self.toolBar.addAction(dumpAction)
        self.toolBar.addSeparator()

        self.waterfallAction = QAction(QtGui.QIcon(os.path.join(image_dir, r'images\waterfall.png')), 'Waterfall plot', self)
        self.waterfallAction.triggered.connect(self.launch_waterfall)
        self.waterfallAction.setIconText("Waterfall")
        self.waterfallAction.setEnabled(False)
        self.toolBar.addAction(self.waterfallAction)
        
        self.spiderAction = QAction(QtGui.QIcon(os.path.join(image_dir, r'images\spider.png')), 'Spider plot', self)
        self.spiderAction.triggered.connect(self.launch_spider)
        self.spiderAction.setIconText("Spider")
        self.spiderAction.setEnabled(False)
        self.toolBar.addAction(self.spiderAction)

        self.swimmerAction = QAction(QtGui.QIcon(os.path.join(image_dir, r'images\swimmer_stack.png')), 'Swimmer plot', self)
        self.swimmerAction.triggered.connect(self.launch_spider)
        self.swimmerAction.setIconText("Swimmer")
        self.swimmerAction.setEnabled(False)
        self.toolBar.addAction(self.swimmerAction)
        self.toolBar.addSeparator()

        #Signal interconnections
        self.waterfall_data_signal.connect(self.Waterfall.on_waterfall_data_signal)
        self.waterfall_data_signal.connect(self.Waterfall_Plot.on_waterfall_data_signal)
        self.Waterfall.general_settings_signal.connect(self.Waterfall_Plot.on_general_settings_signal)

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

    def import_data(self):
        self.file_path = QFileDialog.getOpenFileName(self,"Select Data Template", "C:\\")[0]
        if self.file_path == '':
            pass
        else:
            self.waterfall_data = import_plot_data(self.file_path)
            self.waterfall_data_signal.emit(self.waterfall_data)
        self.waterfallAction.setEnabled(True)
        self.spiderAction.setEnabled(True)
        self.swimmerAction.setEnabled(True)

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
