from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rc

from PyQt5.QtWidgets import (QFontDialog, QListWidgetItem, QColorDialog, QHeaderView, QApplication, QDialog, QWidget, QPushButton, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QComboBox)
from PyQt5 import QtCore, QtGui

import numpy as np
import shelve
import re
from pprint import pprint

import core.gui.swimmer as swimmmer

class CustomCombo(QComboBox):
    def __init__(self,parent,bar_keys_colors,response_type):
        super(QComboBox,self).__init__(parent)
        
        #keys is a dictionary: {'key description':color,...}
        self.dict_of_keys = bar_keys_colors
        self.response_type = response_type
        self.populate()

    def populate(self):
        '''Override method to add items to list'''
        for key in list(self.dict_of_keys.keys()):
            self.pixmap = QtGui.QPixmap(20,20)
            self.pixmap.fill(QtGui.QColor(self.dict_of_keys[key]))
            self.color_icon = QtGui.QIcon(self.pixmap)
            self.addItem(self.color_icon,key)
        self.setCurrentIndex(self.findText(self.response_type,flags=QtCore.Qt.MatchExactly)) #default to the patient cancer type

class Swimmer(QWidget, swimmmer.Ui_Swimmer):
    def __init__(self, parent):
        super(Swimmer,self).__init__(parent)
        self.setupUi(self)
        self.initialize_settings()

        #self.patient_tree = self.create_patient_tree()
        #self.data_viewer_container.addWidget(self.patient_tree)

    #### Initialization functions ####
    def initialize_settings(self):
        '''
        Load stored settings for keys and colors
        '''
        with shelve.open('SwimmerSettings') as shelfFile: 
            self.keys_and_colors = shelfFile['UserSettings']
            shelfFile.close()

    #### Signal functions ####
    def on_swimmer_data_signal(self,signal):
        self.swimmer_data = signal['swimmer_data'] #pandas dataframe
   
class SwimmerPlotter(QWidget):
    def __init__(self,parent):
        super(SwimmerPlotter,self).__init__(parent)

        #Initialize
        self.initialize_settings()
        self.settings_update = False

        #create plotting widget
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
        with shelve.open('SwimmerSettings') as shelfFile: 
            self.keys_and_colors = shelfFile['UserSettings']
            shelfFile.close()

    #### Signal functions ####
    def on_swimmer_data_signal(self,signal):
        self.swimmer_data = signal['swimmer_data'] #pandas dataframe
        self.btn_plot.setEnabled(True)

    def on_general_settings_signal(self,signal):
        try:
            hasattr(self,'ax')
            self.ax.set_title(signal[0])
            self.ax.set_xlabel(signal[1])
            self.ax.set_ylabel(signal[2])
            self.canvas.draw()
        except Exception as e:
            print(e)

    #### Plot functions ####
    def default_plot(self):
        self.settings_update = False
        self.plot()

    def plot(self):
        '''
        Plot swimmer data
        '''
        self.markersize = 5 #needs to be user variable so that as more/less bars added, it looks ok
        self.bar_width = 0.75
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(color = 'k', axis = 'y', alpha=0.25)
        self.bar_locations = np.arange(len(self.swimmer_data.ix[:,0]))
        self.stack_lists = self.swimmer_data.ix[:,1:6] #col 6 is the total time on treatment sum, don't include
        self.stack_rect_lists = []
        self.offset_list = [0]*len(self.stack_lists.ix[:,0])

        if ~self.settings_update:
            for i in range(len(self.stack_lists.keys())):
                self.stack_rect_lists.append(self.ax.barh(self.bar_locations, self.stack_lists.ix[:,i], self.bar_width, edgecolor='k', left=self.offset_list))
                self.offset_list = [sum(x) for x in zip(self.offset_list, self.stack_lists.ix[:,i])]
        else:
            pass
        self.canvas.draw()