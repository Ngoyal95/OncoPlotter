'''
Refs:
Embedding plot: https://sukhbinder.wordpress.com/2013/12/16/simple-pyqt-and-matplotlib-example-with-zoompan/
'''

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (QApplication, QDialog, QWidget, QPushButton, QVBoxLayout, QTreeWidget, QTreeWidgetItem)
from PyQt5 import QtCore, QtGui

import core.gui.waterfall as waterfall
import numpy as np

from pprint import pprint

class Waterfall(QWidget, waterfall.Ui_Waterfall):
    
    general_settings_signal = QtCore.pyqtSignal(list) #send list of plotting params
    
    def __init__(self, parent):
        super(Waterfall,self).__init__(parent)
        self.setupUi(self)
        
        #Button functions
        self.btn_apply_general_settings.clicked.connect(self.send_settings)
        self.patient_tree = self.create_patient_tree()
        self.data_viewer_container.addWidget(self.patient_tree)

    def closeEvent(self,event):
        #Override closeEvent so that we hide the window rather than exit so we don't lose data
        event.ignore()
        self.hide()
        
    def on_waterfall_data_signal(self,signal):
        self.waterfall_data = signal
        
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
                            'Cancer type'
                            ]
            self.headers_item = QTreeWidgetItem(self.headers)
            self.tree.setColumnCount(len(self.headers))
            self.tree.setHeaderItem(self.headers_item)
            self.root.setExpanded(True)
            #self.addItems()
            #self.tree.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
            #self.tree.header().setStretchLastSection(False)
            return self.tree

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
    
    def on_waterfall_data_signal(self,signal):
        self.waterfall_data = signal
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
        self.rect_locations = np.arange(len(self.waterfall_data['']))
        self.ax = self.figure.add_subplot(111)
        self.ax.axhline(y=20, linestyle='--', c='k', alpha=0.5, lw=2.0, label='twenty_percent')
        self.ax.axhline(y=-30, linestyle='--', c='k', alpha=0.5, lw=2.0, label='thirty_percent')
        self.ax.axhline(y=0, c='k', alpha=1, lw=2.0, label='zero_percent')
        self.ax.grid(color = 'k', axis = 'y', alpha=0.25)
        self.rects = self.ax.bar(self.rect_locations,self.waterfall_data[1])
        self.auto_label_responses(self.ax, self.rects, self.waterfall_data)
        self.plot_table()
        self.canvas.draw()
        self.ax.hold(False) #rewrite the plot when plot() called
            
    def plot_table(self):
        rows = ['%s' % x for x in ('Baseline ECOG','Baseline metastasis', 'Baseline albumin','Baseline hemoglobin')]
        columns = self.waterfall_data[0] #patient numbers
        cell_text = []
        for row in range(len(rows)):
            cell_text_temp = []
            for col in columns:
                cell_text_temp.append('x')
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
                    '%s' % waterfall_data[2][i], ha='center', va=valign)
            i+=1