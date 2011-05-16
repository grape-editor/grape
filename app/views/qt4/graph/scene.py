from PyQt4 import QtCore, QtGui

from app.controllers.graphs_controller import GraphsController
from app.models.graph import Graph
from app.views.qt4.vertex.show import VertexShow
from app.views.qt4.edge.show import EdgeShow
from app.views.qt4.graph.selection_box import SelectionBox

class GraphScene(QtGui.QGraphicsScene):
    
    def __init__(self, parent):
        QtGui.QGraphicsScene.__init__(self, parent)
        
        self.action = None
        self.graph = Graph()
        self.graphs_controller = GraphsController()
        
        self.rubberband = SelectionBox(QtGui.QRubberBand.Line, self.parent())
 
    def set_action(self, action):
        if action == "remove_vertex" and len(self.selectedItems()) > 0:
            map(self.remove_vertex, self.selectedItems())
        elif action == "add_edge" and len(self.selectedItems()) > 1:
            self.add_edges(self.selectedItems())
        else:
            self.action = action

    def add_edges(self, vertices):
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                v1 = vertices[i].vertex
                v2 = vertices[j].vertex
                edge = self.graphs_controller.add_edge(self.graph, v1, v2)
                edge_show = EdgeShow(edge, vertices[i], vertices[j])
                self.addItem(edge_show)
        
    def remove_vertex(self, v):
        self.graphs_controller.remove_vertex(self.graph, v.vertex)
        self.removeItem(v)
        
    def mousePressEvent(self, event):
        items = self.items(event.scenePos())
        
        def check_clickable(item):
            return item.acceptedMouseButtons() != QtCore.Qt.NoButton
            
        if len(items) and reduce(lambda a, b: a or b, map(check_clickable, items)):
            QtGui.QGraphicsScene.mousePressEvent(self, event)
        elif event.button() == QtCore.Qt.LeftButton:
            pos = self.parent().mapFromScene(event.scenePos())
            self.rubberband.setGeometry(QtCore.QRect(pos, QtCore.QSize()))
            self.rubberband.show()
  
    def mouseMoveEvent(self, event):
        if self.rubberband.isVisible() and bool(event.buttons() & QtCore.Qt.LeftButton):
            start_pos = self.parent().mapFromScene(event.buttonDownScenePos(QtCore.Qt.LeftButton))
            final_pos = self.parent().mapFromScene(event.scenePos())
            rect = QtCore.QRect(start_pos, final_pos).normalized()
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
            elif self.action == "remove_vertex":
                QtGui.QGraphicsScene.mouseReleaseEvent(self, event)
                map(self.remove_vertex, self.selectedItems())
            elif self.action == None:
                QtGui.QGraphicsScene.mouseReleaseEvent(self, event)
                
    def paint(self):
      print 'oi'
                  
        
