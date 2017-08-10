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
        
    def closeEvent(self,event):
        #Override closeEvent so that we hide the window rather than exit so we don't lose data
        event.ignore()
        self.hide()

class SwimmerPlotter(QWidget):
    def __init__(self,parent=None):
        super(SwimmerPlotter,self).__init__(parent)

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