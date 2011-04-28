from app.views.qt4.screen.show_ui import Ui_ScreenShow
from app.views.qt4.graph.show import GraphShow
from PyQt4 import QtCore, QtGui

class ScreenShow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.ui = Ui_ScreenShow()
        self.ui.setupUi(self)
    
    def on_actionNew_activated(self, checked=None):
        if checked == None:
            graph = GraphShow()
            
            self.ui.tabWidget.addTab(graph, graph.graph.title)
    
    def on_tabWidget_tabCloseRequested(self, number):
        print number
        
