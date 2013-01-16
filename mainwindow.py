#!/usr/bin/env python
# coding=UTF-8
#
# Generated by pykdeuic4 from mainwindow.ui on Sun Jan 13 18:27:26 2013
#
# WARNING! All changes to this file will be lost.
from PyKDE4 import kdecore
from PyKDE4 import kdeui
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()
        self.saveButton.clicked.connect(self.close)
        self.actionQuit.activated.connect(self.close)

    def setupUi(self):
        self.centralwidget = QtGui.QWidget(self)

        self.scanButton = KPushButton(self.centralwidget)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.reduceColorsButton = KPushButton(self.centralwidget)
        self.numColorSpinBox = KIntSpinBox(self.centralwidget)
        self.numColorSpinBox.setMinimum(2)
        self.numColorSpinBox.setMaximum(16)
        self.numColorSpinBox.setProperty("value", 8)

        scanSettingsLayout = QtGui.QHBoxLayout()
        scanSettingsLayout.addWidget(self.scanButton)
        scanSettingsLayout.addItem(spacerItem)
        scanSettingsLayout.addWidget(self.reduceColorsButton)
        scanSettingsLayout.addWidget(self.numColorSpinBox)

        self.colorEditorCells = KColorCells(self.centralwidget,4,4)

        self.previewView = QtGui.QGraphicsView(self.centralwidget)
        self.previewView.setMinimumSize(QtCore.QSize(400, 400))

        self.baseFileNameRequester = KUrlRequester(self.centralwidget)
        self.FileSeqSpinBox = KIntSpinBox(self.centralwidget)

        filenameLayout = QtGui.QHBoxLayout()
        filenameLayout.addWidget(self.baseFileNameRequester)
        filenameLayout.addWidget(self.FileSeqSpinBox)

        self.generatedOutputNameTextLabel = QtGui.QLabel(self.centralwidget)
        self.generatedOutputNameLabel = QtGui.QLabel(self.centralwidget)

        outputNameLayout = QtGui.QHBoxLayout()
        outputNameLayout.addWidget(self.generatedOutputNameLabel)
        outputNameLayout.addWidget(self.generatedOutputNameTextLabel)

        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.saveButton = KPushButton(self.centralwidget)

        saveButtonLayout = QtGui.QHBoxLayout()
        saveButtonLayout.addItem(spacerItem1)
        saveButtonLayout.addWidget(self.saveButton)

        verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        verticalLayout.setMargin(0)
        verticalLayout.addLayout(scanSettingsLayout)
        verticalLayout.addWidget(self.colorEditorCells)
        verticalLayout.addWidget(self.previewView)
        verticalLayout.addLayout(filenameLayout)
        verticalLayout.addLayout(outputNameLayout)
        verticalLayout.addLayout(saveButtonLayout)

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 474, 20))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setMinimumSize(QtCore.QSize(0, 20))
        self.setStatusBar(self.statusbar)

        self.actionQuit = QtGui.QAction(self)
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle(kdecore.i18n(_fromUtf8("MainWindow")))
        self.scanButton.setText(kdecore.i18n(_fromUtf8("Scan")))
        self.reduceColorsButton.setText(kdecore.i18n(_fromUtf8("Reduce Colors")))
        self.generatedOutputNameTextLabel.setText(kdecore.i18n(_fromUtf8("Output:")))
        self.generatedOutputNameLabel.setText(kdecore.i18n(_fromUtf8("generated_output_file_name")))
        self.saveButton.setText(kdecore.i18n(_fromUtf8("Save")))
        self.menuFile.setTitle(kdecore.i18n(_fromUtf8("File")))
        self.actionQuit.setText(kdecore.i18n(_fromUtf8("Quit")))

    def scan(self):
        pass

from PyKDE4.kio import KUrlRequester
from PyKDE4.kdeui import KColorCells, KPushButton, KIntSpinBox
