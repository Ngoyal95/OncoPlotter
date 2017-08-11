from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (QApplication, QDialog, QWidget, QPushButton, QVBoxLayout, QTreeWidget, QTreeWidgetItem)
from PyQt5 import QtCore, QtGui

import numpy as np
import core.gui.swimmer as swimmmer

class Swimmer(QWidget, swimmmer.Ui_Swimmer):
    def __init__(self, parent):
        super(Swimmer,self).__init__(parent)
        self.setupUi(self)

    def on_swimmer_data_signal(self,signal):
        self.swimmer_data = signal['swimmer_data'] #pandas dataframe

class SwimmerPlotter(QWidget):
    def __init__(self,parent):
        super(SwimmerPlotter,self).__init__(parent)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas,self)

        self.btn_plot = QPushButton('Default Plot')
        self.btn_plot.clicked.connect(self.default_plot)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.btn_plot)
        self.setLayout(self.layout)



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

    def default_plot(self):
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
        for i in range(len(self.stack_lists.keys())):
            self.stack_listsself.ax.barh(self.bar_locations, self.stack_lists.ix[:,i], self.bar_width, edgecolor='k', left=self.offset_list)
            self.offset_list = [sum(x) for x in zip(self.offset_list, self.stack_lists.ix[:,i])]

        self.canvas.draw()
        self.ax.hold(False) #rewrite the plot when plot() called