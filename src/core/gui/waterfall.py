# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'waterfall.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Waterfall(object):
    def setupUi(self, Waterfall):
        Waterfall.setObjectName("Waterfall")
        Waterfall.resize(518, 427)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Waterfall.sizePolicy().hasHeightForWidth())
        Waterfall.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Waterfall)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plot_settings = QtWidgets.QGroupBox(Waterfall)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_settings.sizePolicy().hasHeightForWidth())
        self.plot_settings.setSizePolicy(sizePolicy)
        self.plot_settings.setObjectName("plot_settings")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.plot_settings)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.plot_settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab.sizePolicy().hasHeightForWidth())
        self.tab.setSizePolicy(sizePolicy)
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.plot_title_layout = QtWidgets.QHBoxLayout()
        self.plot_title_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.plot_title_layout.setObjectName("plot_title_layout")
        self.label = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setObjectName("label")
        self.plot_title_layout.addWidget(self.label)
        self.plot_title = QtWidgets.QLineEdit(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_title.sizePolicy().hasHeightForWidth())
        self.plot_title.setSizePolicy(sizePolicy)
        self.plot_title.setObjectName("plot_title")
        self.plot_title_layout.addWidget(self.plot_title)
        self.verticalLayout_2.addLayout(self.plot_title_layout)
        self.x_label_layout = QtWidgets.QHBoxLayout()
        self.x_label_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.x_label_layout.setObjectName("x_label_layout")
        self.label_2 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.x_label_layout.addWidget(self.label_2)
        self.x_label = QtWidgets.QLineEdit(self.tab)
        self.x_label.setObjectName("x_label")
        self.x_label_layout.addWidget(self.x_label)
        self.verticalLayout_2.addLayout(self.x_label_layout)
        self.y_label_layout = QtWidgets.QHBoxLayout()
        self.y_label_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.y_label_layout.setObjectName("y_label_layout")
        self.label_3 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.y_label_layout.addWidget(self.label_3)
        self.y_label = QtWidgets.QLineEdit(self.tab)
        self.y_label.setObjectName("y_label")
        self.y_label_layout.addWidget(self.y_label)
        self.verticalLayout_2.addLayout(self.y_label_layout)
        self.twenty_percent_line_layout = QtWidgets.QHBoxLayout()
        self.twenty_percent_line_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.twenty_percent_line_layout.setObjectName("twenty_percent_line_layout")
        self.label_4 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.twenty_percent_line_layout.addWidget(self.label_4)
        self.twenty_percent_line = QtWidgets.QCheckBox(self.tab)
        self.twenty_percent_line.setText("")
        self.twenty_percent_line.setChecked(True)
        self.twenty_percent_line.setObjectName("twenty_percent_line")
        self.twenty_percent_line_layout.addWidget(self.twenty_percent_line)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.twenty_percent_line_layout.addItem(spacerItem)
        self.label_5 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.twenty_percent_line_layout.addWidget(self.label_5)
        self.thirty_percent_line = QtWidgets.QCheckBox(self.tab)
        self.thirty_percent_line.setText("")
        self.thirty_percent_line.setChecked(True)
        self.thirty_percent_line.setObjectName("thirty_percent_line")
        self.twenty_percent_line_layout.addWidget(self.thirty_percent_line)
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.twenty_percent_line_layout.addItem(spacerItem1)
        self.label_6 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.twenty_percent_line_layout.addWidget(self.label_6)
        self.zero_percent_line = QtWidgets.QCheckBox(self.tab)
        self.zero_percent_line.setText("")
        self.zero_percent_line.setChecked(True)
        self.zero_percent_line.setObjectName("zero_percent_line")
        self.twenty_percent_line_layout.addWidget(self.zero_percent_line)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.twenty_percent_line_layout.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.twenty_percent_line_layout)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_7 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_8.addWidget(self.label_7)
        self.label_11 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_8.addWidget(self.label_11)
        self.display_responses_as_text = QtWidgets.QCheckBox(self.tab)
        self.display_responses_as_text.setText("")
        self.display_responses_as_text.setChecked(False)
        self.display_responses_as_text.setAutoExclusive(False)
        self.display_responses_as_text.setObjectName("display_responses_as_text")
        self.horizontalLayout_8.addWidget(self.display_responses_as_text)
        spacerItem3 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.label_9 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_8.addWidget(self.label_9)
        self.display_responses_as_color = QtWidgets.QCheckBox(self.tab)
        self.display_responses_as_color.setText("")
        self.display_responses_as_color.setChecked(True)
        self.display_responses_as_color.setAutoExclusive(True)
        self.display_responses_as_color.setObjectName("display_responses_as_color")
        self.horizontalLayout_8.addWidget(self.display_responses_as_color)
        spacerItem4 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem4)
        self.label_10 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_8.addWidget(self.label_10)
        self.use_custom_keys = QtWidgets.QCheckBox(self.tab)
        self.use_custom_keys.setText("")
        self.use_custom_keys.setAutoExclusive(True)
        self.use_custom_keys.setObjectName("use_custom_keys")
        self.horizontalLayout_8.addWidget(self.use_custom_keys)
        spacerItem5 = QtWidgets.QSpacerItem(1, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_12 = QtWidgets.QLabel(self.tab)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_3.addWidget(self.label_12)
        self.show_cancer_type = QtWidgets.QCheckBox(self.tab)
        self.show_cancer_type.setText("")
        self.show_cancer_type.setObjectName("show_cancer_type")
        self.horizontalLayout_3.addWidget(self.show_cancer_type)
        spacerItem6 = QtWidgets.QSpacerItem(1, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_13 = QtWidgets.QLabel(self.tab)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_6.addWidget(self.label_13)
        self.outline_bars = QtWidgets.QCheckBox(self.tab)
        self.outline_bars.setText("")
        self.outline_bars.setObjectName("outline_bars")
        self.horizontalLayout_6.addWidget(self.outline_bars)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem7)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_8 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_4.addWidget(self.label_8)
        self.include_table = QtWidgets.QCheckBox(self.tab)
        self.include_table.setText("")
        self.include_table.setObjectName("include_table")
        self.horizontalLayout_4.addWidget(self.include_table)
        spacerItem8 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem9)
        self.btn_apply_general_settings = QtWidgets.QPushButton(self.tab)
        self.btn_apply_general_settings.setEnabled(False)
        self.btn_apply_general_settings.setObjectName("btn_apply_general_settings")
        self.verticalLayout_2.addWidget(self.btn_apply_general_settings)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_2.sizePolicy().hasHeightForWidth())
        self.tab_2.setSizePolicy(sizePolicy)
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_14 = QtWidgets.QLabel(self.tab_2)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_2.addWidget(self.label_14)
        self.key_name = QtWidgets.QLineEdit(self.tab_2)
        self.key_name.setObjectName("key_name")
        self.horizontalLayout_2.addWidget(self.key_name)
        self.btn_get_key_color = QtWidgets.QPushButton(self.tab_2)
        self.btn_get_key_color.setText("")
        self.btn_get_key_color.setObjectName("btn_get_key_color")
        self.horizontalLayout_2.addWidget(self.btn_get_key_color)
        self.btn_add_key = QtWidgets.QPushButton(self.tab_2)
        self.btn_add_key.setObjectName("btn_add_key")
        self.horizontalLayout_2.addWidget(self.btn_add_key)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.listWidget = QtWidgets.QListWidget(self.tab_2)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_4.addWidget(self.listWidget)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.btn_apply_keys_and_colors_settings = QtWidgets.QPushButton(self.tab_2)
        self.btn_apply_keys_and_colors_settings.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_apply_keys_and_colors_settings.sizePolicy().hasHeightForWidth())
        self.btn_apply_keys_and_colors_settings.setSizePolicy(sizePolicy)
        self.btn_apply_keys_and_colors_settings.setObjectName("btn_apply_keys_and_colors_settings")
        self.horizontalLayout_7.addWidget(self.btn_apply_keys_and_colors_settings)
        self.btn_default_settings = QtWidgets.QPushButton(self.tab_2)
        self.btn_default_settings.setObjectName("btn_default_settings")
        self.horizontalLayout_7.addWidget(self.btn_default_settings)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.tabWidget.addTab(self.tab_2, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.data_viewer_container = QtWidgets.QVBoxLayout()
        self.data_viewer_container.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.data_viewer_container.setObjectName("data_viewer_container")
        self.horizontalLayout.addLayout(self.data_viewer_container)
        self.verticalLayout.addWidget(self.plot_settings)
        self.btn_finalize_plot = QtWidgets.QPushButton(Waterfall)
        self.btn_finalize_plot.setEnabled(False)
        self.btn_finalize_plot.setObjectName("btn_finalize_plot")
        self.verticalLayout.addWidget(self.btn_finalize_plot)

        self.retranslateUi(Waterfall)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Waterfall)

    def retranslateUi(self, Waterfall):
        _translate = QtCore.QCoreApplication.translate
        Waterfall.setWindowTitle(_translate("Waterfall", "Dialog"))
        self.plot_settings.setTitle(_translate("Waterfall", "Waterfall Plot Settings"))
        self.label.setText(_translate("Waterfall", "Plot Title: "))
        self.label_2.setText(_translate("Waterfall", "X-Axis Label:"))
        self.label_3.setText(_translate("Waterfall", "Y-Axis Label: "))
        self.label_4.setText(_translate("Waterfall", "+20% Line:"))
        self.label_5.setText(_translate("Waterfall", "-30% Line:"))
        self.label_6.setText(_translate("Waterfall", "0% Line:"))
        self.label_7.setText(_translate("Waterfall", "Display patient response (CR,PR,PD,SD):"))
        self.label_11.setText(_translate("Waterfall", "Text"))
        self.label_9.setText(_translate("Waterfall", "Color coding"))
        self.label_10.setText(_translate("Waterfall", "Custom keys"))
        self.label_12.setText(_translate("Waterfall", "Show cancer type:"))
        self.label_13.setText(_translate("Waterfall", "Outline bars:"))
        self.label_8.setText(_translate("Waterfall", "Include table (no x-axis label will show)"))
        self.btn_apply_general_settings.setText(_translate("Waterfall", "Apply General Settings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Waterfall", "General settings"))
        self.label_14.setText(_translate("Waterfall", "Add key:"))
        self.btn_add_key.setText(_translate("Waterfall", "Add"))
        self.btn_apply_keys_and_colors_settings.setText(_translate("Waterfall", "Apply color coding settings"))
        self.btn_default_settings.setText(_translate("Waterfall", "Default settings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Waterfall", "Color coding and markers"))
        self.btn_finalize_plot.setText(_translate("Waterfall", "Finalize Plot for Export"))

