import math
from PyQt4 import QtCore, QtGui

class EdgeShow(QtGui.QGraphicsItem):
    def __init__(self, sourceNode, destNode):
        QtGui.QGraphicsItem.__init__(self)
        self.arrowSize = 8.0
        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.source = sourceNode
        self.dest = destNode
        self.source.add_edge(self)
        self.dest.add_edge(self)
        self.adjust()
        
    def sourceNode(self):
        return self.source
  
    def setSourceNode(self, node):
        self.source = node
        self.adjust()
  
    def destNode(self):
        return self.dest
  
    def setDestNode(self, node):
        self.dest = node
        self.adjust()
  
    def adjust(self):
        if not self.source or not self.dest:
            return
  
        line = QtCore.QLineF(self.mapFromItem(self.source, 0, 0), self.mapFromItem(self.dest, 0, 0))
        length = line.length()
  
        if length == 0.0:
            return
  
        source_offset = QtCore.QPointF((line.dx() * self.source.vertex.size / 2) / length, (line.dy() * self.source.vertex.size / 2) / length)
        dest_offset = QtCore.QPointF((line.dx() * self.dest.vertex.size / 2) / length, (line.dy() * self.dest.vertex.size / 2) / length)
  
        self.prepareGeometryChange()
        self.sourcePoint = line.p1() + source_offset
        self.destPoint = line.p2() - dest_offset
  
    def boundingRect(self):
        if not self.source or not self.dest:
            return QtCore.QRectF()
  
        penWidth = 1
        extra = (penWidth + self.arrowSize) / 2.0
  
        return QtCore.QRectF(self.sourcePoint,
                             QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                           self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)
  
    def paint(self, painter, option, widget):
        if not self.source or not self.dest:
            return
  
        # Draw the line itself.
        line = QtCore.QLineF(self.sourcePoint, self.destPoint)
  
        if line.length() == 0.0:
            return
  
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(line)
  
        # Draw the arrows if there's enough room.
        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = 2 * math.pi - angle
  
        sourceArrowP1 = self.sourcePoint + QtCore.QPointF(math.sin(angle + math.pi / 3) * self.arrowSize,
                                                          math.cos(angle + math.pi / 3) * self.arrowSize)
        sourceArrowP2 = self.sourcePoint + QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3) * self.arrowSize,
                                                          math.cos(angle + math.pi - math.pi / 3) * self.arrowSize);  
        destArrowP1 = self.destPoint + QtCore.QPointF(math.sin(angle - math.pi / 3) * self.arrowSize,
                                                      math.cos(angle - math.pi / 3) * self.arrowSize)
        destArrowP2 = self.destPoint + QtCore.QPointF(math.sin(angle - math.pi + math.pi / 3) * self.arrowSize,
                                                      math.cos(angle - math.pi + math.pi / 3) * self.arrowSize)
  
        painter.setBrush(QtCore.Qt.black)
        painter.drawPolygon(QtGui.QPolygonF([line.p1(), sourceArrowP1, sourceArrowP2]))
        painter.drawPolygon(QtGui.QPolygonF([line.p2(), destArrowP1, destArrowP2]))

