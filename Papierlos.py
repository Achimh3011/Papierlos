import sys
from PyQt4 import QtGui  #@UnresolvedImport  #@IgnorePep8
from PyKDE4 import kdeui  #@UnresolvedImport  #@IgnorePep8

import logging
logging.basicConfig(level=logging.DEBUG)

import mainwindow

import sane  #@UnresolvedImport  #@IgnorePep8


class scanner(object):

    def __init__(self):
        sane.init()
        devices = sane.get_devices()
        if not devices:
            raise ValueError
        self.device = sane.open(devices[0][0])

    def scan(self):
        return self.device.scan()


class no_scanner(object):

    def scan(self):
        from PIL import Image  #@UnresolvedImport #@IgnorePep8
        return Image.open('test.png').convert('RGB')

app = QtGui.QApplication(sys.argv)

try:
    scan_dev = no_scanner()
except ValueError:
    kdeui.KMessageBox.error(None, 'No scanner device found.', 'No Scanner')
    sys.exit(1)

mainWindow = mainwindow.MainWindow()
mainWindow.device = scan_dev
mainWindow.show()


sys.exit(app.exec_())
