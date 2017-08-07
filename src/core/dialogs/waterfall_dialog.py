from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (QApplication, QDialog, QWidget)
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
    
    def plot(self):
        self.n = len(waterfall_data[0])
        self.rect_locations = np.arange(self.n)
    
    def auto_label_responses(self,ax,data):
        
        
