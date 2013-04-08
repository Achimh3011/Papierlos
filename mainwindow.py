
from PyKDE4.kio import KUrlRequester  #@UnresolvedImport  #@IgnorePep8
from PyKDE4.kdeui import KColorCells, KPushButton, KIntSpinBox  #@UnresolvedImport  #@IgnorePep8
from PyKDE4 import kdecore  #@UnresolvedImport  #@IgnorePep8
from PyQt4 import QtCore, QtGui  #@UnresolvedImport  #@IgnorePep8
from PyQt4.QtCore import SIGNAL  #@UnresolvedImport  #@IgnorePep8
from PyQt4.Qt import Qt  #@UnresolvedImport  #@IgnorePep8
from PIL import Image  #@UnresolvedImport #@IgnorePep8
import ImageQt

import logging
from copy import deepcopy

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


def crop(image):
    sx, sy = [4 * (s / 4) for s in image.size]
    log.info("Cropping image to size %dx%d." % (sx, sy))
    return image.transform((sx, sy), Image.EXTENT, (0, 0, sx, sy))


def grayscale():
    colortable = []
    for r in range(256):
        c = QtGui.QColor(QtGui.qRgb(r, r, r))
        colortable.append(c)
    return colortable


def dist(color1, color2):
    return (abs(color1.red() - color2.red()) +
        abs(color1.green() - color2.green()) +
        abs(color1.blue() - color2.blue()))


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
        self.colors = None
        self.setupUi()

        self.saveButton.clicked.connect(self.close)
        self.actionQuit.activated.connect(self.close)
        self.scanButton.clicked.connect(self.scan)
        self.resetColorsButton.clicked.connect(self.resetColors)
        self.numColorSlider.valueChanged.connect(self.updateNumColors)
        self.connect(self.previewView, SIGNAL('resize()'), self.updatePreview)

    def setupUi(self):
        self.centralwidget = QtGui.QWidget(self)

        self.scanButton = KPushButton()
        self.nColorLabel = QtGui.QLabel()
        self.numColorSlider = QtGui.QSlider(Qt.Horizontal)
        self.numColorSlider.setMinimum(2)
        self.numColorSlider.setTracking(False)
        self.resetColorsButton = KPushButton()

        scanSettingsLayout = QtGui.QHBoxLayout()
        scanSettingsLayout.addWidget(self.scanButton)
        scanSettingsLayout.addWidget(self.numColorSlider)
        scanSettingsLayout.addWidget(self.nColorLabel)
        scanSettingsLayout.addWidget(self.resetColorsButton)

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
        self.resetColorsButton.setText(kdecore.i18n(_fromUtf8("Reset")))
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

    def scan(self):
        self.scanned_pil = self.device.scan()
        self.scanned_pil = crop(self.scanned_pil)
        self.scanned_pil = self.scanned_pil.convert('L')
        self.scanned_image = ImageQt.ImageQt(self.scanned_pil)
        self.showInfo()

        self.colors = grayscale()
        self.colors_orig = deepcopy(self.colors)
        n_color, self.histo = self.createHistogram()

        for i, c in enumerate(self.colors):
            self.scanned_image.setColor(i, c.rgba())

        self.numColorSlider.setMaximum(n_color)
        self.numColorSlider.setValue(n_color)
        self.showImage()

    def showImage(self):
        self.updateColorCells()
        self.updatePreview()

    def updatePreview(self):
        if self.scanned_image:
            for i, c in enumerate(self.colors):
                self.scanned_image.setColor(i, c.rgba())
            scaled_image = self.scanned_image.scaled(self.previewView.size(),
                                                     aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            pm = QtGui.QPixmap.fromImage(scaled_image)
            self.previewView.setPixmap(pm)

    def updateColorCells(self):
        for i, (ci, freq) in enumerate(self.histo):
            c = self.colors[ci] if freq else QtGui.QColor()
            self.colorEditorCells.setColor(i, c)

    def updateColorCells_flat(self):
        for i in range(256):
            c = self.colors[i]
            self.colorEditorCells.setColor(i, c)

    def updateNumColors(self):
        self.reduceColors(self.numColorSlider.value())
        self.nColorLabel.setText("%3d" % self.numColorSlider.value())
        self.updateColorCells()

    def createHistogram(self):
        histo = self.scanned_pil.histogram()[:256]
        log.debug('Histogram (%d entries): %s' % (len(histo), histo))
        histo = zip(range(len(histo)), histo)
        histo.sort(key=lambda x: -x[1])
        log.debug('Histogram zipped and sorted: %s' % histo)
        return len([ci for (ci, frequency) in histo if frequency > 0]), histo

    def reduceColors(self, num):
        if self.scanned_pil:
            log.info("Removing unimportant colors down to %3d" % num)

            self.colors = deepcopy(self.colors_orig)
            color_steps = self.numColorSlider.value() - 1
            ref_colors = [QtGui.QColor(c, c, c) for c in range(0, 255, 256 / color_steps)]
            ref_colors.append(QtGui.QColor(255, 255, 255))
            log.debug("Reference colors are: %s" % [str(c.name()) for c in ref_colors])

            for color_index, dummy_frequency in self.histo:
                color = self.colors[color_index]
                distances = []
                for ref_color in ref_colors:
                    distances.append(dist(ref_color, color))
                nearest = min(range(len(distances)), key=distances.__getitem__)
                nearest_color = ref_colors[nearest]
                self.colors[color_index] = nearest_color
            log.debug("Colors now %d: %s" % (len(self.colors), ",".join([str(c.name()) for c in self.colors])))
            self.updateColorCells()
            self.updatePreview()

    def resetColors(self):
        log.info("resetColors")
        self.numColorSlider.setValue(self.numColorSlider.maximum())
        self.colors = deepcopy(self.colors_orig)
        self.updateColorCells()
        self.updatePreview()


