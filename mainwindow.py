
from PyKDE4.kio import KUrlRequester
from PyKDE4.kdeui import KColorCells, KPushButton, KIntSpinBox
from PyKDE4 import kdecore
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL
from PIL import Image  #@UnresolvedImport #@IgnorePep8
import ImageQt

import logging

log = logging.getLogger(__name__)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig): #@IgnorePep8
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class ResizableImageLabel(QtGui.QLabel):

    def __init__(self, parent=None):
        QtGui.QLabel.__init__(self, parent)
        self.scaledContents = True
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def resizeEvent(self, evt=None):
        self.emit(SIGNAL('resize()'))
        return QtGui.QLabel.resizeEvent(self, evt)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.scanned_image = None
        self.scanned_pil = None
        self.setupUi()

        self.saveButton.clicked.connect(self.close)
        self.actionQuit.activated.connect(self.close)
        self.scanButton.clicked.connect(self.scan)
        self.reduceColorsButton.clicked.connect(self.reduceColorsPressed)
        self.connect(self.previewView, SIGNAL('resize()'), self.updatePreview)

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

        colorSpacerLeft = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.colorEditorCells = KColorCells(self.centralwidget, 16, 16)
        colorSpacerRight = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

        colorEditorLayout = QtGui.QHBoxLayout()
        colorEditorLayout.addItem(colorSpacerLeft)
        colorEditorLayout.addWidget(self.colorEditorCells, 0)
        colorEditorLayout.addItem(colorSpacerRight)

        self.previewView = ResizableImageLabel(self.centralwidget)
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
        verticalLayout.addLayout(scanSettingsLayout, 0)
        verticalLayout.addLayout(colorEditorLayout, 0)
        verticalLayout.addWidget(self.previewView, 1)
        verticalLayout.addLayout(filenameLayout, 0)
        verticalLayout.addLayout(outputNameLayout, 0)
        verticalLayout.addLayout(saveButtonLayout, 0)

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

    def showInfo(self):
        size = self.scanned_pil.size
        mode = self.scanned_pil.mode
        info = self.scanned_pil.info
        self.statusbar.showMessage('Size: "%dx%d", Mode: "%s, Info: "%s"' % (size[0], size[1], mode, info))
        #self.scanned_pil.show()

    def scan(self):
        self.scanned_pil = self.device.scan()
        #self.scanned_pil = Image.open("test.png")
        self.showInfo()
        self.scanned_image = ImageQt.ImageQt(self.scanned_pil)
        self.updatePreview()
        self.updateColorCells()
        self.updatePreview()

    def updatePreview(self):
        if self.scanned_image:
            scaled_image = self.scanned_image.scaled(self.previewView.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            pm = QtGui.QPixmap.fromImage(scaled_image)
            self.previewView.setPixmap(pm)

    def updateColorCells(self):
        if self.scanned_image:
            colors = [QtGui.QColor(rgb) for rgb in self.scanned_image.colorTable()]
            for i, c in enumerate(colors):
                self.colorEditorCells.setColor(i, c)

    def reduceColorsPressed(self):
        self.reduceColors(self.numColorSpinBox.value())
        self.updateColorCells()

    def reduceColors(self, num):
        if self.scanned_pil:
            log.info('Reducing colors to %d' % num)
            self.scanned_pil = self.scanned_pil.quantize(num, method=0)
            sx, sy = [4 * ((s - 1) / 4) for s in self.scanned_pil.size]
            log.info("Cropping image to size %dx%d." % (sx, sy))
            converted = self.scanned_pil.transform((sx, sy), Image.EXTENT, (0, 0, sx, sy))
            converted = converted.convert('P')
            colortable = []
            palette = converted.getpalette()
            for i in range(0, len(palette), 3):
                colortable.append(QtGui.qRgb(*palette[i:i + 3]))

            self.scanned_image = ImageQt.ImageQt(converted)
            self.scanned_image.setColorTable(colortable)
            self.showInfo()
            self.updatePreview()
            self.updateColorCells()
