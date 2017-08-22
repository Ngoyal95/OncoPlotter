from PyQt5.QtWidgets import (QColorDialog, QWidget, QPushButton, QComboBox)
from PyQt5 import QtCore, QtGui


class ColorButton(QPushButton):
    '''
    Custom button for color selection
    '''
    def __init__(self,parent,color):
        super(QPushButton,self).__init__(parent)
        
        self.setAutoFillBackground(True)
        self.color = color
        self.set_background_color()
        self.clicked.connect(self.get_color)

    def get_color(self):
        self.color_select = QColorDialog.getColor()
        self.color = self.color_select.name(0) #return hex code string
        self.set_background_color()

    def set_background_color(self):
        self.setStyleSheet("background-color: %s" % self.color)

    def give_color(self):
        return self.color
    
class Combo_Keys_and_Colors(QComboBox):
    def __init__(self,parent,bar_keys_colors,response_type):
        super(QComboBox,self).__init__(parent)
        
        #keys is a dictionary: {'key description':color,...}
        self.dict_of_keys = bar_keys_colors
        self.response_type = response_type
        self.populate()

    def populate(self):
        '''Override method to add items to dropdown'''
        for key in list(self.dict_of_keys.keys()):
            self.pixmap = QtGui.QPixmap(20,20)
            self.pixmap.fill(QtGui.QColor(self.dict_of_keys[key]))
            self.color_icon = QtGui.QIcon(self.pixmap)
            self.addItem(self.color_icon,key)
        self.setCurrentIndex(self.findText(self.response_type,flags=QtCore.Qt.MatchExactly)) #default to the patient cancer type

class Combo_Events(QComboBox):
    def __init__(self,parent,event_keys_colors,event):
        super(QComboBox,self).__init__(parent)

        #events_keys_colors is a dictionary: {'event key description':color,...}
        self.dict_of_events = event_keys_colors
        self.event_type = event
        self.populate()

    def populate(self):
        '''Override method to add items to the combobox dropdown'''
        for key in list(self.dict_of_events.keys()):
            self.pixmap = QtGui.QPixmap(20,20)
            self.pixmap.fill(QtGui.QColor(self.dict_of_events[key]))
            self.color_icon = QtGui.QIcon(self.pixmap)
            self.addItem(self.color_icon,key)
        self.setCurrentIndex(self.findText(self.event_type,flags=QtCore.Qt.MatchExactly)) #default to the patient cancer type
      
