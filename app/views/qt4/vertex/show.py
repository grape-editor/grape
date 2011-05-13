from PyQt4 import QtCore, QtGui

class VertexShow(QtGui.QGraphicsItem):
    
    def __init__(self, vertex):
        QtGui.QGraphicsItem.__init__(self)
        
        self.edge_list = []
        
        self.vertex = vertex
        
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QtGui.QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(-1)
        
        self.setPos(vertex.position[0], vertex.position[1])

        self.title = QtGui.QGraphicsTextItem(self, self.scene())
        self.title.setPlainText(self.vertex.title)
        self.title.adjustSize()
        self.title.setPos(-(self.title.boundingRect().width() / 2), -(self.title.boundingRect().height() / 2))
        
    def add_edge(self, edge):
        self.edge_list.append(edge)
        self.calculate_edges_trajectory()
    
    def boundingRect(self):
        radius = self.vertex.size / 2
        adjust = 2
        return QtCore.QRectF(-radius - adjust, -radius - adjust, self.vertex.size + adjust, self.vertex.size + adjust)
    
    def paint(self, painter, option, widget):
        painter.setClipRect(option.exposedRect)
        color = None
        
        if (self.isSelected()):
            #TODO - Global configuration here
            color = QtGui.QColor.fromRgbF(0, 1, 0)
        else:
            color = QtGui.QColor.fromRgbF(self.vertex.fill_color[0], self.vertex.fill_color[0], self.vertex.fill_color[0])
        
        radius = self.vertex.size / 2

        painter.setBrush(color)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, self.vertex.border_size))
        painter.drawEllipse(-radius, -radius, self.vertex.size, self.vertex.size)

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionHasChanged:
            pos = value.toPointF()
            self.vertex.position[0] = pos.x()
            self.vertex.position[1] = pos.y()
            
            self.calculate_edges_trajectory()
            
        return QtGui.QGraphicsItem.itemChange(self, change, value)
    
    def calculate_edges_trajectory(self):
        vertex_set = []
        
        for edge in self.edge_list:
            if edge.start != self and not edge.start in vertex_set:
                vertex_set.append(edge.start)
            elif edge.end != self and not edge.end in vertex_set:
                vertex_set.append(edge.end)
        
        edge_sets = []
        
        for vertex in vertex_set:
            edge_sets.append([])

            for edge in self.edge_list:
                if edge.start == vertex or edge.end == vertex:
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
                    
                    mult = -mult
                    
                    edge.adjust()
                    
                length += step
                
            if len(set) == 1:
                edge = set.pop()
                edge.path = QtGui.QPainterPath()
                edge.path.moveTo(edge.start_point)
                edge.path.lineTo(edge.end_point)
                edge.adjust()

    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)
