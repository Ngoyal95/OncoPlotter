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

from PyQt5.QtWidgets import (QColorDialog, QHeaderView, QApplication, QDialog, QWidget, QPushButton, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QComboBox)
from PyQt5 import QtCore, QtGui

import core.gui.waterfall as waterfall
import numpy as np
import shelve
from pprint import pprint

class CustomCombo(QComboBox):
    def __init__(self,parent,bar_keys_colors,response_type):
        super(QComboBox,self).__init__(parent)
        
        #keys is a dictionary: {'key description':color,...}
        self.dict_of_keys = bar_keys_colors
        self.response_type = response_type
        self.populate()

    def populate(self):
        '''Override method to add items to list'''
        for key in list(self.dict_of_keys.keys()):
            self.pixmap = QtGui.QPixmap(20,20)
            self.pixmap.fill(QtGui.QColor(self.dict_of_keys[key]))
            self.color_icon = QtGui.QIcon(self.pixmap)
            self.addItem(self.color_icon,key)
        self.setCurrentIndex(self.findText(self.response_type,flags=QtCore.Qt.MatchExactly)) #default to the patient cancer type

class Waterfall(QWidget, waterfall.Ui_Waterfall):
    
    plot_settings_signal = QtCore.pyqtSignal(list) #send list of plotting params
    updated_rectangles_signal = QtCore.pyqtSignal(list) #send list of updated artists for redrawing

    def __init__(self, parent):
        super(Waterfall,self).__init__(parent)
        self.setupUi(self)
        
        self.get_settings()

        #Button functions
        self.btn_apply_general_settings.clicked.connect(self.send_settings)
        self.btn_apply_keys_and_colors_settings.clicked.connect(self.send_settings)
        self.patient_tree = self.create_patient_tree()
        self.data_viewer_container.addWidget(self.patient_tree)
        self.btn_color_test.clicked.connect(self.get_color)
        
    def get_color(self):
        self.color = QColorDialog.getColor() #returns a color object
        print(color)

    def get_settings(self):
        ##########################################################
        '''NEED TO FIX THIS - CHANGE HOW THIS DATA IS LOADED '''
        ##########################################################
        # try:
        #     with shelve.open('WaterfallSettings') as shelfFile: 
        #         self.keys_and_colors = shelfFile['keys_and_colors']
        #         shelfFile.close()
        # except:
        #     #set and use default settings
        #     self.keys_and_colors = {
        #                             'CR':'#03945D',
        #                             'PR':'#B1EE97',
        #                             'PD':'#FF6F69',
        #                             'SD':'#707070',
        #                             'a':'r',
        #                             'b':'g',
        #                             'c':'b'
        #                             }
        #     with shelve.open('WaterfallSettings') as shelfFile:
        #         shelfFile['keys_and_colors'] = self.keys_and_colors
        #         shelfFile.close()
        self.keys_and_colors = {
                                'CR':'#03945D',
                                'PR':'#B1EE97',
                                'PD':'#FF6F69',
                                'SD':'#707070',
                                'a':'#FF0000',
                                'b':'#00FF00',
                                'c':'#0000FF'
                                }
        
    def on_waterfall_data_signal(self,signal):
        self.waterfall_data = signal['waterfall_data'] #pandas dataframe
        
    def on_generated_rectangles_signal(self,signal):
        print(signal[1])
        self.rectangles_received = signal[0]
        self.keys_received = signal[1]
        self.add_items() #display in table
        self.btn_apply_general_settings.setEnabled(True)
        self.btn_finalize_plot.setEnabled(True)
        self.btn_apply_keys_and_colors_settings.setEnabled(True)

    def send_settings(self):
        '''
        Emit both general plot settings, and color labeling settings. These are the settings to be used when the plot is created.
        
        '''
        self.general_settings = [
                                        self.plot_title.text(),
                                        self.x_label.text(),
                                        self.y_label.text(),
                                        [self.twenty_percent_line.isChecked(),
                                        self.thirty_percent_line.isChecked(),
                                        self.zero_percent_line.isChecked()],
                                        [self.display_responses_as_text.isChecked(),
                                        self.display_responses_as_color.isChecked(),
                                        self.use_custom_keys.isChecked()],
                                        self.include_table.isChecked(),
                                        self.show_cancer_type.isChecked(),
                                        self.get_updated_color_coding()
                                    ]
        self.plot_settings_signal.emit(self.general_settings)

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
            self.tree.setItemWidget(self.rect_item, 4, CustomCombo(self,self.keys_and_colors,self.keys_received[i])) #send the label of the rectangle as the key to determine color
            self.rect_item.setFlags(self.rect_item.flags() | QtCore.Qt.ItemIsEditable)
            i+=1

    def get_updated_color_coding(self):
        tmp_updated_color_coding = []
        self.root = self.tree.invisibleRootItem()
        child_count = self.root.childCount()
        #return list of keys (children are iterated in order they were entered, which agrees with order of patient data in waterfall_data lists)
        return [self.tree.itemWidget(self.root.child(i),4).currentText() for i in range(child_count)]

    def on_updated_tree_item(self):
        #update the rectangle which was edited
        pass

class WaterfallPlotter(QWidget):

    generated_rectangles_signal = QtCore.pyqtSignal(list) #send list of rects for data display in tree

    def __init__(self,parent):
        super(WaterfallPlotter,self).__init__(parent)

        self.get_settings()
        self.settings_update = False

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas,self)

        self.btn_plot = QPushButton('Default Plot')
        self.btn_plot.clicked.connect(self.plot)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.btn_plot)
        self.setLayout(self.layout)
        
    
    def on_waterfall_data_signal(self,signal):
        self.waterfall_data = signal['waterfall_data'] #pandas dataframe
        self.btn_plot.setEnabled(True)

    def get_settings(self):
        ##########################################################
        '''NEED TO FIX THIS - CHANGE HOW THIS DATA IS LOADED '''
        ##########################################################
        # try:
        #     with shelve.open('WaterfallSettings') as shelfFile: 
        #         self.keys_and_colors = shelfFile['keys_and_colors']
        #         shelfFile.close()
        # except:
        #     #set and use default settings
        #     self.keys_and_colors = {
        #                             'CR':'#03945D',
        #                             'PR':'#B1EE97',
        #                             'PD':'#FF6F69',
        #                             'SD':'#707070',
        #                             'a':'r',
        #                             'b':'g',
        #                             'c':'b'
        #                             }
        #     with shelve.open('WaterfallSettings') as shelfFile:
        #         shelfFile['keys_and_colors'] = self.keys_and_colors
        #         shelfFile.close()
        self.keys_and_colors = {
                                'CR':'#03945D',
                                'PR':'#B1EE97',
                                'PD':'#FF6F69',
                                'SD':'#707070',
                                'a':'#FF0000',
                                'b':'#00FF00',
                                'c':'#0000FF'
                                }

    def on_general_settings_signal(self,signal):
        self.gen_settings = signal
        self.settings_update = True
        self.plot()
    
    def get_bar_colors(self,responses):
        return [self.keys_and_colors[x] for x in responses]

    def plot(self):
        '''
        Plot waterfall data
        '''            
        self.figure.clear()
        self.rect_locations = np.arange(len(self.waterfall_data['Best response percent change']))
        self.ax = self.figure.add_subplot(111)
        self.patches = []
        self.bar_labels = self.waterfall_data['Overall response']

        if self.settings_update == False:
            self.ax.tick_params(
                            axis='x',          # changes apply to the x-axis
                            which='both',      # both major and minor ticks are affected
                            bottom='on',      # ticks along the bottom edge are off
                            top='on',         # ticks along the top edge are off
                            labelbottom='on'
                            ) # labels along the bottom edge are off
            self.ax.axhline(y=20, linestyle='--', c='k', alpha=0.5, lw=2.0, label='twenty_percent')
            self.ax.axhline(y=-30, linestyle='--', c='k', alpha=0.5, lw=2.0, label='thirty_percent')
            self.ax.axhline(y=0, c='k', alpha=1, lw=2.0, label='zero_percent')
            self.ax.grid(color = 'k', axis = 'y', alpha=0.25)
            used_keys = list(set(self.waterfall_data['Overall response']))
            self.bar_colors = self.get_bar_colors(self.waterfall_data['Overall response'])
            self.rects = self.ax.bar(self.rect_locations, self.waterfall_data['Best response percent change'], color=self.bar_colors, label=self.waterfall_data['Overall response'])
            for key in used_keys:
                self.patches.append(mpatches.Patch(color = self.keys_and_colors[key],label=key))
            self.ax.legend(handles=self.patches)
        else:
            self.ax.legend([])
            #settings were updated, we received them and stored in variable self.gen_settings
            self.ax.set_title(self.gen_settings[0])
            self.ax.set_xlabel(self.gen_settings[1])
            self.ax.set_ylabel(self.gen_settings[2])
            if self.gen_settings[3][0]:
                self.ax.axhline(y=20, linestyle='--', c='k', alpha=0.5, lw=2.0, label='twenty_percent')
            if self.gen_settings[3][1]:
                self.ax.axhline(y=-30, linestyle='--', c='k', alpha=0.5, lw=2.0, label='thirty_percent')
            if self.gen_settings[3][2]:
                self.ax.axhline(y=0, c='k', alpha=1, lw=2.0, label='zero_percent')

            if self.gen_settings[4][0]:
                #show responses as labels, default color bars
                #legend depends on user specified keys
                self.rects = self.ax.bar(self.rect_locations, self.waterfall_data['Best response percent change'], label=self.waterfall_data['Overall response'])
                self.add_labels(self.ax, self.rects, self.waterfall_data, 1)
            elif self.gen_settings[4][1]:
                #color bars with response type
                used_keys = list(set(self.waterfall_data['Overall response']))
                self.bar_colors = self.get_bar_colors(self.waterfall_data['Overall response'])
                self.rects = self.ax.bar(self.rect_locations, self.waterfall_data['Best response percent change'], color=self.bar_colors, label=self.waterfall_data['Overall response'])
                for key in used_keys:
                    self.patches.append(mpatches.Patch(color = self.keys_and_colors[key],label=key))
                self.ax.legend(handles=self.patches)
            elif self.gen_settings[4][2]:
                #response not shown as color coding, custom color code the bars
                self.bar_labels = self.gen_settings[7]
                self.bar_colors = self.get_bar_colors(self.gen_settings[7])
                used_keys = list(set(self.gen_settings[7]))
                self.rects = self.ax.bar(self.rect_locations, self.waterfall_data['Best response percent change'], color=self.bar_colors, label=self.gen_settings[7])
                for key in used_keys:
                    self.patches.append(mpatches.Patch(color = self.keys_and_colors[key],label=key))
                self.ax.legend(handles=self.patches)
            else:
                self.rects = self.ax.bar(self.rect_locations, self.waterfall_data['Best response percent change'], label=self.waterfall_data['Overall response'])
            
            #add table
            if self.gen_settings[5]:
                self.plot_table()
            
            #add labeling (response type or cancer type)
            if self.gen_settings[6] and ~self.gen_settings[4][0]:
                self.add_labels(self.ax, self.rects, self.waterfall_data, 0)
            
        self.ax.grid(color = 'k', axis = 'y', alpha=0.25)
        self.canvas.draw()
        self.generated_rectangles_signal.emit([self.rects, self.bar_labels])
            
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
                        
    def add_labels(self, ax, rects, waterfall_data, label_type):
        '''
        Add labels above/below bars. label_type == 1 --> display responses; == 0 --> display cancer type
        '''
        i = 0
        if label_type:
            for rect in rects:
                height = rect.get_height()
                if height >= 0:
                    valign = 'bottom'
                else:
                    valign = 'top'
                    
                ax.text(rect.get_x() + rect.get_width()/2., height,
                        '%s' % waterfall_data['Overall response'][i], ha='center', va=valign)
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
                        '%s' % waterfall_data['Cancer'][i], ha='center', va=valign, rotation='vertical')
                i+=1   