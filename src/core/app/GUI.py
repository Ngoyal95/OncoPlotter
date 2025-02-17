#! python3

import ctypes
import os
import sys
import shelve
import re
from pathlib import Path
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QFrame,
                             QMainWindow, QPushButton, QSizePolicy, QSplitter,
                             QTextEdit, QVBoxLayout, QWidget)

#GUI 
import core.gui.mainwindow as mainwindow
#Support functions
from core.app.support_functions import import_plot_data

#Dialogs
from core.dialogs.spider_dialog import Spider, SpiderPlotter
from core.dialogs.swimmer_dialog import Swimmer, SwimmerPlotter
from core.dialogs.waterfall_dialog import Waterfall, WaterfallPlotter

image_dir = os.path.dirname(os.path.abspath('../OncoPlot'))

class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):

    waterfall_data_signal = QtCore.pyqtSignal(dict)
    spider_data_signal = QtCore.pyqtSignal(dict)
    swimmer_data_signal = QtCore.pyqtSignal(dict)

    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)

        self.default_waterfall_keys_and_colors = {
                                'CR':'#03945D',
                                'PR':'#B1EE97',
                                'PD':'#FF6F69',
                                'SD':'#707070'
                                }

        self.default_spider_keys_and_colors = {
                                'CR':'#03945D',
                                'PR':'#B1EE97',
                                'PD':'#FF6F69',
                                'SD':'#707070'
                                }

        self.default_spider_event_colors = {
                                'New Lesions':'#e00b0b',
                                'Clinical Progression':'#e05c0b',
                                'Treatment Ongoing':'#000000',
                                '':'#e1e1e1'
                                }
        self.default_spider_event_markers = {
                                'New Lesions':'^',
                                'Clinical Progression':'D',
                                'Treatment Ongoing':'>',
                                '':''                     
                                }

        self.default_swimmer_keys_and_colors = {
                                'CR':'#03945D',
                                'PR':'#B1EE97',
                                'PD':'#FF6F69',
                                'SD':'#707070',
                                'DL1':'#1C26AB',
                                'DL2':'#2F55BB',
                                'DL3':'#4285CC',
                                'DL4':'#55B4DD',
                                'DL5':'#68E4EE'
                                }

        self.setupUi(self)
        self.setup_plot_keys_and_colors()
        self.setup_window()
        self.setup_waterfall_signals()
        self.setup_swimmer_signals()
        self.setup_spider_signals()
            
    #### Setup functions ####
    def setup_plot_keys_and_colors(self):
        '''
        Set defaults for keys and color coding if shelve files do not exist. Otherwise do nothing since they exist
        '''
        waterfall_file = Path("WaterfallSettings.dat")
        spider_file = Path("SpiderSettings.dat")
        swimmer_settings = Path("SwimmerSettings.dat")
        existance_check = [waterfall_file.is_file(),spider_file.is_file(),swimmer_settings.is_file()]

        if ~existance_check[0]:
            #if WaterfallSettings.dat doesn't exist, create it and set default params
            shelfFile = shelve.open('WaterfallSettings')
            shelfFile['DefaultSettings'] = self.default_waterfall_keys_and_colors
            shelfFile['UserSettings'] = self.default_waterfall_keys_and_colors
            shelfFile.close()

        if ~existance_check[1]:
            shelfFile = shelve.open('SpiderSettings')
            shelfFile['DefaultSettings'] = self.default_spider_keys_and_colors
            shelfFile['KeysColors'] = self.default_spider_keys_and_colors
            shelfFile['EventsColors'] = self.default_spider_event_colors
            shelfFile['EventMarkers'] = self.default_spider_event_markers
            shelfFile.close()

        if ~existance_check[2]:
            shelfFile = shelve.open('SwimmerSettings')
            shelfFile['DefaultSettings'] = self.default_swimmer_keys_and_colors
            shelfFile['KeysColors'] = self.default_swimmer_keys_and_colors
            shelfFile['EventsColors'] = self.default_spider_event_colors
            shelfFile['EventMarkers'] = self.default_spider_event_markers
            shelfFile.close()

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

        self.Spider_Plot = SpiderPlotter(self)
        self.Spider = Spider(self)
        self.Spider_Widget = QWidget()
        self.Spider_Box = QVBoxLayout()
        self.Spider_Splitter = QSplitter(QtCore.Qt.Horizontal)
        self.Spider_Splitter.addWidget(self.Spider)
        self.Spider_Splitter.addWidget(self.Spider_Plot)
        self.Spider_Box.addWidget(self.Spider_Splitter)
        self.Spider_Widget.setLayout(self.Spider_Box)

        self.Swimmer_Plot = SwimmerPlotter(self)
        self.Swimmer = Swimmer(self)
        self.Swimmer_Widget = QWidget()
        self.Swimmer_Box = QVBoxLayout()
        self.Swimmer_Splitter = QSplitter(QtCore.Qt.Horizontal)
        self.Swimmer_Splitter.addWidget(self.Swimmer)
        self.Swimmer_Splitter.addWidget(self.Swimmer_Plot)
        self.Swimmer_Box.addWidget(self.Swimmer_Splitter)
        self.Swimmer_Widget.setLayout(self.Swimmer_Box)

        self.stackedWidget.addWidget(self.Waterfall_Widget) #0 in stackedwidget
        self.stackedWidget.addWidget(self.Spider_Widget) #1 in stackedwidget
        self.stackedWidget.addWidget(self.Swimmer_Widget) #2 in stackedwidget
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
        self.swimmerAction.triggered.connect(self.launch_swimmer)
        self.swimmerAction.setIconText("Swimmer")
        self.swimmerAction.setEnabled(False)
        self.toolBar.addAction(self.swimmerAction)
        self.toolBar.addSeparator()

    #### Signal Connections ####
    def setup_waterfall_signals(self):
        self.waterfall_data_signal.connect(self.Waterfall.on_waterfall_data_signal)
        self.Waterfall.plot_signal.connect(self.Waterfall_Plot.on_plot_signal) #updated plot settings

    def setup_swimmer_signals(self):
        self.swimmer_data_signal.connect(self.Swimmer.on_swimmer_data_signal)
        self.Swimmer.plot_signal.connect(self.Swimmer_Plot.on_plot_signal)

    def setup_spider_signals(self):
        self.spider_data_signal.connect(self.Spider.on_spider_data_signal)
        self.Spider.plot_signal.connect(self.Spider_Plot.on_plot_signal) #updated plot settings
        
    #### Launch dialogs functions ####
    def launch_waterfall(self):
        self.statusbar.showMessage('Waterfall plot')
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget.show()

    def launch_spider(self):
        self.statusbar.showMessage('Spider plot')
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget.show()

    def launch_swimmer(self):
        self.statusbar.showMessage('Swimmer plot')
        self.stackedWidget.setCurrentIndex(2)
        self.stackedWidget.show()

    def import_data(self):
        self.statusbar.showMessage('Importing data')
        self.file_path = QFileDialog.getOpenFileName(self,"Select Data Template", "C:\\")[0]
        if bool(self.file_path and self.file_path.strip()):
            self.data_set = import_plot_data(self.file_path)
            self.waterfall_data_signal.emit(self.data_set)
            self.swimmer_data_signal.emit(self.data_set)
            self.spider_data_signal.emit(self.data_set)
            self.waterfallAction.setEnabled(True)
            self.spiderAction.setEnabled(True)
            self.swimmerAction.setEnabled(True)
            self.statusbar.showMessage('Done importing')
        else:
            self.waterfallAction.setEnabled(False)
            self.spiderAction.setEnabled(False)
            self.swimmerAction.setEnabled(False)
            self.statusbar.showMessage('Import cancelled')

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
