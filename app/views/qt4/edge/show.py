import math
from PyQt4 import QtCore, QtGui

class EdgeShow(QtGui.QGraphicsItem):
    
    def __init__(self, edge):
        QtGui.QGraphicsItem.__init__(self)

        self.vertex = edge
        self.arrow_size = 10

        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QtGui.QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(-1)

  def adjust(self):
  
        start = self.edge.start.position
        end = self.edge.end.position
        
        line = QtCore.QLineF(self.mapFromItem(start, 0, 0), self.mapFromItem(end, 0, 0))
        length = line.length()
  
        if length == 0.0:
            return
  
        edge_offset = QtCore.QPointF((line.dx() * 10) / length, (line.dy() * 10) / length)
  
        self.prepareGeometryChange()

#        self.sourcePoint = line.p1() + edgeOffset
#        self.destPoint = line.p2() - edgeOffset
  

    def boundingRect(self)
        pen_width = 1
        extra = (pen_width + self.arrow_size) / 2.0

        position_start = self.edge.start.position
        position_end = self.edge.start.position

        size = QtCore.QSizeF(position_end[0] - position_start[0], position_end[1] - position_star[1])
        return QtCore.QRectF(position_start, size).normalized().adjusted(-extra, -extra, extra, extra)

    def paint(painter, style, widget):
  
        line = QtCore.QLineF(position_start, position_end)
        if line.length() == 0.0:
            return

        # Draw the line itself
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(line)


        # Draw the arrows
        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = 2 * math.pi - angle

        start1 = sourcePoint + QtCore.QPointF(math.sin(angle + math.pi / 3) * arrow_size,
                                            math.cos(angle + math.pi / 3) * arrow_size))
        start2 = sourcePoint + QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3) * arrow_size,
                                            math.cos(angle + math.pi - math.pi / 3) * arrow_size))
        end1 = destPoint + QtCore.QPointF(math.sin(angle - math.pi / 3) * arrow_size,
                                        math.cos(angle - math.pi / 3) * arrow_size))
        end1 = destPoint + QtCore.QPointF(math.sin(angle - math.pi + math.pi / 3) * arrow_size,
                                        math.cos(angle - math..pi + math.pi / 3) * arrow_size))

        painter.setBrush(QtCore.Qt.black)

        # Another mistery
        
        painter.setBrush(QtCore.Qt.black)
        painter.drawPolygon(QtGui.QPolygonF([line.p1(), start1, start2]))
        painter.drawPolygon(QtGui.QPolygonF([line.p2(), end1, end2]))

    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)



