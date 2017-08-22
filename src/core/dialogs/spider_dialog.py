from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rc

from PyQt5.QtWidgets import (QFontDialog, QListWidgetItem, QColorDialog, QHeaderView, QApplication, QDialog, QWidget, QPushButton, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QComboBox)
from PyQt5 import QtCore, QtGui

import core.gui.waterfall as waterfall
import numpy as np
import shelve
import re
from pprint import pprint

import core.gui.spider as spider

class Spider(QWidget, spider.Ui_Spider):

    def __init__(self, parent):
        super(Spider,self).__init__(parent)
        self.setupUi(self)
        self.initialize_settings()
    
    #### Initialization functions ####
    def initialize_settings(self):
        '''
        Load stored settings for keys and colors
        '''
        with shelve.open('SpiderSettings') as shelfFile: 
            self.keys_and_colors = shelfFile['UserSettings']
            shelfFile.close()
    
    #### Signal functions ####
    def on_spider_data_signal(self,signal):
        self.spider_data = signal['spider_data']

class SpiderPlotter(QWidget):
    
    def __init__(self,parent):
        super(SpiderPlotter,self).__init__(parent)

        #initialize
        self.initialize_settings()
        self.settings_update = False

        #creating plotting widget
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas,self)
        self.btn_plot = QPushButton('Create Default Plot (RESET)')
        self.btn_plot.clicked.connect(self.default_plot)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.btn_plot)
        self.setLayout(self.layout)
    
    #### Initialization functions ####
    def initialize_settings(self):
        '''
        Load stored settings for keys and colors
        '''
        with shelve.open('SpiderSettings') as shelfFile: 
            self.keys_and_colors = shelfFile['UserSettings']
            shelfFile.close()

    #### Signal functions ####
    def on_spider_data_signal(self,signal):
        self.spider_data = signal['spider_data']
        
    #### Plotting functions ####
    def default_plot(self):
        self.settings_update = False
        self.plot()

    def plot(self):
        '''
        Plot spider data
        '''
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.x_axis_marks = self.spider_data.ix[:len(self.spider_data)-2,0] #all but last row, 0th column of the dataframe is the time from baseline measurement
        self.num_of_timepoints = len(self.x_axis_marks)
        self.number_of_series = len(self.spider_data.columns) #remaining columns are for tumor burden percent changes
        self.patient_responses = self.spider_data.ix[len(self.spider_data)-1,:]
        print(self.patient_responses)
        self.series = [] #list of the series being plotted

        if self.settings_update == False:
            #standard plot, replotted when 'Create Default Plot (RESET)' is clicked
            for i in range(1,self.number_of_series):
                pt_series = [x for x in self.spider_data.ix[:len(self.spider_data)-2,i] if x is not 'Nan']
                clr = self.keys_and_colors[self.patient_responses[i]]
                self.series.append(self.ax.plot(self.x_axis_marks,pt_series, linestyle='solid', linewidth='2', color=clr))
        else:
            pass
        self.ax.grid(color = 'k', axis = 'y', alpha=0.25)
        self.canvas.draw()

    #### Miscellaneous functions ####