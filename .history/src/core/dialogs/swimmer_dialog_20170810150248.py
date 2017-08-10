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
    def __init__(self,parent=None):
        super(SwimmerPlotter,self).__init__(parent)


        markersize = 5 #needs to be user variable so that as more/less bars added, it looks ok
        bar_width = 0.75


        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas,self)

        self.btn_plot = QPushButton('Default Plot')
        self.btn_plot.clicked.connect(self.default_plot)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.btn_plot)
        self.setLayout(layout)

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
        bar_locations = np.arange(len(self.swimmer_data.ix[:,0]))
        