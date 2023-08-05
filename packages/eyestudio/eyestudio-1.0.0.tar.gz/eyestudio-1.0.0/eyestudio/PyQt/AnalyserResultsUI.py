# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyQt/AnalyserResultsUI.ui'
#
# Created: Thu Apr 22 23:40:21 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AnalyserResults(object):
    def setupUi(self, AnalyserResults):
        AnalyserResults.setObjectName("AnalyserResults")
        AnalyserResults.setWindowModality(QtCore.Qt.WindowModal)
        AnalyserResults.resize(747, 623)
        self.verticalLayout_3 = QtGui.QVBoxLayout(AnalyserResults)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scrollArea = QtGui.QScrollArea(AnalyserResults)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 719, 553))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.wrapperLayout = QtGui.QVBoxLayout()
        self.wrapperLayout.setObjectName("wrapperLayout")
        self.resultsLayout = QtGui.QVBoxLayout()
        self.resultsLayout.setObjectName("resultsLayout")
        self.wrapperLayout.addLayout(self.resultsLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.wrapperLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.wrapperLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushExport = QtGui.QPushButton(AnalyserResults)
        self.pushExport.setObjectName("pushExport")
        self.horizontalLayout.addWidget(self.pushExport)
        self.pushClose = QtGui.QPushButton(AnalyserResults)
        self.pushClose.setObjectName("pushClose")
        self.horizontalLayout.addWidget(self.pushClose)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(AnalyserResults)
        QtCore.QMetaObject.connectSlotsByName(AnalyserResults)

    def retranslateUi(self, AnalyserResults):
        AnalyserResults.setWindowTitle(QtGui.QApplication.translate("AnalyserResults", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushExport.setText(QtGui.QApplication.translate("AnalyserResults", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.pushClose.setText(QtGui.QApplication.translate("AnalyserResults", "Close", None, QtGui.QApplication.UnicodeUTF8))

