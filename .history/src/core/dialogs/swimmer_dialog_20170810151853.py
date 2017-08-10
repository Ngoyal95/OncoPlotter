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

    def closeEvent(self,event):
        #Override closeEvent so that we hide the window rather than exit so we don't lose data
        event.ignore()
        self.hide()

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

        markersize = 5 #needs to be user variable so that as more/less bars added, it looks ok
        bar_width = 0.75

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
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(color = 'k', axis = 'y', alpha=0.25)
        self.bar_locations = np.arange(len(self.swimmer_data.ix[:,0]))
        self.stack_lists = [x for x in self.swimmer_data.ix[:,1:6]]
        
        self.offset_list = [0]*len(stack_length_lists[0])
        for i in range(len(stack_lists)):
            ax.barh(self.bar_locations, self.stack_lists[i], bar_width, color = 'b', left = offset_list, edgecolor = 'k')
            offset_list = [sum(x) for x in zip(offset_list, stack_length_lists[i])]

        self.canvas.draw()
        self.ax.hold(False) #rewrite the plot when plot() called