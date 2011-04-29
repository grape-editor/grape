from PyQt4 import QtCore, QtGui

from app.views.qt4.graph.scene import GraphScene

class GraphView(QtGui.QGraphicsView):
    
    def __init__(self, parent):
        QtGui.QGraphicsView.__init__(self, parent)
        self.scene = GraphScene(self)
        self.setScene(self.scene)
    
    def set_action(self, action):
        self.scene.set_action(action)
