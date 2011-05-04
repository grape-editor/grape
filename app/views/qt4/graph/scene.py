from PyQt4 import QtCore, QtGui

from app.controllers.graphs_controller import GraphsController
from app.models.graph import Graph
from app.views.qt4.vertex.show import VertexShow

class GraphScene(QtGui.QGraphicsScene):
    
    def __init__(self, parent):
        QtGui.QGraphicsScene.__init__(self, parent)
        
        self.action = None
        self.graph = Graph()
        self.graphs_controller = GraphsController()
        
        self.rubberband = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle)
        self.rubberband.pen = QtGui.QPen()
        self.rubberband.pen.setWidth(1)

    def set_action(self, action):
        self.action = action
        
    def mousePressEvent(self, event):
        if self.itemAt(event.scenePos()):
            QtGui.QGraphicsScene.mousePressEvent(self, event)
        elif event.button() == QtCore.Qt.LeftButton:
            self.rubberband.setGeometry(QtCore.QRect(event.screenPos(), QtCore.QSize()))
            self.rubberband.show()
  
    def mouseMoveEvent(self, event):
        if self.rubberband.isVisible() and bool(event.buttons() & QtCore.Qt.LeftButton):
            rect = QtCore.QRect(event.buttonDownScreenPos(QtCore.Qt.LeftButton), event.screenPos()).normalized()
            rectf = QtCore.QRectF(event.buttonDownScenePos(QtCore.Qt.LeftButton), event.scenePos()).normalized()

            self.rubberband.setGeometry(rect)
            p = QtGui.QPolygonF(rectf)
            
            path = QtGui.QPainterPath()
            path.addPolygon(p)
            
            if bool(event.modifiers() & QtCore.Qt.ControlModifier) or bool(event.modifiers() & QtCore.Qt.ShiftModifier):
                path += self.selectionArea()

            self.setSelectionArea(path, QtCore.Qt.IntersectsItemShape)
        else:
            QtGui.QGraphicsScene.mouseMoveEvent(self, event)
  
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.rubberband.isVisible():
                self.rubberband.hide()
        
            if self.action == "add_vertex":
                position = event.scenePos()
                position = [position.x(), position.y()]
                vertex = self.graphs_controller.add_vertex(self.graph, position)
                vertex_show = VertexShow(vertex)
                self.addItem(vertex_show)
                self.set_action(None)
            elif self.action == None:
                QtGui.QGraphicsScene.mouseReleaseEvent(self, event)
        
