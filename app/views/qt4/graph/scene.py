from PyQt4 import QtCore, QtGui

from app.models.vertex import Vertex
from app.views.qt4.vertex.show import VertexShow

class GraphScene(QtGui.QGraphicsScene):
    
    def __init__(self, parent):
        QtGui.QGraphicsScene.__init__(self, parent)
        
        self.action = None
        
    def set_action(self, action):
        self.action = action
        
    def mouseReleaseEvent(self, event):
        if self.action == "add_vertex":
            pos = event.scenePos()
            vertex = Vertex(0, (pos.x(), pos.y()))
            v = VertexShow(vertex)
            self.addItem(v)
            self.set_action(None)
        elif self.action == None:
            QtGui.QGraphicsScene.mouseReleaseEvent(self, event)
        
