from PyQt4 import QtCore, QtGui

from app.views.qt4.graph.scene import GraphScene

class GraphView(QtGui.QGraphicsView):
    
    def __init__(self, parent):
        QtGui.QGraphicsView.__init__(self, parent)
        self.scene = GraphScene(self)
        self.setScene(self.scene)
    
    def set_action(self, action):
        if action == "zoom_in":
            self.zoom_in()
        elif action == "zoom_out":
            self.zoom_out()
        elif action == "normal_size":
            self.normal_size()
        else:
            self.scene.set_action(action)
        
    def zoom_in(self):
        self.scale(1.1, 1.1)
 
    def zoom_out(self):
        self.scale(1.0 / 1.1, 1.0 / 1.1)
    
    def normal_size(self):
        self.resetTransform()
