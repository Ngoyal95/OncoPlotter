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
        Waterfall.resize(982, 580)
        self.gridLayout_2 = QtWidgets.QGridLayout(Waterfall)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.plot_settings = QtWidgets.QGroupBox(Waterfall)
        self.plot_settings.setObjectName("plot_settings")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.plot_settings)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.bar_keys_and_event_markers = QtWidgets.QGroupBox(self.plot_settings)
        self.bar_keys_and_event_markers.setObjectName("bar_keys_and_event_markers")
        self.gridLayout_3.addWidget(self.bar_keys_and_event_markers, 0, 1, 1, 1)
        self.general_settings = QtWidgets.QGroupBox(self.plot_settings)
        self.general_settings.setObjectName("general_settings")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.general_settings)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_3.addWidget(self.general_settings, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.plot_settings, 0, 0, 1, 1)

        self.retranslateUi(Waterfall)
        QtCore.QMetaObject.connectSlotsByName(Waterfall)

    def retranslateUi(self, Waterfall):
        _translate = QtCore.QCoreApplication.translate
        Waterfall.setWindowTitle(_translate("Waterfall", "Dialog"))
        self.plot_settings.setTitle(_translate("Waterfall", "Waterfall Plot Settings"))
        self.bar_keys_and_event_markers.setTitle(_translate("Waterfall", "Bar Color Keys and Event Markers"))
        self.general_settings.setTitle(_translate("Waterfall", "General Settings"))

