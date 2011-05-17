from PyQt4 import QtCore, QtGui

from app.models import MultiGraph
from app.controllers import GraphsController

from app.views.qt4.node.show import NodeShow
from app.views.qt4.edge.show import EdgeShow
from app.views.qt4.graph.selection_box import SelectionBox

class GraphScene(QtGui.QGraphicsScene):
    
    def __init__(self, parent):
        QtGui.QGraphicsScene.__init__(self, parent)
        
        self.action = None
        
        self.rubberband = SelectionBox(QtGui.QRubberBand.Line, self.parent())
 
    def set_action(self, action):
        if action == "remove_node" and len(self.selectedItems()) > 0:
            map(self.remove_node, self.selectedItems())
        elif action == "add_edge" and len(self.selectedItems()) > 1:
            self.add_edges(self.selectedItems())
        else:
            self.action = action

    def add_edges(self, nodes):
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                n1 = nodes[i].node['id']
                n2 = nodes[j].node['id']
                edge = self.controller.add_edge(self.graph, n1, n2)
                if edge != None:
                    edge_show = EdgeShow(edge, nodes[i], nodes[j])
                    self.addItem(edge_show)
        
    def remove_node(self, node):
        self.controller.remove_node(self.graph, node.node)
        for edge in node.edge_list:
            self.removeItem(edge)
        self.removeItem(node)
        
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
        
            if self.action == "add_node":
                position = event.scenePos()
                position = [position.x(), position.y()]
                node = self.controller.add_node(self.graph, position)
                node_show = NodeShow(node)
                self.addItem(node_show)
                self.set_action(None)
            elif self.action == "remove_node":
                QtGui.QGraphicsScene.mouseReleaseEvent(self, event)
                map(self.remove_node, self.selectedItems())
            elif self.action == None:
                QtGui.QGraphicsScene.mouseReleaseEvent(self, event)
                
    def paint(self):
      print 'oi'
                  
        
