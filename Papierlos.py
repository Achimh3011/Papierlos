import sys
from PyQt4 import QtGui
import mainwindow
import sane

app = QtGui.QApplication(sys.argv)

sane.init()
devices = sane.get_devices()

mainWindow = mainwindow.MainWindow()
mainWindow.device = sane.open(devices[0][0])
mainWindow.show()


sys.exit(app.exec_())
