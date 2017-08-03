#! python3

from PyQt5.QtWidgets import (QLineEdit, QProgressBar, QDialog, QTableView, 
                            QFileDialog, QAction, QApplication, QWidget, 
                            QPushButton, QMessageBox, QDesktopWidget, QMainWindow,
                            QTreeWidget, QTreeWidgetItem, QItemDelegate
                            )
from PyQt5 import QtCore, QtGui

#GUI 
import core.gui.mainwindow as mainwindow

import os
import sys

image_dir = os.path.dirname(os.path.abspath('../OncoPlot'))

class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)

        self.spiderImage = QtGui.QPixmap(os.path.join(image_dir,'images\spider_nonstack.png'))
        self.btn_spider.setIcon(QtGui.QIcon(self.spiderImage))

        self.spiderImage = QtGui.QPixmap(os.path.join(image_dir,'images\spider_stack.png'))
        self.btn_spider_stacked.setIcon(QtGui.QIcon(self.spiderImage))

def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    main()