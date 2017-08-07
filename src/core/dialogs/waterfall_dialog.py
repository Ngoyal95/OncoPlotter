from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (QApplication, QDialog, QWidget, QPushButton, )
from PyQt5 import QtCore, QtGui

import core.gui.waterfall as waterfall
import numpy as np

class Waterfall(QWidget, waterfall.Ui_Waterfall):
    def __init__(self, parent):
        super(Waterfall,self).__init__(parent)
        self.setupUi(self)
        
        #connect signals
        parent.waterfall_data_signal.connect(self.get_data)

    def closeEvent(self,event):
        #Override closeEvent so that we hide the window rather than exit so we don't lose data
        event.ignore()
        self.hide()
        
    def get_data(self,signal):
        self.waterfall_data = signal
        
class WaterfallPlotter(QWidget):
    def __init__(self,parent=none)
        super(WaterfallPlotter,self).__init__(parent)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas,self)
        self.toolbar.hide()

        self.btn_plot = QPushButton('Default Plot')
        self.btn_plot.clicked.connect(self.plot)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.btn_plot)
        self.setLayout(layout)
    
    def default_plot(self):
        '''
        Plot waterfall data
        '''
        self.n = len(waterfall_data[0])
        self.rect_locations = np.arange(self.n)
        ax = self.figure.add_subplot(111)
        ax.hold(False) #rewrite the plot when plot() called
        ax.axhline(y=20, linestyle='--', c='k', alpha=0.5, width = 1)
        ax.axhline(y=-30, linestyle='--', c='k', alpha=0.5, width = 1)
        ax.axhline(y=0, c='k', alpha=1, width = 1)
        self.rects = ax.bar(self.rect_locations,self.waterfall_data[1])
        self.auto_label_responses(ax, self.rects, self.waterfall_data)
        self.canvas.draw()
        
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
                valign = 'top
                
            ax.text(rect.get_x() + rect.get_width()/2., height,
                    '%s' % waterfall_data[2][i], ha='center', va=valign)
            i+=1
            
        
