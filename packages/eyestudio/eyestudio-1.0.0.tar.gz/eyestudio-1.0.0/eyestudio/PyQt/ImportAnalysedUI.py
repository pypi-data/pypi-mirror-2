# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyQt/ImportAnalysedUI.ui'
#
# Created: Thu Apr 22 23:40:21 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ImportAnalysedDialog(object):
    def setupUi(self, ImportAnalysedDialog):
        ImportAnalysedDialog.setObjectName("ImportAnalysedDialog")
        ImportAnalysedDialog.setWindowModality(QtCore.Qt.WindowModal)
        ImportAnalysedDialog.resize(375, 250)
        self.verticalLayout = QtGui.QVBoxLayout(ImportAnalysedDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(ImportAnalysedDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.filterList = QtGui.QListWidget(ImportAnalysedDialog)
        self.filterList.setObjectName("filterList")
        self.verticalLayout.addWidget(self.filterList)
        self.buttonBox = QtGui.QDialogButtonBox(ImportAnalysedDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ImportAnalysedDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ImportAnalysedDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ImportAnalysedDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ImportAnalysedDialog)

    def retranslateUi(self, ImportAnalysedDialog):
        ImportAnalysedDialog.setWindowTitle(QtGui.QApplication.translate("ImportAnalysedDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ImportAnalysedDialog", "Analysed data:", None, QtGui.QApplication.UnicodeUTF8))

