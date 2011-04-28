from app.views.qt4.screen.show_ui import Ui_ScreenShow
from PyQt4 import QtCore, QtGui

class ScreenShow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.ui = Ui_ScreenShow()
        self.ui.setupUi(self)
    
    def on_actionNew_activated(self, checked=None):
        if checked == None:
            scrollarea = QtGui.QScrollArea()     
            b = QtGui.QPushButton('Close', self)
            b.setGeometry(0, 0, 1000, 1000)
            scrollarea.setWidget(b)
            scrollarea.setAlignment(QtCore.Qt.AlignCenter)
            
            self.ui.tabWidget.addTab(scrollarea, "xisde")
