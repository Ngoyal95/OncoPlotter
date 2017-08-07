'''
Refs:
Embedding plot: https://sukhbinder.wordpress.com/2013/12/16/simple-pyqt-and-matplotlib-example-with-zoompan/
'''

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (QApplication, QDialog, QWidget, QPushButton, QVBoxLayout)
from PyQt5 import QtCore, QtGui

import core.gui.waterfall as waterfall
import numpy as np

class Waterfall(QWidget, waterfall.Ui_Waterfall):
    
    general_settings_signal = QtCore.pyqtSignal(list) #send list of plotting params
    
    def __init__(self, parent):
        super(Waterfall,self).__init__(parent)
        self.setupUi(self)
        
        #connect signals
        parent.waterfall_data_signal.connect(self.get_data)

        #Button functions
        self.apply_general_settings.clicked.connect(self.general_settings)

    def closeEvent(self,event):
        #Override closeEvent so that we hide the window rather than exit so we don't lose data
        event.ignore()
        self.hide()
        
    def get_data(self,signal):
        self.waterfall_data = signal
        
    def general_settings(self):
        pass

class WaterfallPlotter(QWidget):
    def __init__(self,parent=None):
        super(WaterfallPlotter,self).__init__(parent)

        parent.waterfall_data_signal.connect(self.get_data)

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
    
    def get_data(self,signal):
        self.waterfall_data = signal

    def default_plot(self):
        '''
        Plot waterfall data
        '''
        self.rect_locations = np.arange(len(self.waterfall_data[0]))
        ax = self.figure.add_subplot(111)
        ax.axhline(y=20, linestyle='--', c='k', alpha=0.5, lw=2.0)
        ax.axhline(y=-30, linestyle='--', c='k', alpha=0.5, lw=2.0)
        ax.axhline(y=0, c='k', alpha=1, lw=2.0)
        ax.grid(color = 'k', axis = 'y', alpha=0.25)
        self.rects = ax.bar(self.rect_locations,self.waterfall_data[1])
        self.auto_label_responses(ax, self.rects, self.waterfall_data)
        self.canvas.draw()
        ax.hold(False) #rewrite the plot when plot() called
        
    def update_plot(self):
        '''
        TODO
        '''
        pass
                    
    def auto_label_responses(self, ax, rects, waterfall_data):
        '''Add labels above/below bars'''
        i = 0
        for rect in rects:
            height = rect.get_height()
            if height >= 0:
                valign = 'bottom'
            else:
                valign = 'top'
                
            ax.text(rect.get_x() + rect.get_width()/2., height,
                    '%s' % waterfall_data[2][i], ha='center', va=valign)
            i+=1