'''
Refs:
Embedding plot: https://sukhbinder.wordpress.com/2013/12/16/simple-pyqt-and-matplotlib-example-with-zoompan/
'''

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (QHeaderView, QApplication, QDialog, QWidget, QPushButton, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QComboBox)
from PyQt5 import QtCore, QtGui

import core.gui.waterfall as waterfall
import numpy as np

from pprint import pprint

class CustomCombo(QComboBox):
    

class Waterfall(QWidget, waterfall.Ui_Waterfall):
    
    general_settings_signal = QtCore.pyqtSignal(list) #send list of plotting params
    updated_rectangles_signal = QtCore.pyqtSignal(list) #send list of updated artists for redrawing

    def __init__(self, parent):
        super(Waterfall,self).__init__(parent)
        self.setupUi(self)
        
        #Button functions
        self.btn_apply_general_settings.clicked.connect(self.send_settings)
        self.patient_tree = self.create_patient_tree()
        self.data_viewer_container.addWidget(self.patient_tree)

    def on_waterfall_data_signal(self,signal):
        self.waterfall_data = signal['waterfall_data'] #pandas dataframe
        

    def on_generated_rectangles_signal(self,signal):
        self.rectangles_received = signal[0]
        self.add_items() #display in table
        #print(self.rectangles_received)


    def send_settings(self,signal):
        self.list_general_settings = [
                                        self.plot_title.text(),
                                        self.x_label.text(),
                                        self.y_label.text(),
                                        self.twenty_percent_line.isChecked(),
                                        self.thirty_percent_line.isChecked(),
                                        self.zero_percent_line.isChecked(),
                                        self.display_responses_as_text.isChecked()
                                    ]
        self.general_settings_signal.emit(self.list_general_settings)

    def create_patient_tree(self):
            '''
            Create QTreeWidget populated with a patient's data for the DataEntry dialog.
            Assumes that self.temp_patient is the patient of interest and that the variable belongs to the dialog.
            '''
            self.tree = QTreeWidget()
            self.root = self.tree.invisibleRootItem()
            self.headers = [
                            'Patient #',
                            'Best response %',
                            'Overall response',
                            'Cancer',
                            'Color coding key',
                            ]
            self.headers_item = QTreeWidgetItem(self.headers)
            self.tree.setColumnCount(len(self.headers))
            self.tree.setHeaderItem(self.headers_item)
            self.root.setExpanded(True)
            self.tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.tree.header().setStretchLastSection(False)
            return self.tree

    def add_items(self):
        '''
        Populate viewing tree
        '''
        self.tree.clear() #clear prior to entering items, prevent aggregation
        i=0
        for rect in self.rectangles_received:
            #populate editable tree with rect data
            self.rect_item = QTreeWidgetItem(self.root)
            self.rect_params = [
                                self.waterfall_data['Patient number'][i], 
                                rect.get_height(),
                                self.waterfall_data['Overall response'][i],
                                self.waterfall_data['Cancer'][i]
                                ]
            for col in range(0,4):
                self.rect_item.setText(col,str(self.rect_params[col]))
                self.rect_item.setTextAlignment(col,4)
            self.tree.setItemWidget(self.rect_item, 4, QComboBox())
            self.rect_item.setFlags(self.rect_item.flags() | QtCore.Qt.ItemIsEditable)
            i+=1
        
    def on_updated_tree_item(self):
        #update the rectangle which was edited
        pass

class WaterfallPlotter(QWidget):

    generated_rectangles_signal = QtCore.pyqtSignal(list) #send list of rects for data display in tree

    def __init__(self,parent):
        super(WaterfallPlotter,self).__init__(parent)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas,self)

        self.btn_plot = QPushButton('Default Plot')
        self.btn_plot.clicked.connect(self.default_plot)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.btn_plot)
        self.setLayout(self.layout)
    
    def on_waterfall_data_signal(self,signal):
        self.waterfall_data = signal['waterfall_data'] #pandas dataframe
        self.btn_plot.setEnabled(True)

    def on_general_settings_signal(self,signal):
        try:
            hasattr(self,'ax')
            self.ax.set_title(signal[0])
            self.ax.set_xlabel(signal[1])
            self.ax.set_ylabel(signal[2])
            self.canvas.draw()
        except Exception as e:
            print(e)
            
    def default_plot(self):
        '''
        Plot waterfall data
        '''
        self.figure.clear()
        self.rect_locations = np.arange(len(self.waterfall_data['Best response percent change']))
        self.ax = self.figure.add_subplot(111)
        self.ax.axhline(y=20, linestyle='--', c='k', alpha=0.5, lw=2.0, label='twenty_percent')
        self.ax.axhline(y=-30, linestyle='--', c='k', alpha=0.5, lw=2.0, label='thirty_percent')
        self.ax.axhline(y=0, c='k', alpha=1, lw=2.0, label='zero_percent')
        self.ax.grid(color = 'k', axis = 'y', alpha=0.25)
        self.rects = self.ax.bar(self.rect_locations,self.waterfall_data['Best response percent change'])
        self.auto_label_responses(self.ax, self.rects, self.waterfall_data)
        #self.plot_table()
        self.canvas.draw()
        self.ax.hold(False) #rewrite the plot when plot() called
        self.generated_rectangles_signal.emit([self.rects])
            
    def plot_table(self):
        rows = ['%s' % x for x in self.waterfall_data.keys()]
        rows = rows[4:] #skip first three, they are the 4 standard headers, rest are table rows
        columns = self.waterfall_data['Patient number'] #patient numbers
        cell_text = []
        for row in rows:
            cell_text_temp = []
            for col in range(len(columns)):
                cell_text_temp.append(self.waterfall_data[row][col])
            cell_text.append(cell_text_temp)
        the_table = plt.table(cellText=cell_text, rowLabels=rows, colLabels=columns, loc='bottom', cellLoc='center')
        plt.subplots_adjust(bottom=0.15,left=0.5)
        self.ax.set_xlim(-0.5,len(columns)-0.5)
        plt.tick_params(
                        axis='x',          # changes apply to the x-axis
                        which='both',      # both major and minor ticks are affected
                        bottom='off',      # ticks along the bottom edge are off
                        top='off',         # ticks along the top edge are off
                        labelbottom='off'
                        ) # labels along the bottom edge are off
    
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
                    '%s' % waterfall_data['Overall response'][i], ha='center', va=valign)
            i+=1
