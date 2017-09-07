'''
Refs:
Embedding plot: https://sukhbinder.wordpress.com/2013/12/16/simple-pyqt-and-matplotlib-example-with-zoompan/

General notes:
1) The plot updating mechanism works as follows:
    a) a default plot is created
        ai) then user is allowed to make edits
    b) edits are sent to the WaterfallPlotter widget, which then redraws the plot using the new information
        bi) this includes axis labels, color coding, and which lines to include (0,20,-30)
    c) after the plot is redrawn, the data is sent BACK to the Waterfall module for updating the viewer tree
    d) process then repeats, the widgets update eachother by taking turns

'''

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rc

from PyQt5.QtWidgets import (QFontDialog, QListWidgetItem, QColorDialog, QHeaderView, QApplication, QDialog, QWidget, QPushButton, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QComboBox)
from PyQt5 import QtCore, QtGui

import numpy as np
import shelve
import re
from pprint import pprint

import core.gui.waterfall as waterfall
from core.gui.custom_widgets import ColorButton, Combo_Events, Combo_Keys_and_Colors

class Waterfall(QWidget, waterfall.Ui_Waterfall):
    
    plot_signal = QtCore.pyqtSignal(list) #send list of plotting params

    def __init__(self, parent):
        super(Waterfall,self).__init__(parent)
        
        #Initialize
        self.setupUi(self)
        self.initialize_settings()
        
        self.patient_tree = self.create_patient_tree()
        self.data_viewer_container.addWidget(self.patient_tree) #create tree (returned by function) and add tree to viewer
        
        self.populate_keys_and_colors_view()
        
        self.btn_get_color = ColorButton(self,'#a4e9ff')
        self.color_btn_container.addWidget(self.btn_get_color)

        #Button functions
        self.btn_plot.clicked.connect(self.send_plot_signal) #apply general settings, update keys/colors, and replot
        self.btn_add_key.clicked.connect(self.add_key_to_list)
        self.btn_default_settings.clicked.connect(self.set_default_keys_and_colors)

    #### Initialization functions ####
    def initialize_settings(self):
        '''
        Load stored settings for keys and colors
        '''
        with shelve.open('WaterfallSettings') as shelfFile:
            self.default_keys_and_colors = shelfFile['UserSettings']
            self.keys_and_colors = shelfFile['UserSettings']
            shelfFile.close()

    #### Signal functions ####
    def on_waterfall_data_signal(self,signal):
        self.waterfall_data = signal['waterfall_data'] #pandas dataframe
        self.bar_heights = self.waterfall_data['Percent change']
        self.bar_locations = np.arange(len(self.waterfall_data['Percent change']))        
        self.responses = self.waterfall_data['Overall response']
        self.keys = self.responses #initially, assume color coding according to response type, but change keys if diff color coding
        self.default_labels = self.waterfall_data['Cancer'] #default label is the cancer type
        self.labels = self.waterfall_data['Cancer']
        self.btn_plot.setEnabled(True)

    def send_plot_signal(self):
        '''
        Emit both general plot settings, and color labeling settings. These are the settings to be used when the plot is created.
        '''
        self.values = [
                        self.bar_locations,
                        self.bar_heights,
                        self.keys, #custom key to override color coding
                        self.responses, #patient response, used for standard color coding
                        self.labels,
                        self.waterfall_data
        ]
        self.settings = {
                        'titles':[
                                self.plot_title.text(),
                                self.x_label.text(),
                                self.y_label.text()
                        ],
                        'lines':
                        [
                                self.twenty_percent_line.isChecked(),
                                self.zero_percent_line.isChecked(),
                                self.thirty_percent_line.isChecked(),
                                self.show_grid.isChecked()
                        ],
                        'labels':[
                                self.display_responses_as_text.isChecked(),
                                self.display_responses_as_color.isChecked(),
                                self.use_custom_keys.isChecked(),
                                self.show_cancer_type.isChecked()
                        ],
                        'general':[
                                self.spin_fontsize.value(),
                                self.outline_bars.isChecked(),
                                self.show_legend.isChecked(),
                                self.include_table.isChecked(),
                                self.y_tick_interval.value()
                        ]
        }
        self.keys_colors = [
                        self.keys_and_colors
        ]
        self.plot_signal.emit([
                            self.values,
                            self.settings,
                            self.keys_colors
        ])

    #### Patient tree viewer related functions ####
    def create_patient_tree(self):
        '''
        Create QTreeWidget populated with a patient's data for the DataEntry dialog.
        '''
        self.tree = QTreeWidget()
        self.root = self.tree.invisibleRootItem()
        self.headers = [
                        'Patient #',
                        'Best response %',
                        'Response',
                        'Cancer',
                        'Color key',
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
        for bar in self.bar_heights:
            #populate editable tree with rect data
            self.rect_item = QTreeWidgetItem(self.root)
            self.rect_params = [
                                self.waterfall_data['Patient number'][i], 
                                self.bar_heights[i],
                                self.waterfall_data['Overall response'][i],
                                self.waterfall_data['Cancer'][i]
                                ]
            for col in range(0,4):
                self.rect_item.setText(col,str(self.rect_params[col]))
                self.rect_item.setTextAlignment(col,4)
            self.tree.setItemWidget(self.rect_item, 4, Combo_Events(self,self.keys_and_colors,self.patient_response[i])) #send the label of the rectangle as the key to determine color
            self.rect_item.setFlags(self.rect_item.flags() | QtCore.Qt.ItemIsEditable)
            i+=1

    def update_tree(self):
        '''
        Used to update the patient viewer tree with new key names and colors
        '''
        self.add_items() #update the tree with new keys and colors

    #### Custom keys and colors functions ####
    def populate_keys_and_colors_view(self):
        if hasattr(self,'tree_keys_and_colors'):
            self.tree_keys_and_colors.setParent(None)
            del self.tree_keys_and_colors
            self.tree_keys_and_colors = self.create_keys_and_colors_tree()
            self.keys_and_colors_container.addWidget(self.tree_keys_and_colors)
        else:
            self.tree_keys_and_colors = self.create_keys_and_colors_tree()
            self.keys_and_colors_container.addWidget(self.tree_keys_and_colors)

    def create_keys_and_colors_tree(self):
        '''
        Populate the keys and colors tree (self.list_keys_and_colors) with values in self.keys_and_colors
        '''
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

    def add_key_to_list(self):
        '''
        Add a key to the list when self.btn_add_key is pressed. Color obtained from self.btn_get_color
        '''
        self.key_to_add = self.key_name.text()
        self.color_to_add = self.btn_get_color.give_color()

        if re.search('[a-zA-Z0-9]', self.key_to_add):
            self.key_name.clear() #clear lineedit
            self.keys_and_colors[self.key_to_add] = self.color_to_add
            self.populate_keys_and_colors_view()
            self.update_tree()
        
    def update_keys_and_colors(self):
        '''
        Update self.keys_and_colors and send settings (call self.send_settings()) to reflect changes in plot
        '''
        self.root_keys_and_colors = self.tree_keys_and_colors.invisibleRootItem()
        child_count = self.root_keys_and_colors.childCount()
        for i in range(child_count):
            child = self.root_keys_and_colors.child(i)
            self.key_update = child.text(0)
            self.color_update = self.tree_keys_and_colors.itemWidget(child,1)
            self.keys_and_colors[self.key_update] = self.color_update.give_color()
        self.send_settings()
        self.update_tree() #note, we update tree after sending settings so that the tree now reflects any changes in key/color changes in dropdowns
        #if we do update_tree() before sending, the tree will not properly reflect changes in dropdowns, and changes in key will not appear in plot

    def set_default_keys_and_colors(self):
        '''
        Return the default keys (CR,PR,PD,SD) to their original colors
        '''
        temp_shelf = shelve.open('WaterfallSettings')
        temp_settings = temp_shelf['DefaultSettings']
        temp_shelf.close()
        for key in temp_settings.keys():
            self.keys_and_colors[key] = temp_settings[key]

        self.populate_keys_and_colors_view()
        self.update_keys_and_colors()

    #### Miscellaneous functions ####
    def get_updated_color_coding(self):
        self.root = self.tree.invisibleRootItem()
        child_count = self.root.childCount()
        #return list of keys (children are iterated in order they were entered, which agrees with order of patient data in waterfall_data lists)
        return [self.tree.itemWidget(self.root.child(i),4).currentText() for i in range(child_count)]

class WaterfallPlotter(QWidget):
    def __init__(self,parent):
        super(WaterfallPlotter,self).__init__(parent)
        
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
    
    #### Plot data extraction functions and plot ####
    def extract_plot_data(self,data):
        '''
         Pull out plotting data (bar locations, bar lengths, responses
        '''
        self.bar_locations = data[0]
        self.bar_heights = data[1]
        self.keys = data[2]
        self.responses = data[3]
        self.labels = data[4]
        self.waterfall_data = data[5]

    def extract_formatting_data(self,data):
        '''
        Pull out formatting data (titles, fontsize, markersize, show grid/lines or not, etc..)
        '''
        self.titles = data['titles']
        self.line_settings = data['lines']
        self.label_settings = data['labels']
        self.general_settings = data['general']

    def extract_indicators(self,data):
        '''
        Get formatting info (keys and colors info)
        '''
        self.keys_and_colors = data[0]

    def plot(self):
        '''
        Plot waterfall data
        '''
        self.bar_width = 0.9
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.patches = []
        self.ax.legend([])
        self.edge_color = 'k'

        self.bar_colors = self.get_bar_colors(self.keys)
        self.ax.set_title(self.titles[0], fontsize=self.general_settings[0])
        self.ax.set_xlabel(self.titles[1], fontsize=self.general_settings[0])
        self.ax.set_ylabel(self.titles[2], fontsize=self.general_settings[0])

        self.ax.axhline(y=20, linestyle='--', c='k', alpha=self.line_settings[0]/2.0, lw=2.0, label='twenty_percent')
        self.ax.axhline(y=0, c='k', alpha=self.line_settings[1], lw=2.0, label='zero_percent')
        self.ax.axhline(y=-30, linestyle='--', c='k', alpha=self.line_settings[2]/2.0, lw=2.0, label='thirty_percent')
        self.ax.grid(color = 'k', axis = 'y', alpha=self.line_settings[3]/4.0)
      
        if ~self.general_settings[1]:
            self.edge_color = ''
        if self.general_settings[2]:
            self.ax.legend(handles=self.patches)
        if self.general_settings[3]:
            self.plot_table()

        #legend
        if self.label_settings[1]: #show responses as colors
            used_keys = list(set(self.responses))
        elif self.label_settings[2]: #use custom keys
            used_keys = list(set(self.keys))
        for key in used_keys:
            self.patches.append(mpatches.Patch(color = self.keys_and_colors[key],label=key))

        self.rects = self.ax.bar(left=self.bar_locations, height=self.bar_heights, color=self.bar_colors)

        if self.label_settings[0]: #show responses as text
            self.add_labels(self.ax, self.rects, self.responses, 1)
        if self.label_settings[3]: #show custom label (default is cancer type)
            self.add_labels(self.ax, self.rects, self.labels, 0)
                    
        self.canvas.draw()
            
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
        the_table = self.ax.table(cellText=cell_text, rowLabels=rows, colLabels=columns, loc='bottom', cellLoc='center', colLoc='center')
        plt.subplots_adjust(bottom=0.15,left=0.5)
        self.ax.set_xlim(-0.5,len(columns)-0.5)
        self.ax.tick_params(
                        axis='x',          # changes apply to the x-axis
                        which='both',      # both major and minor ticks are affected
                        bottom='off',      # ticks along the bottom edge are off
                        top='off',         # ticks along the top edge are off
                        labelbottom='off'
                        ) # labels along the bottom edge are off
                        
    def add_labels(self, ax, rects, labels, label_type):
        '''
        Add labels above/below bars. label_type == 1 --> display responses; == 0 --> display cancer type
        '''
        i = 0
        if label_type:
            for rect in rects:
                height = rect.get_height()
                if height >= 0:
                    hgt = height
                    valign = 'bottom'
                else:
                    hgt = height-0.25
                    valign = 'top'
                    
                ax.text(rect.get_x() + rect.get_width()/2., hgt,
                        '%s' % labels[i], ha='center', va=valign)
                i+=1
        else:
            for rect in rects:
                height = rect.get_height()
                if height >= 0:
                    valign = 'top'
                    hgt = -1
                else:
                    valign = 'bottom'
                    hgt = 1

                ax.text(rect.get_x() + rect.get_width()/2., hgt,
                        '%s' % labels[i], ha='center', va=valign, rotation='vertical')
                i+=1   

    #### Miscellaneous functions ####
    def get_bar_colors(self,keys):
        '''
        Used to get colors from the dictionary self.keys_and_colors based on the list of keys provided
        '''
        return [self.keys_and_colors[key] for key in keys]