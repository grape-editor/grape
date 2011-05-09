from PyQt4 import QtCore, QtGui

class VertexShow(QtGui.QGraphicsItem):
    
    def __init__(self, vertex):
        QtGui.QGraphicsItem.__init__(self)
        
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
    
    def boundingRect(self):
        self.vertex.size = 30
        radius = self.vertex.size / 2
        adjust = 2
        return QtCore.QRectF(-radius - adjust, -radius - adjust, self.vertex.size + adjust, self.vertex.size + adjust)
    
    def paint(self, painter, option, widget):
        color = None
        if (self.isSelected()):
            #TODO - Global configuration here
            color = QtGui.QColor.fromRgbF(0, 1, 0)
        else:
            color = QtGui.QColor.fromRgbF(self.vertex.fill_color[0], self.vertex.fill_color[0], self.vertex.fill_color[0])
        
        self.border_size = 2
        self.vertex.size = 30
        radius = self.vertex.size / 2

        painter.setBrush(color)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, self.vertex.border_size))
        painter.drawEllipse(-radius, -radius, self.vertex.size, self.vertex.size)

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionHasChanged:
            pos = value.toPointF()
            self.vertex.position[0] = pos.x()
            self.vertex.position[1] = pos.y()
            
        return QtGui.QGraphicsItem.itemChange(self, change, value)

    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)
