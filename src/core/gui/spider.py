# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spider.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Spider(object):
    def setupUi(self, Spider):
        Spider.setObjectName("Spider")
        Spider.resize(364, 580)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Spider)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.plot_settings = QtWidgets.QGroupBox(Spider)
        self.plot_settings.setObjectName("plot_settings")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.plot_settings)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.data_viewer_container = QtWidgets.QVBoxLayout()
        self.data_viewer_container.setObjectName("data_viewer_container")
        self.tabWidget = QtWidgets.QTabWidget(self.plot_settings)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
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
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.spin_markersize = QtWidgets.QSpinBox(self.tab)
        self.spin_markersize.setMinimum(1)
        self.spin_markersize.setObjectName("spin_markersize")
        self.horizontalLayout_4.addWidget(self.spin_markersize)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.plot_setting_viewer = QtWidgets.QVBoxLayout()
        self.plot_setting_viewer.setObjectName("plot_setting_viewer")
        self.verticalLayout_2.addLayout(self.plot_setting_viewer)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.key_name = QtWidgets.QLineEdit(self.groupBox)
        self.key_name.setObjectName("key_name")
        self.horizontalLayout_2.addWidget(self.key_name)
        self.key_color = QtWidgets.QVBoxLayout()
        self.key_color.setObjectName("key_color")
        self.horizontalLayout_2.addLayout(self.key_color)
        self.btn_add_key = QtWidgets.QPushButton(self.groupBox)
        self.btn_add_key.setObjectName("btn_add_key")
        self.horizontalLayout_2.addWidget(self.btn_add_key)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.keys_and_colors_container = QtWidgets.QVBoxLayout()
        self.keys_and_colors_container.setObjectName("keys_and_colors_container")
        self.verticalLayout.addLayout(self.keys_and_colors_container)
        self.btn_default_keys = QtWidgets.QPushButton(self.groupBox)
        self.btn_default_keys.setObjectName("btn_default_keys")
        self.verticalLayout.addWidget(self.btn_default_keys)
        self.verticalLayout_5.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.event_name = QtWidgets.QLineEdit(self.groupBox_2)
        self.event_name.setObjectName("event_name")
        self.horizontalLayout_3.addWidget(self.event_name)
        self.marker_combo_container = QtWidgets.QVBoxLayout()
        self.marker_combo_container.setObjectName("marker_combo_container")
        self.horizontalLayout_3.addLayout(self.marker_combo_container)
        self.marker_color = QtWidgets.QVBoxLayout()
        self.marker_color.setObjectName("marker_color")
        self.horizontalLayout_3.addLayout(self.marker_color)
        self.btn_add_event = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_add_event.setObjectName("btn_add_event")
        self.horizontalLayout_3.addWidget(self.btn_add_event)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.markers_and_colors_container = QtWidgets.QHBoxLayout()
        self.markers_and_colors_container.setObjectName("markers_and_colors_container")
        self.verticalLayout_4.addLayout(self.markers_and_colors_container)
        self.btn_default_markers = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_default_markers.setObjectName("btn_default_markers")
        self.verticalLayout_4.addWidget(self.btn_default_markers)
        self.verticalLayout_5.addWidget(self.groupBox_2)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.marker_reference_container = QtWidgets.QVBoxLayout()
        self.marker_reference_container.setObjectName("marker_reference_container")
        self.verticalLayout_7.addLayout(self.marker_reference_container)
        self.tabWidget.addTab(self.tab_3, "")
        self.data_viewer_container.addWidget(self.tabWidget)
        self.horizontalLayout.addLayout(self.data_viewer_container)
        self.verticalLayout_3.addWidget(self.plot_settings)
        self.btn_apply_general_settings = QtWidgets.QPushButton(Spider)
        self.btn_apply_general_settings.setObjectName("btn_apply_general_settings")
        self.verticalLayout_3.addWidget(self.btn_apply_general_settings)
        self.pushButton_2 = QtWidgets.QPushButton(Spider)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_3.addWidget(self.pushButton_2)

        self.retranslateUi(Spider)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Spider)

    def retranslateUi(self, Spider):
        _translate = QtCore.QCoreApplication.translate
        Spider.setWindowTitle(_translate("Spider", "Dialog"))
        self.plot_settings.setTitle(_translate("Spider", "Spider Plot Settings"))
        self.label.setText(_translate("Spider", "Plot Title: "))
        self.label_2.setText(_translate("Spider", "X-Axis Label:"))
        self.label_3.setText(_translate("Spider", "Y-Axis Label: "))
        self.label_6.setText(_translate("Spider", "Markersize:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Spider", "General settings"))
        self.groupBox.setTitle(_translate("Spider", "Keys"))
        self.label_4.setText(_translate("Spider", "Add key:"))
        self.btn_add_key.setText(_translate("Spider", "Add"))
        self.btn_default_keys.setText(_translate("Spider", "Default key settings"))
        self.groupBox_2.setTitle(_translate("Spider", "Event Markers"))
        self.label_5.setText(_translate("Spider", "Add event:"))
        self.btn_add_event.setText(_translate("Spider", "Add"))
        self.btn_default_markers.setText(_translate("Spider", "Default marker settings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Spider", "Color coding and markers"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Spider", "Markers reference"))
        self.btn_apply_general_settings.setText(_translate("Spider", "Apply General Settings"))
        self.pushButton_2.setText(_translate("Spider", "PushButton"))

