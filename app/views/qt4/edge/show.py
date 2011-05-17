import math
from PyQt4 import QtCore, QtGui

class EdgeShow(QtGui.QGraphicsItem):
    def __init__(self, edge, start_node, end_node):
        QtGui.QGraphicsItem.__init__(self)
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.edge = edge
        
        self.arrowSize = 8.0
        self.start_point = QtCore.QPointF()
        self.end_point = QtCore.QPointF()
        self.start = start_node
        self.end = end_node
        self.start.add_edge(self)
        self.end.add_edge(self)
        self.adjust()
    
    def set_start_node(self, node):
        self.start = node
        self.adjust()
  
    def set_end_node(self, node):
        self.end = node
        self.adjust()
  
    def adjust(self):
        if not self.start or not self.end:
            return
  
        line = QtCore.QLineF(self.mapFromItem(self.start, 0, 0), self.mapFromItem(self.end, 0, 0))
        length = line.length()
  
        if length == 0.0:
            return
  
        source_offset = QtCore.QPointF((line.dx() * self.start.node['size'] / 2) / length, (line.dy() * self.start.node['size'] / 2) / length)
        dest_offset = QtCore.QPointF((line.dx() * self.end.node['size'] / 2) / length, (line.dy() * self.end.node['size'] / 2) / length)
  
        self.prepareGeometryChange()
        self.start_point = line.p1() + source_offset
        self.end_point = line.p2() - dest_offset
  
    def boundingRect(self):
        if not self.start or not self.end:
            return QtCore.QRectF()
  
        penWidth = 1
        extra = (penWidth + self.arrowSize) / 2.0
        polygon = QtGui.QPolygonF([self.start_point, self.end_point, self.anchor_point])
        return QtCore.QRectF(polygon.boundingRect()).normalized().adjusted(-extra, -extra, extra, extra)
  
    def paint(self, painter, option, widget):
        painter.setClipRect(option.exposedRect)
        line = QtCore.QLineF(self.start_point, self.end_point)
  
        if line.length() == 0.0:
            return
  
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.strokePath(self.path, painter.pen())
        
        if self.edge['directed']:
            angle = math.acos(line.dx() / line.length())
            if line.dy() >= 0:
                angle = 2 * math.pi - angle
  
            sourceArrowP1 = self.start_point + QtCore.QPointF(math.sin(angle + math.pi / 3) * self.arrowSize,
                                                              math.cos(angle + math.pi / 3) * self.arrowSize)
            sourceArrowP2 = self.start_point + QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3) * self.arrowSize,
                                                              math.cos(angle + math.pi - math.pi / 3) * self.arrowSize);  
            destArrowP1 = self.end_point + QtCore.QPointF(math.sin(angle - math.pi / 3) * self.arrowSize,
                                                          math.cos(angle - math.pi / 3) * self.arrowSize)
            destArrowP2 = self.end_point + QtCore.QPointF(math.sin(angle - math.pi + math.pi / 3) * self.arrowSize,
                                                          math.cos(angle - math.pi + math.pi / 3) * self.arrowSize)
  
            painter.setBrush(QtCore.Qt.black)
            painter.drawPolygon(QtGui.QPolygonF([line.p1(), sourceArrowP1, sourceArrowP2]))
            painter.drawPolygon(QtGui.QPolygonF([line.p2(), destArrowP1, destArrowP2]))

