import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

image_dir = os.path.dirname(os.path.abspath('../OncoPlot'))


class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()

        #Button appearances
        self.btn_waterfall = QPushButton(self)
        self.btn_spider = QPushButton(self)
        self.btn_swimmer = QPushButton(self)

        # self.btn_layout = QVBoxLayout()
        # self.btn_layout.addChildWidget(self.btn_waterfall)
        # self.btn_layout.addChildWidget(self.btn_spider)
        # self.btn_layout.addChildWidget(self.btn_swimmer)

        self.btn_waterfall.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(image_dir,'images\waterfall.png'))))
        self.btn_spider.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(image_dir,'images\spider.png'))))
        self.btn_swimmer.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(image_dir,'images\swimmer_stack.png'))))
        self.btn_waterfall.setIconSize(QtCore.QSize(380,250))
        self.btn_spider.setIconSize(QtCore.QSize(380,250))
        self.btn_waterfall.setFixedSize(400,250)
        self.btn_spider.setFixedSize(400,250)
        self.btn_swimmer.setIconSize(QtCore.QSize(380,250))
        self.btn_swimmer.setFixedSize(400,250)
        
        #hbox = QHBoxLayout(self)
        #vbox = QVBoxLayout(self)

        grid = QGridLayout(self)
        grid.addWidget(self.btn_spider)
        grid.addWidget(self.btn_swimmer)
        grid.addWidget(self.btn_waterfall)


        #split1 = QSplitter(Qt.Vertical)
        #split1.addWidget(grid)
        # split1.addWidget(QPushButton('1'))
        # split1.addWidget(QPushButton('2'))
        # split1.addWidget(QPushButton('3'))
        
        # split1.addWidget(self.btn_spider)
        # split1.addWidget(self.btn_swimmer)
        # split1.addWidget(self.btn_waterfall)

        #split2 = QSplitter(Qt.Horizontal)
        #split2.addWidget(QPushButton())

        #hbox.addWidget(split1)

        #hbox.addWidget(vbox)

        # topleft = QFrame()
        # topleft.setFrameShape(QFrame.StyledPanel)
        # bottom = QFrame()
        # bottom.setFrameShape(QFrame.StyledPanel)

        # splitter1 = QSplitter(Qt.Horizontal)
        # textedit = QTextEdit()
        # splitter1.addWidget(textedit)
        # splitter1.addWidget(topleft)
        # splitter1.setSizes([100,200])

        # splitter2 = QSplitter(Qt.Vertical)
        # splitter2.addWidget(splitter1)
        # splitter2.addWidget(bottom)

        # hbox.addWidget(splitter2)

        self.setLayout(grid)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QSplitter demo')
        self.show()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()