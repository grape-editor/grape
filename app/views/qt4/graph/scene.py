from PyQt4 import QtCore, QtGui

from app.models import *
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
        elif action == "align_horizontal" and len(self.selectedItems()) > 1:
            self.align_vertical(self.selectedItems())
        elif action == "align_vertical" and len(self.selectedItems()) > 1:
            self.align_horizontal(self.selectedItems())
        else:
            self.action = action
    
    def align_horizontal(self, nodes):
        mean = int(sum(map(lambda n: n.node['position'][1], nodes)) / len(nodes))
        for node in nodes:
            node.node['position'] = (node.node['position'][0], mean)
            node.setPos(node.node['position'][0], node.node['position'][1])
            node.calculate_edges_trajectory()

    def align_vertical(self, nodes):
        mean = int(sum(map(lambda n: n.node['position'][0], nodes)) / len(nodes))
        for node in nodes:
            node.node['position'] = (mean, node.node['position'][1])
            node.setPos(node.node['position'][0], node.node['position'][1])
            node.calculate_edges_trajectory()

    def refresh_graph(self):
        nodes = {}
        
        for i in self.graph.node:
            node = self.graph.node[i]
            nodes[i] = self.add_node(node)
            
        for i in self.graph.edge:
            for j in self.graph.edge[i]:
                if isinstance(self.graph, MultiGraph) or isinstance(self.graph, MultiDiGraph):
                    for k in self.graph.edge[i][j]:
                        self.add_edge(nodes[i], nodes[j], self.graph.edge[i][j][k])
                else:
                    self.add_edge(nodes[i], nodes[j], self.graph.edge[i][j])
    
    def add_edge(self, n1, n2, edge=None):
        n1id = n1.node['id']
        n2id = n2.node['id']
        
        if not edge:
          edge = self.controller.add_edge(self.graph, n1id, n2id)
          
        edge_show = EdgeShow(edge, n1, n2)
        self.addItem(edge_show)
    
    def add_node(self, node):
        node_show = NodeShow(self, node)

        self.addItem(node_show)
        
        return node_show
        
    def add_edges(self, nodes):
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                self.add_edge(nodes[i], nodes[j])
    
    def remove_node(self, node):
        self.controller.remove_node(self.graph, node.node)
        
        for edge in list(node.edge_list):
            edge.start.edge_list.remove(edge)
            edge.end.edge_list.remove(edge)

            edge.setVisible(False)
#            self.removeItem(edge)
        
        self.removeItem(node)
        
    def mousePressEvent(self, event):
        items = self.items(event.scenePos())
        
        def check_clickable(item):
            return item.acceptedMouseButtons() != QtCore.Qt.NoButton
            
        if self.action == "add_edge":
            position = event.scenePos()
            nodes = self.items(position)
            node = None
            
            while not isinstance(node, NodeShow) and len(nodes) > 0:
                node = nodes.pop()
            
            source = self.selectedItems()[0]
            
            if node and node != source and isinstance(node, NodeShow):
                self.add_edge(source, node)
                
            self.set_action(None)
        elif len(items) and reduce(lambda a, b: a or b, map(check_clickable, items)):
            QtGui.QGraphicsScene.mousePressEvent(self, event)
        elif event.button() in [QtCore.Qt.LeftButton, QtCore.Qt.RightButton]:
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
                self.add_node(node)
                self.set_action(None)
            elif self.action == "remove_node":
                QtGui.QGraphicsScene.mouseReleaseEvent(self, event)
                map(self.remove_node, self.selectedItems())
            elif self.action == None:
                QtGui.QGraphicsScene.mouseReleaseEvent(self, event)
                
        if event.button() == QtCore.Qt.RightButton:
            menu = QtGui.QMenu()

            # Sorcery is used here. But don't care, it really works
            ui = self.parent().parent().parent().parent().parent().parent().ui

            menu.addAction(ui.actionAdd_node)
            menu.addAction(ui.actionRemove_node)
            menu.addSeparator()
            menu.addAction(ui.actionAdd_edge)
            menu.addAction(ui.actionRemove_edge)
            menu.addSeparator()
            menu.addAction(ui.actionAlign_vertically)
            menu.addAction(ui.actionAlign_horizontally)
           
            menu.exec_(event.screenPos())
            
                
                
