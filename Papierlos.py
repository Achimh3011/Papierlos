import sys
from PyQt4 import QtGui
import mainwindow


app = QtGui.QApplication(sys.argv)

mainWindow = mainwindow.MainWindow()
mainWindow.show()

sys.exit(app.exec_())
