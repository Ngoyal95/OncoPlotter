from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rc

from PyQt5.QtWidgets import (QFontDialog, QListWidgetItem, QColorDialog, QHeaderView, QApplication, QDialog, QWidget, QPushButton, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QComboBox)
from PyQt5 import QtCore, QtGui

import core.gui.waterfall as waterfall
import numpy as np
import shelve
import re
import pandas as pd
from pprint import pprint

import core.gui.spider as spider

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
      

class Spider(QWidget, spider.Ui_Spider):

    general_settings_signal = QtCore.pyqtSignal(list)
    updated_keys_events_and_colors_signal = QtCore.pyqtSignal(list)

    def __init__(self, parent):
        super(Spider,self).__init__(parent)
        self.setupUi(self)
        self.initialize_settings()

        self.patient_tree = self.create_patient_tree()
        self.data_viewer_container.addWidget(self.patient_tree)
        
        #button functions
        self.btn_apply_general_settings.clicked.connect(self.send_settings)

    #### Initialization functions ####
    def initialize_settings(self):
        '''
        Load stored settings for keys and colors
        '''
        with shelve.open('SpiderSettings') as shelfFile: 
            self.keys_and_colors = shelfFile['KeysColors']
            self.events_keys_and_colors = shelfFile['EventsColors']
            self.events_markers = shelfFile['EventMarkers']
            shelfFile.close()
    
    #### Signal functions ####
    def on_spider_data_signal(self,signal):
        self.spider_data = signal['spider_data']

    def on_generated_series_signal(self,signal):
        self.series_received = signal[0] #patient plots
        self.responses_received = signal[1] #used to populate tree
        self.events_received = signal[2] #used to populate tree, lists of events per patient
        self.add_items()
        self.btn_apply_general_settings.setEnabled(True)

    def send_settings(self):
        '''
        Used to send plotting information (keys, events and their markers, and associated colors for both keys and events) to the SpiderPlotter widget
        '''
        self.general_settings = [
                                self.plot_title.text(),
                                self.x_label.text(),
                                self.y_label.text(),
                                self.get_updated_responses(),
                                self.get_updated_events()
                                ]
        self.updated_keys_events_and_colors_signal.emit([self.keys_and_colors,self.events_keys_and_colors,self.events_markers])
        self.general_settings_signal.emit(self.general_settings)

    #### Patient tree viewer related functions ####
    def create_patient_tree(self):
        '''
        Create QTreeWidget populated with patient's data
        '''
        self.tree = QTreeWidget()
        self.root = self.tree.invisibleRootItem()
        self.headers = [
                        'Patient #',
                        'Cancer',
                        'Best response',
                        'Color key',
                        'Time from baseline',
                        'Tumor burden % change',
                        'Event'
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
        self.tree.clear() #clear tree prior to entering items to prevent aggregation
        i=0
        for i in range(len(self.series_received)):
            self.pt_series = self.series_received[i][0]
            self.pt_item = QTreeWidgetItem(self.root)
            #store values to be added to treeitem in a list, None values are placeholders for combobox items
            self.pt_params = [
                            i,
                            self.spider_data[i][len(self.spider_data)-1],
                            self.spider_data[i][len(self.spider_data)-1],
                            None,
                            self.pt_series.get_xdata(orig=True),
                            self.pt_series.get_ydata(orig=True),
                            None
                            ]
            for col in range(3):
                #add pt info to the patient item
                self.pt_item.setText(col,str(self.pt_params[col]))
                self.pt_item.setTextAlignment(col,4)
            self.tree.setItemWidget(self.pt_item, 3, Combo_Keys_and_Colors(self,self.keys_and_colors,self.responses_received[i]))
            
            #now need to add child items for each timepoint
            for j in range(len(self.pt_params[4])):
                self.exam_item = QTreeWidgetItem(self.pt_item)
                for col in range(4,len(self.headers)-1):
                    self.insert_str = str(self.pt_params[col][j])
                    if self.insert_str.lower() == 'nan':
                        self.insert_str = '-'
                    self.exam_item.setText(col, self.insert_str)
                self.tree.setItemWidget(self.exam_item, len(self.headers)-1, Combo_Events(self,self.events_keys_and_colors,self.events_received[i][j]))

    def update_tree(self):
        '''
        Used to update the patient viewer tree with the new key names, marker names, and colors
        '''
        self.add_items() #update the tree with new keys and colors

    def get_updated_responses(self):
        '''
        Used to get list of updated patient responses to send to the plotter widget
        '''
        self.root = self.tree.invisibleRootItem()
        child_count = self.root.childCount()
        #return list of keys for patients
        return [self.tree.itemWidget(self.root.child(i),3).currentText() for i in range(child_count)]

    def get_updated_events(self):
        '''
        Used to get updated list of lists for events for each patient to send to the plotter widget
        '''
        temp_list_of_patient_events = []
        self.root = self.tree.invisibleRootItem()
        child_count = self.root.childCount()
        for i in range(child_count):
            temp_event_list = []
            event_count = self.root.child(i).childCount()
            temp_event_list = [
                                self.tree.itemWidget(self.root.child(i).child(j),6).currentText() 
                                if (self.root.child(i).child(j).text(5) is not '-' and self.tree.itemWidget(self.root.child(i).child(j),6).currentText() is not '') 
                                else None for j in range(event_count)
                                ]
            temp_list_of_patient_events.append(temp_event_list)
        return temp_list_of_patient_events

class SpiderPlotter(QWidget):
    
    generated_series_signal = QtCore.pyqtSignal(list)

    def __init__(self,parent):
        super(SpiderPlotter,self).__init__(parent)

        #initialize
        self.initialize_settings()
        self.settings_update = False

        #creating plotting widget
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas,self)
        self.btn_plot = QPushButton('Create Default Plot (RESET)')
        self.btn_plot.clicked.connect(self.default_plot)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.btn_plot)
        self.setLayout(self.layout)
    
    #### Initialization functions ####
    def initialize_settings(self):
        '''
        Load stored settings for keys and colors
        '''
        with shelve.open('SpiderSettings') as shelfFile: 
            self.keys_and_colors = shelfFile['KeysColors']
            self.events_keys_and_colors = shelfFile['EventsColors']
            self.events_markers = shelfFile['EventMarkers']
            shelfFile.close()

    #### Signal functions ####
    def on_spider_data_signal(self,signal):
        self.spider_data = signal['spider_data']
        self.x_axis_marks = self.spider_data.ix[:len(self.spider_data)-3,0] #all but last row, 0th column of the dataframe is the time from baseline measurement
        self.y_axis_marks = self.spider_data.ix[:len(self.spider_data)-3,1:]
        self.num_of_timepoints = len(self.x_axis_marks)
        self.number_of_series = len(self.spider_data.columns)-1 #remaining columns are for tumor burden percent changes
        self.patient_responses = self.spider_data.ix[len(self.spider_data)-2,1:]
        self.patient_events = [[None]*self.num_of_timepoints]*self.number_of_series
    
    def on_general_settings_signal(self,signal):
        self.plot_titles = signal[0:3]
        self.patient_responses = signal[3]
        self.patient_events = signal[4]
        self.settings_update = True
        self.plot()
    
    def on_updated_keys_events_and_colors(self,signal):
        #self.keys_and_colors = signal[0]
        #self.events_keys_and_colors = signal[1]
        #self.events_markers = signal[2]
        pass

    #### Plotting functions ####
    def default_plot(self):
        self.settings_update = False
        self.plot()

    def plot(self):
        '''
        Plot spider data
        '''
        markersize = 2
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        
        self.patient_cancers = self.spider_data.ix[len(self.spider_data)-1,:]
        self.series = [] #list of the series being plotted
        self.patches = [] #used for legend

        if self.settings_update == False:
            #standard plot, replotted when 'Create Default Plot (RESET)' is clicked
            for i in range(0,self.number_of_series):
                self.pt_series = [x for x in self.y_axis_marks.ix[:,i] if x is not 'Nan']
                clr = self.keys_and_colors[self.spider_data.ix[len(self.spider_data)-2,1:][i]]
                self.series.append(self.ax.plot(self.x_axis_marks,self.pt_series, linestyle='solid', linewidth='2', color=clr, marker='o'))
            
            used_keys = list(set(self.spider_data.ix[len(self.spider_data)-2,1:]))
            for key in used_keys:
                self.patches.append(mpatches.Patch(color=self.keys_and_colors[key],label=key))
            self.ax.legend(handles=self.patches)
            self.generated_series_signal.emit([self.series,self.spider_data.ix[len(self.spider_data)-2,1:],[[None]*self.num_of_timepoints]*self.number_of_series])
            
        else:
            self.ax.legend([])
            self.ax.set_title(self.plot_titles[0])
            self.ax.set_xlabel(self.plot_titles[1])
            self.ax.set_ylabel(self.plot_titles[2])

            #plot data with color coding
            for i in range(0,self.number_of_series):
                self.pt_series = [x for x in self.y_axis_marks.ix[:,i] if x is not 'Nan']
                clr = self.keys_and_colors[self.patient_responses[i]]
                self.series.append(self.ax.plot(self.x_axis_marks,self.pt_series, linestyle='solid', linewidth='2', color=clr, marker='o'))
            
            #make legend
            used_keys = list(set(self.patient_responses))
            for key in used_keys:
                self.patches.append(mpatches.Patch(color=self.keys_and_colors[key],label=key))
            self.ax.legend(handles=self.patches)
            self.generated_series_signal.emit([self.series,self.patient_responses,self.patient_events])

            #plot events with color coding
            for i in range(len(self.pt_series)):
                self.pt_event_locations = [x if x is not 'Nan' else 0 for x in self.y_axis_marks.ix[:,i]] #can't plot if y location is a string
                self.pt_event_colors = [self.events_keys_and_colors[x] for x in self.patient_events[i]]
                self.pt_event_markers = [self.events_markers[x] for x in self.patient_events[i]]

                for m, c, x, y in zip(self.pt_event_markers,self.pt_event_colors,self.x_axis_marks,self.pt_event_locations):
                    self.ax.plot(x,y,marker=m,c=c)

        self.ax.grid(color = 'k', axis = 'y', alpha=0.25)
        self.canvas.draw()

    #### Miscellaneous functions ####