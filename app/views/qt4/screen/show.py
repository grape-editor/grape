from app.views.qt4.screen.show_ui import Ui_ScreenShow
from app.views.qt4.graph.show import GraphShow
from PyQt4 import QtCore, QtGui

class ScreenShow(QtGui.QMainWindow):
    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self)
        
        self.parent = parent
        self.ui = Ui_ScreenShow()
        self.ui.setupUi(self)
    
    def on_tabWidget_tabCloseRequested(self, number):
        self.ui.tabWidget.removeTab(number)

    def on_actionOpen_triggered(self, checked=None):
        if checked == None:
            pass
            
    def on_actionNew_triggered(self, checked=None):
        if checked == None:
            graph = GraphShow()
            
            self.ui.tabWidget.addTab(graph, graph.graph.title)
            self.ui.tabWidget.setCurrentWidget(graph)
            
    def on_actionSave_triggered(self, checked=None):
        if checked == None:
            pass
            
    def on_actionSave_as_triggered(self, checked=None):
        if checked == None:
            pass
            
    def on_actionRever_triggered(self, checked=None):
        if checked == None:
            pass
            
    def on_actionClose_triggered(self, checked=None):
        if checked == None:
            self.close()
            
    def on_actionQuit_triggered(self, checked=None):
        if checked == None:
            self.parent.app.closeAllWindows()
            
    def on_actionUndo_triggered(self, checked=None):
        if checked == None:
            pass
            
    def on_actionRedo_triggered(self, checked=None):
        if checked == None:
            pass
            
    def on_actionAdd_vertex_triggered(self, checked=None):
        if checked == None:
            tab = self.ui.tabWidget.currentWidget()
            if tab:
                tab.set_action("add_vertex")
            
    def on_actionRemove_vertex_triggered(self, checked=None):
        if checked == None:
            tab = self.ui.tabWidget.currentWidget()
            if tab:
                tab.set_action("remove_vertex")
            
    def on_actionAdd_edge_triggered(self, checked=None):
        if checked == None:
            pass
            
    def on_actionRemove_edge_triggered(self, checked=None):
        if checked == None:
            pass
            
    def on_actionAlign_vertically_triggered(self, checked=None):
        if checked == None:
            pass
            
    def on_actionAlign_horizontally_triggered(self, checked=None):
        if checked == None:
            pass
            
    def on_actionZoom_in_triggered(self, checked=None):
        if checked == None:
            pass
            
    def on_actionZoom_out_triggered(self, checked=None):
        if checked == None:
            pass
            
    def on_actionNormal_size_triggered(self, checked=None):
        if checked == None:
            pass
            
    def on_actionFullscreen_triggered(self, checked=None):
        if checked == None:
            pass
            
    def on_actionAbout_triggered(self, checked=None):
        if checked == None:
            pass
            
