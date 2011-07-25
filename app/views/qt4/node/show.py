from PyQt4 import QtCore, QtGui

class NodeShow(QtGui.QGraphicsItem):
    
    def __init__(self, parent, node):
        QtGui.QGraphicsItem.__init__(self)
        
        self.edge_list = []
        
        self.node = node
        self.parent = parent
        
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QtGui.QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(-1)
        
        self.setPos(node['position'][0], node['position'][1])

        self.title = QtGui.QGraphicsTextItem(self, self.scene())
        self.title.setPlainText(self.node['title'])
        self.title.adjustSize()
        self.title.setPos(-(self.title.boundingRect().width() / 2), -(self.title.boundingRect().height() / 2))

    def add_edge(self, edge):
        self.edge_list.append(edge)
        self.calculate_edges_trajectory()
    
    def boundingRect(self):
        radius = self.node['size'] / 2
        adjust = 2
        return QtCore.QRectF(-radius - adjust, -radius - adjust, self.node['size'] + adjust, self.node['size'] + adjust)
    
    def paint(self, painter, option, widget):
        painter.setClipRect(option.exposedRect)
        color = None
        
        if (self.isSelected()):
            #TODO - Global configuration here
            color = QtGui.QColor.fromRgbF(0, 1, 0)
        else:
            color = QtGui.QColor.fromRgbF(*self.node['fill_color'])
        
        radius = self.node['size'] / 2

        painter.setBrush(color)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, self.node['border_size']))
        painter.drawEllipse(-radius, -radius, self.node['size'], self.node['size'])

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionHasChanged:
            pos = value.toPointF()
            self.node['position'] = (pos.x(), pos.y())
            
            self.calculate_edges_trajectory()
            
        return QtGui.QGraphicsItem.itemChange(self, change, value)
    
    def calculate_edges_trajectory(self):
        node_set = []
        
        for edge in self.edge_list:
            if edge.start != self and not edge.start in node_set:
                node_set.append(edge.start)
            elif edge.end != self and not edge.end in node_set:
                node_set.append(edge.end)
        
        edge_sets = []
        
        for node in node_set:
            edge_sets.append([])

            for edge in self.edge_list:
                if edge.start == node or edge.end == node:
                    edge_sets[-1].append(edge)
        
        for set in edge_sets:
            line = QtCore.QLineF(set[0].start.pos(), set[0].end.pos())
            mean = line.pointAt(0.5)
            line.setP1(mean)
            line = line.normalVector()
            step = 15
            length = 15
            
            while len(set) > 1:
                mult = 1

                for _ in range(2):
                    edge = set.pop()
                    line.setLength(length * mult)
                    edge.path = QtGui.QPainterPath()
                    edge.path.moveTo(edge.start_point)
                    edge.path.quadTo(line.p2(), edge.end_point)
                    edge.anchor_point = line.p2()
                    
                    mult = -mult
                    
                    edge.adjust()
                    
                length += step
                
            if len(set) == 1:
                edge = set.pop()
                edge.path = QtGui.QPainterPath()
                edge.path.moveTo(edge.start_point)
                edge.path.lineTo(edge.end_point)
                edge.anchor_point = edge.end_point
                edge.adjust()

    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)

        if event.button() == QtCore.Qt.RightButton:
            menu = QtGui.QMenu()

            # Sorcery is used here. But don't care, it really works
            ui = self.parent.parent().parent().parent().parent().parent().parent().ui

            menu.addAction(ui.actionAdd_node)
            menu.addAction(ui.actionRemove_node)
            menu.addSeparator()
            menu.addAction(ui.actionAdd_edge)
            menu.addAction(ui.actionRemove_edge)
            menu.addSeparator()
            menu.addAction(ui.actionAlign_vertically)
            menu.addAction(ui.actionAlign_horizontally)
           
            menu.exec_(event.screenPos())
            
    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)
