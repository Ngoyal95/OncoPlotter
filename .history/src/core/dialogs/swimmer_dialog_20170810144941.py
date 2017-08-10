from PyQt5.QtWidgets import (QWidget)
from PyQt5 import QtCore, QtGui

import core.gui.swimmer as swimmmer

class Swimmer(QWidget, swimmmer.Ui_Swimmer):
    def __init__(self, parent):
        super(Swimmer,self).__init__(parent)
        self.setupUi(self)
        
    def closeEvent(self,event):
        #Override closeEvent so that we hide the window rather than exit so we don't lose data
        event.ignore()
        self.hide()

class WaterfallPlotter(QWidget):
    def __init__(self,parent=None):
        super(WaterfallPlotter,self).__init__(parent)

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