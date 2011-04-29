from PyQt4 import QtCore, QtGui

from app.views.qt4.vertex.show import VertexShow

class GraphView(QtGui.QGraphicsView):
    
    def __init__(self, parent):
        QtGui.QGraphicsView.__init__(self, parent)
        self.scene = QtGui.QGraphicsScene(self)
        self.setScene(self.scene)
        
        
    def mouseReleaseEvent(self, event):
        v = VertexShow()
        self.scene.addItem(VertexShow())
        print event.posF()
        v.setPos(event.posF())
