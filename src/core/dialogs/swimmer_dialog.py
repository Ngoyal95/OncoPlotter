from PyQt5.QtWidgets import (QApplication, QDialog, QWidget)
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

class SwimmerPlotter(QWidget):
    pass