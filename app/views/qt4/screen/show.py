from app.views.qt4.screen.show_ui import Ui_ScreenShow
from app.views.qt4.graph.show import GraphShow
from PyQt4 import QtCore, QtGui

from app.controllers import GraphsController

class ScreenShow(QtGui.QMainWindow):
    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self)
        
        self.controller = GraphsController()
        
        self.parent = parent
        self.ui = Ui_ScreenShow()
        self.ui.setupUi(self)
    
    def on_tabWidget_tabCloseRequested(self, number):
        self.ui.tabWidget.removeTab(number)

    def on_actionOpen_triggered(self, checked=None):
        if checked == None:
            formats = []

            
            files_types = ""
            for format in formats:
                files_types += format + ";;"
            files_types += "All files (*.*)"

            paths = QtGui.QFileDialog.getOpenFileNames(self, 'Open file', '', files_types)
            
            for path in paths:
                g = self.controller.open(str(path))
                graph = GraphShow(g)
                self.ui.tabWidget.addTab(graph, graph.graph.graph['title'])
                self.ui.tabWidget.setCurrentWidget(graph)
            
    def on_actionNew_triggered(self, checked=None):
        if checked == None:
            graph = GraphShow()
            
            self.ui.tabWidget.addTab(graph, graph.graph.graph['title'])
            self.ui.tabWidget.setCurrentWidget(graph)
            
    def on_actionSave_triggered(self, checked=None):
        if checked == None:
            pass

    def solve_imports(self, possible_formats):
        for format in possible_formats:
            imported = False
            
            if 'dependencies' in format:
                for dep in format['dependencies']:
                    try:
                        __import__(dep)
                    except:
                        continue
                    else:
                        imported = True    
                        break

            if imported:
                formats.append(format['name'])

        return formats

    def formats_to_save(self):
        possible_formats = [
            {'name': "Adjacence List (*.al)"},
            {'name': "Multiline Adjacence List (*.mal)"},
            {'name': "Edge List (*.el)"},
            {'name': "Graph Exchange XML Format (*.gexf)", 
                'dependencies': ['xml.etree.cElementTree', 'xml.etree.ElementTree']},
            {'name': "Graph Modelling Language (*.gml)",
                'dependencies': ['pyparsing', 'matplotlib.pyparsing']},
            {'name': "Pickle (*.pickle)",
                'dependencies': ['cPickle', 'pickle']},
            {'name': "GraphML (*.graphml)", 
                'dependencies': ['xml.etree.cElementTree', 'xml.etree.ElementTree']},
            {'name': "YAML (*.yml)",
                'dependencies': ['yaml']},
            {'name': "Pajek (*.pajek)"}
        ]
        
        return solve_formats(possible_formats)        

    def formats_to_open(self):
        possible_formats = [
            {'name': "Adjacence List (*.al)"},
            {'name': "Multiline Adjacence List (*.mal)"},
            {'name': "Edge List (*.el)"},
            {'name': "Graph Exchange XML Format (*.gexf)", 
                'dependencies': ['xml.etree.cElementTree', 'xml.etree.ElementTree']},
            {'name': "Graph Modelling Language (*.gml)",
                'dependencies': ['pyparsing', 'matplotlib.pyparsing']},
            {'name': "Pickle (*.pickle)",
                'dependencies': ['cPickle', 'pickle']},
            {'name': "GraphML (*.graphml)", 
                'dependencies': ['xml.etree.cElementTree', 'xml.etree.ElementTree']},
            {'name': "YAML (*.yml)",
                'dependencies': ['yaml']},
            {'name': "Pajek (*.pajek)"},
            {'name': "LEDA (*.leda)"},
            {'name': "Sparse6 (*.sparse6)"},
            {'name': "GIS Shapefile (*.shp)",
                'dependencies': ['osgeo']}
        ]
        
        return solve_formats(possible_formats)        
                    
    def on_actionSave_as_triggered(self, checked=None):
        if checked == None:
            tab = self.ui.tabWidget.currentWidget()
            if tab:
                formats = self.formats_to_save()
                
                files_types = ""
                for format in formats:
                    files_types += format + ";;"

#                files_types += "All files (*.*)"
                
                path = QtGui.QFileDialog.getSaveFileName(self, 'Save file', '', files_types)
                print path
                if path:
                    self.controller.save(tab.graph, str(path))
            
            
    def on_actionRevert_triggered(self, checked=None):
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
            
    def on_actionAdd_node_triggered(self, checked=None):
        if checked == None:
            tab = self.ui.tabWidget.currentWidget()
            if tab:
                tab.set_action("add_node")
            
    def on_actionRemove_node_triggered(self, checked=None):
        if checked == None:
            tab = self.ui.tabWidget.currentWidget()
            if tab:
                tab.set_action("remove_node")
            
    def on_actionAdd_edge_triggered(self, checked=None):
        if checked == None:
            tab = self.ui.tabWidget.currentWidget()
            if tab:
                tab.set_action("add_edge")
            
    def on_actionRemove_edge_triggered(self, checked=None):
        if checked == None:
            pass
            
    def on_actionAlign_vertically_triggered(self, checked=None):
        if checked == None:
            tab = self.ui.tabWidget.currentWidget()
            if tab:
                tab.set_action("align_vertical")
            
            
    def on_actionAlign_horizontally_triggered(self, checked=None):
        if checked == None:
            tab = self.ui.tabWidget.currentWidget()
            if tab:
                tab.set_action("align_horizontal")
            
    def on_actionZoom_in_triggered(self, checked=None):
        if checked == None:
            tab = self.ui.tabWidget.currentWidget()
            if tab:
                tab.set_action("zoom_in")
            
    def on_actionZoom_out_triggered(self, checked=None):
        if checked == None:
            tab = self.ui.tabWidget.currentWidget()
            if tab:
                tab.set_action("zoom_out")
            
    def on_actionNormal_size_triggered(self, checked=None):
        if checked == None:
            tab = self.ui.tabWidget.currentWidget()
            if tab:
                tab.set_action("normal_size")

            
    def on_actionFullscreen_triggered(self, checked=None):
        if checked == None:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
            
    def on_actionAbout_triggered(self, checked=None):
        if checked == None:
            pass
            
