import sys
from PyQt4 import QtGui
from PyKDE4 import kdeui
import mainwindow
import sane
import logging

logging.basicConfig(level=logging.DEBUG)

app = QtGui.QApplication(sys.argv)

sane.init()
devices = sane.get_devices()
if not devices:
    kdeui.KMessageBox.error(None, 'No scanner device found.', 'No Scanner')
    sys.exit(1)

mainWindow = mainwindow.MainWindow()
mainWindow.device = sane.open(devices[0][0])
mainWindow.show()


sys.exit(app.exec_())
