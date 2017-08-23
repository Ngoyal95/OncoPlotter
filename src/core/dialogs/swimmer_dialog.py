from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rc

from PyQt5.QtWidgets import (QLabel, QFontDialog, QListWidgetItem, QColorDialog, QHeaderView, QApplication, QDialog, QWidget, QPushButton, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QComboBox)
from PyQt5 import QtCore, QtGui

import numpy as np
import shelve
import re
import os
from pprint import pprint

import core.gui.swimmer as swimmmer
from core.gui.custom_widgets import Combo_Keys_and_Colors, Combo_Events, Combo_Markers, ColorButton

mark_dict = {
".":"point",
",":"pixel",
"o":"circle",
"v":"triangle_down",
"^":"triangle_up",
"<":"triangle_left",
">":"triangle_right",
"1":"tri_down",
"2":"tri_up",
"3":"tri_left",
"4":"tri_right",
"8":"octagon",
"s":"square",
"p":"pentagon",
"*":"star",
"h":"hexagon1",
"H":"hexagon2",
"+":"plus",
"D":"diamond",
"d":"thin_diamond",
"|":"vline",
"_":"hline",
"":'no marker'
}

image_dir = os.path.dirname(os.path.abspath('../OncoPlot'))

class Swimmer(QWidget, swimmmer.Ui_Swimmer):

    plot_signal = QtCore.pyqtSignal(list)

    def __init__(self, parent):
        super(Swimmer,self).__init__(parent)
        self.setupUi(self)
        self.initialize_settings()

        #marker reference image
        self.marker_ref = QLabel()
        self.marker_pixmap = QtGui.QPixmap(os.path.join(image_dir,'images\markers_reference.png'))
        self.marker_ref.setPixmap(self.marker_pixmap)
        self.marker_reference_container.addWidget(self.marker_ref)
               
        #button functions
        self.btn_plot.clicked.connect(self.send_plot_signal)
        
        self.btn_default_keys.clicked.connect(self.default_keys)
        self.btn_default_markers.clicked.connect(self.default_markers)
        self.btn_add_key.clicked.connect(self.add_key)
        self.btn_add_event.clicked.connect(self.add_event)

        #Custom widgets
        self.marker_combo = Combo_Markers(self,mark_dict, None) #pass None for the default
        self.marker_combo_container.addWidget(self.marker_combo)

        self.btn_get_color = ColorButton(self,'#a4e9ff')
        self.key_color.addWidget(self.btn_get_color)

        self.btn_get_marker_color = ColorButton(self,'#a4e9ff')
        self.marker_color.addWidget(self.btn_get_marker_color)

    #### Initialization functions ####
    def initialize_settings(self):
        '''
        Load stored settings for keys and colors
        '''
        with shelve.open('SwimmerSettings') as shelfFile: 
            self.keys_and_colors = shelfFile['KeysColors']
            self.default_keys_and_colors = shelfFile['KeysColors']
            self.event_colors = shelfFile['EventsColors']
            self.event_markers = shelfFile['EventMarkers']
            shelfFile.close()

    #### Signal functions ####
    def on_swimmer_data_signal(self,signal):
        self.swimmer_data = signal['swimmer_data'] #pandas dataframe
        self.numcols = len(list(self.swimmer_data))
        self.bar_locations = np.arange(len(self.swimmer_data.iloc[:,0])) #list
        self.patients = list(self.swimmer_data.iloc[:,0])
        self.responses = list(self.swimmer_data.iloc[:,1])
        self.cancers = list(self.swimmer_data.iloc[:,2])
        self.stack_lengths = self.swimmer_data.iloc[:,3:self.numcols-1] #pandas dataframe, last column is the total time on treatment sum, don't include
        self.events = []

        self.dosage_staging_bool = dosage_staging(self.stack_lengths) #True if dosage staging is used, otherwise False

        self.populate_patient_tree()
        self.populate_keys_tree()
        self.populate_markers_tree()

    def send_plot_signal(self):
        '''
        Send all plotting information, signal plotter widget to plot
        '''
        self.values = [
                        self.bar_locations, 
                        self.stack_lengths,
                        self.responses,
                        self.events
                    ]
        self.settings = [
                        self.plot_title.text(),
                        self.x_label.text(),
                        self.y_label.text(),
                        self.spin_fontsize.value(),
                        self.spin_markersize.value(),
                        self.outline_bars.isChecked(),
                        self.show_events.isChecked(),
                        self.dosage_staging_bool
                        ]
        self.keys_markers_colors = [
                                self.keys_and_colors,
                                self.event_colors,
                                self.event_markers
                                ]
        self.plot_signal.emit([
                            self.values,
                            self.settings,
                            self.keys_markers_colors
                            ])

    #### Patient tree viewer related functions ####
    def create_patient_tree(self):
        '''
        Create QTreeWidget populated with patient's data
        '''
        self.tree_patients = QTreeWidget()
        self.root_patients = self.tree_patients.invisibleRootItem()
        self.headers = [
                        'Patient #',
                        'Cancer',
                        'Best response',
                        'Key',
                        'Timepoint',
                        'Event'
                        ]
        self.headers_item = QTreeWidgetItem(self.headers)
        self.tree_patients.setColumnCount(len(self.headers))
        self.tree_patients.setHeaderItem(self.headers_item)
        self.root_patients.setExpanded(True)
        self.tree_patients.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tree_patients.header().setStretchLastSection(False)
        return self.tree_patients

    def populate_patient_tree(self):
        tree = self.create_patient_tree()
        self.add_items()
        self.patient_tree_container.addWidget(tree)

    def add_items(self):
        '''
        Populate viewing tree
        '''
        self.tree_patients.clear() #clear tree prior to entering items to prevent aggregation
        i=0
        for i in range(len(self.patients)):
            self.pt_item = QTreeWidgetItem(self.root_patients)
            self.pt_params = [
                            self.patients[i],
                            self.cancers[i],
                            self.responses[i],
                            ]
            for col in range(3):
                self.pt_item.setText(col,str(self.pt_params[col]))
                self.pt_item.setTextAlignment(col,4)

    def update_tree(self):
        '''
        Used to update the patient viewer tree with the new key names, marker names, and colors
        '''
        self.add_items() #update the tree with new keys and colors

    def get_updated_responses(self):
        '''
        Used to get list of updated patient responses to send to the plotter widget
        '''
        pass
        self.root_patients = self.tree_patients.invisibleRootItem()
        child_count = self.root_patients.childCount()
        #return list of keys for patients
        return [self.tree_patients.itemWidget(self.root_patients.child(i),3).currentText() for i in range(child_count)]

    def get_updated_events(self):
        '''
        Used to get updated list of lists for events for each patient to send to the plotter widget
        '''
        pass
        temp_list_of_patient_events = []
        self.root_patients = self.tree_patients.invisibleRootItem()
        child_count = self.root_patients.childCount()
        for i in range(child_count):
            temp_event_list = []
            event_count = self.root_patients.child(i).childCount()
            temp_event_list = [
                                self.tree_patients.itemWidget(self.root_patients.child(i).child(j),6).currentText() 
                                if (self.root_patients.child(i).child(j).text(5) is not '-' and self.tree_patients.itemWidget(self.root_patients.child(i).child(j),6).currentText() is not '') 
                                else '' for j in range(event_count)
                                ]
            temp_list_of_patient_events.append(temp_event_list)
        return temp_list_of_patient_events

    #### Custom keys,markers,colors functions ####
    #create trees
    def create_keys_tree(self):
        self.tree_keys_and_colors = QTreeWidget()
        self.root_keys_and_colors = self.tree_keys_and_colors.invisibleRootItem()
        self.tree_keys_and_colors.setColumnCount(2)
        self.tree_keys_and_colors.setHeaderItem(QTreeWidgetItem(['Key','Color']))
        self.root_keys_and_colors.setExpanded(True)
        self.tree_keys_and_colors.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tree_keys_and_colors.header().setStretchLastSection(False)

        #initialize items in tree
        for key in self.keys_and_colors.keys():
            self.pixmap = QtGui.QPixmap(20,20)
            self.pixmap.fill(QtGui.QColor(self.keys_and_colors[key]))
            self.color_icon = QtGui.QIcon(self.pixmap)
            self.key_color_item = QTreeWidgetItem(self.root_keys_and_colors)
            self.key_color_item.setTextAlignment(0,4)
            self.key_color_item.setText(0,key)
            self.tree_keys_and_colors.setItemWidget(self.key_color_item,1,ColorButton(self,self.keys_and_colors[key])) #add custom button for color
            
        return self.tree_keys_and_colors

    def create_markers_tree(self):
        self.tree_markers_and_colors = QTreeWidget()
        self.root_markers_and_colors = self.tree_markers_and_colors.invisibleRootItem()
        self.tree_markers_and_colors.setColumnCount(3)
        self.tree_markers_and_colors.setHeaderItem(QTreeWidgetItem(['Event','Marker','Color']))
        self.root_markers_and_colors.setExpanded(True)
        self.tree_markers_and_colors.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tree_markers_and_colors.header().setStretchLastSection(False)

        #initialize items in tree
        for key in self.event_markers.keys():
            if key != '':
                self.pixmap = QtGui.QPixmap(20,20)
                self.pixmap.fill(QtGui.QColor(self.event_colors[key]))
                self.color_icon = QtGui.QIcon(self.pixmap)
                self.marker_item = QTreeWidgetItem(self.root_markers_and_colors)
                self.marker_item.setTextAlignment(0,4)
                self.marker_item.setText(0,key)
                #self.marker_item.setText(1,mark_dict[self.event_markers[key]]) #note, self.event_markers[key] returns the actual marker character, which can then be used to get the 'name'
                self.tree_markers_and_colors.setItemWidget(self.marker_item,1,Combo_Markers(self,mark_dict,mark_dict[self.event_markers[key]]))
                self.tree_markers_and_colors.setItemWidget(self.marker_item,2,ColorButton(self,self.event_colors[key])) #add custom button for color
                
        return self.tree_markers_and_colors

    #populate trees
    def populate_keys_tree(self):
        if hasattr(self,'keys_tree'):
            self.keys_tree.setParent(None)
            del self.keys_tree
            self.keys_tree = self.create_keys_tree()
            self.keys_and_colors_container.addWidget(self.keys_tree)
        else:
            self.keys_tree = self.create_keys_tree()
            self.keys_and_colors_container.addWidget(self.keys_tree)

    def populate_markers_tree(self):
        if hasattr(self,'markers_tree'):
            self.markers_tree.setParent(None)
            del self.markers_tree
            self.markers_tree = self.create_markers_tree()
            self.markers_and_colors_container.addWidget(self.markers_tree)
        else:
            self.markers_tree = self.create_markers_tree()
            self.markers_and_colors_container.addWidget(self.markers_tree)

    #Add key or marker
    def add_key(self):
        self.key_to_add = self.key_name.text()
        self.color_to_add = self.btn_get_color.give_color()

        if re.search('[a-zA-Z0-9]', self.key_to_add):
            self.key_name.clear() #clear lineedit
            self.keys_and_colors[self.key_to_add] = self.color_to_add
            self.populate_keys_tree()
            self.update_tree()

    def add_event(self):
        self.event_to_add = self.event_name.text()
        self.event_marker = self.marker_combo.give_marker()
        self.event_color = self.btn_get_marker_color.give_color()

        if re.search('[a-zA-Z0-9]', self.event_to_add):
            self.event_name.clear() #clear lineedit
            self.event_colors[self.event_to_add] = self.event_color
            self.event_markers[self.event_to_add] = self.event_marker
            self.populate_markers_tree()
            self.update_tree()

    #update dictionaries and plot
    def update_keys(self):
        '''
        Update self.keys_and_colors and send settings (call self.send_settings()) to reflect changes in plot
        '''
        self.keys_root = self.keys_tree.invisibleRootItem()
        child_count = self.keys_root.childCount()
        for i in range(child_count):
            child = self.keys_root.child(i)
            self.key_update = child.text(0)
            self.color_update = self.keys_tree.itemWidget(child,1).give_color()
            self.keys_and_colors[self.key_update] = self.color_update

    def update_events(self):
        '''
        Update self.event_colors and self.event_markers and send settings (call self.send_settings()) to reflect changes in plot
        '''
        self.markers_root = self.markers_tree.invisibleRootItem()
        child_count = self.markers_root.childCount()
        for i in range(child_count):
            child = self.markers_root.child(i)
            self.event_update = child.text(0)
            self.marker_update = self.markers_tree.itemWidget(child,1).give_marker()
            self.color_update = self.markers_tree.itemWidget(child,2).give_color()
            self.event_markers[self.event_update] = self.marker_update
            self.event_colors[self.event_update] = self.color_update
    
    def update_keys_and_events(self):
        self.update_events()
        self.update_keys()
        self.send_settings()
        self.update_tree()

    #default keys, markers, and colors
    def default_keys(self):
        '''
        Return the default keys (CR,PR,PD,SD) to their original colors
        '''
        temp_shelf = shelve.open('SwimmerSettings')
        temp_settings = temp_shelf['KeysColors']
        temp_shelf.close()
        for key in temp_settings.keys():
            self.keys_and_colors[key] = temp_settings[key]

        self.populate_keys_tree()
        self.update_keys()

    def default_markers(self):
        '''
        Return the default markers to their original colors
        '''
        temp_shelf = shelve.open('SwimmerSettings')
        temp_settings = temp_shelf['EventsColors']
        temp_shelf.close()
        for key in temp_settings.keys():
            self.event_colors[key] = temp_settings[key]
        self.populate_markers_tree()
        self.update_keys()


class SwimmerPlotter(QWidget):
    def __init__(self,parent):
        super(SwimmerPlotter,self).__init__(parent)

        #create plotting widget
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas,self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    #### Signal functions ####
    def on_plot_signal(self,signal):
        '''
        signal[0] is plot data, signal[1] is plot formatting data, and signal[2] is keys,markers,and colors data
        '''
        self.plot_data = signal[0]
        self.formatting_data = signal[1]
        self.indicators = signal[2]
        
        self.extract_plot_data(self.plot_data)
        self.extract_formatting_data(self.formatting_data)
        self.extract_indicators(self.indicators)

        self.plot()

    #### Plot data extraction functions ####
    def extract_plot_data(self,data):
        '''
        Pull out plotting data (bar locations, bar lengths, responses, and events)
        '''
        self.stack_locs = data[0]
        self.stack_lengths = data[1]
        self.responses = data[2]
        self.events = data[3]
        self.stack_offsets = [0]*len(self.stack_lengths.iloc[:,0])

    def extract_formatting_data(self,data):
        '''
        Pull out formatting data (titles, fontsize, markersize)
        '''
        self.plot_titles = data[0:3]
        self.fontsize = data[3]
        self.markersize = data[4]
        if data[5]:
            self.outline = 'k'
        else:
            self.outline = ''
        self.show_events = data[6]
        self.dosage_staging_bool = data[7]

    def extract_indicators(self,data):
        '''
        Get formatting information (key and marker info)
        '''
        self.keys_and_colors = data[0]
        self.event_colors = data[1]
        self.event_markers = data[2]

    def plot(self):
        '''
        Plot swimmer data
        '''
        self.bar_width = 0.9
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(color = 'k', axis = 'y', alpha=0.25)

        self.ax.legend([])
        self.ax.set_title(self.plot_titles[0], fontsize = self.fontsize)
        self.ax.set_xlabel(self.plot_titles[1], fontsize = self.fontsize)
        self.ax.set_ylabel(self.plot_titles[2], fontsize = self.fontsize)

        if self.dosage_staging_bool:
            #dosage staging used
            #take column headers from stacks dataframe, use them as labels for legend
            self.dosage_dict = {}
            for i in range(len(list(self.stack_lengths))):
                self.dosage_dict[list(self.stack_lengths)[i]] = self.keys_and_colors[['DL1','DL2','DL3','DL4','DL5'][i]] #mapping from column header (key) to color keys for dosages
                
            self.colors = [[self.dosage_dict[key]]*len(self.stack_lengths) for key in self.dosage_dict]                
        else:
            #color with custom keys, default to responses
            self.colors = get_bar_colors(self.keys_and_colors,self.responses)*5

        for i in range(len(list(self.stack_lengths))):
            self.ax.barh(self.stack_locs, self.stack_lengths.iloc[:,i], self.bar_width, color=self.colors[i], edgecolor=self.outline, left=self.stack_offsets)
            self.stack_offsets = [sum(x) for x in zip(self.stack_offsets, self.stack_lengths.iloc[:,i])]

        if self.show_events:
            #plot events
            pass

        self.canvas.draw()

def dosage_staging(stacks):
    '''
    Check the stacks dataframe to determine if multiple dosages occured, returns True if so
    '''
    uniques = stacks.apply(lambda x: x.nunique())
    for i in range(len(stacks.iloc[:,1])):
        if stacks.iloc[i,1] != 0:
            return True
    return False

def get_bar_colors(dict_to_use,keys):
    '''
    Used to get colors from the provided dict depending on keys passed
    '''
    return [dict_to_use[key] for key in keys]

def get_color_list(num_stacks,dosage_dict,keys_and_colors,responses):
    if num_stacks>1:
        dosage_dict
    else:
        return get_bar_colors(keys_and_colors,responses)*5