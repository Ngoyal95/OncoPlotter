from PyQt5.QtWidgets import (QApplication, QDialog, QWidget)
from PyQt5 import QtCore, QtGui

import core.gui.waterfall as waterfall

class Waterfall(QWidget, waterfall.Ui_Waterfall):
    def __init__(self, parent):
        super(Waterfall,self).__init__(parent)
        self.setupUi(self)
        self.hide()

    def closeEvent(self,event):
        #Override closeEvent so that we hide the window rather than exit so we don't lose data
        event.ignore()
        self.hide()