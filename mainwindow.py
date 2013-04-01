
from PyKDE4.kio import KUrlRequester  #@UnresolvedImport  #@IgnorePep8
from PyKDE4.kdeui import KColorCells, KPushButton, KIntSpinBox  #@UnresolvedImport  #@IgnorePep8
from PyKDE4 import kdecore  #@UnresolvedImport  #@IgnorePep8
from PyQt4 import QtCore, QtGui  #@UnresolvedImport  #@IgnorePep8
from PyQt4.QtCore import SIGNAL  #@UnresolvedImport  #@IgnorePep8
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


def crop(image):
    sx, sy = [4 * (s / 4) for s in image.size]
    log.info("Cropping image to size %dx%d." % (sx, sy))
    return image.transform((sx, sy), Image.EXTENT, (0, 0, sx, sy))


def dist(color1, color2):
    return sum([abs(c1 - c2) for  c1, c2 in zip(color1, color2)])


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
        self.reduceColorsButton.clicked.connect(self.filterOutUnimportantColors)
        self.connect(self.previewView, SIGNAL('resize()'), self.updatePreview)

    def setupUi(self):
        self.centralwidget = QtGui.QWidget(self)

        self.scanButton = KPushButton(self.centralwidget)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.reduceColorsButton = KPushButton(self.centralwidget)
        self.numColorSpinBox = KIntSpinBox(self.centralwidget)
        self.numColorSpinBox.setMinimum(2)
        self.numColorSpinBox.setMaximum(16)
        self.numColorSpinBox.setProperty("value", 16)

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

    def scan(self):
        self.scanned_pil = self.device.scan()
        self.showInfo()
        self.scanned_image = ImageQt.ImageQt(crop(self.scanned_pil))
        self.updateColorCells()
        self.updatePreview()

    def updatePreview(self):
        if self.scanned_image:
            scaled_image = self.scanned_image.scaled(self.previewView.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            pm = QtGui.QPixmap.fromImage(scaled_image)
            self.previewView.setPixmap(pm)

    def updateColorCells(self):
        if self.scanned_image:
            if self.scanned_pil.mode != 'P':
                self.convertImage()
            colors = [QtGui.QColor(rgb) for rgb in self.scanned_image.colorTable()]
            for i, c in enumerate(colors):
                self.colorEditorCells.setColor(i, c)
        else:
            for i in range(self.colorEditorCells.count()):
                self.colorEditorCells.setColor(i, QtGui.QColor())

    def reduceColorsPressed(self):
        self.reduceColors(self.numColorSpinBox.value())
        self.updateColorCells()

    def convertImage(self):
        converted = crop(self.scanned_pil).convert('P')
        colortable = []
        palette = converted.getpalette()
        for i in range(0, len(palette), 3):
            colortable.append(QtGui.qRgb(*palette[i:i + 3]))
        self.scanned_pil = converted

        self.scanned_image = ImageQt.ImageQt(converted)
        self.scanned_image.setColorTable(colortable)


    def filterOutUnimportantColors(self):
        if self.scanned_pil:
            log.info("Removing unimportant colors.")
            if self.scanned_pil.mode != 'P':
                self.convertImage()
            num_color = self.numColorSpinBox.value()-1
            histo = self.scanned_pil.histogram()
            log.debug('Histogram: %s' % histo)
            histo = zip(range(len(histo)), histo)
            log.debug('Histogram zipped: %s' % histo)
            histo.sort(key=lambda x: -x[1])
            log.debug('Histogram sorted: %s' % histo)

            ref_colors = [(c,c,c) for c in range(0,256,256/num_color)] + [(255,255,255)]

            colors = self.scanned_pil.getpalette()
            for ci, freq in histo:
            #for ci, freq in histo[num_color:]:
                color = colors[ci * 3:ci * 3 + 3]
                distances = []
                #for cr, dummy in histo[:num_color]:
                #    ref_color = colors[cr * 3:cr * 3 + 3]
                for ref_color in ref_colors:
                    distances.append(dist(ref_color, color))
                nearest = min(xrange(len(distances)), key=distances.__getitem__)
                #cn = histo[nearest][0]
                #nearest_color = colors[cn * 3:cn * 3 + 3]
                nearest_color = ref_colors[nearest]
                #log.info("Removed color %d (%d,%d,%d) %d px." % (ci, color[0], color[1], color[2], freq))
                colors[ci * 3:ci * 3 + 3] = nearest_color
            log.info("Colors now %d: %s" % (len(colors), str(colors)))
            self.scanned_pil.putpalette(colors)
            colortable = []
            for i in range(0, len(colors), 3):
                colortable.append(QtGui.qRgb(*colors[i:i + 3]))
            self.scanned_image = ImageQt.ImageQt(crop(self.scanned_pil))
            self.scanned_image.setColorTable(colortable)
            self.updateColorCells()
            self.updatePreview()

    def reduceColors(self, num):
        if self.scanned_pil:
            log.info('Reducing colors to %d' % num)
            self.scanned_pil = self.scanned_pil.quantize(num, method=0)
            self.convertImage()
            self.showInfo()
            self.updatePreview()
            self.updateColorCells()
