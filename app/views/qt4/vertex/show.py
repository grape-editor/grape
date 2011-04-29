from PyQt4 import QtCore, QtGui

class VertexShow(QtGui.QGraphicsItem):
    
    def __init__(self, vertex):
        QtGui.QGraphicsItem.__init__(self)
        
        self.vertex = vertex
        
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges);
        self.setCacheMode(QtGui.QGraphicsItem.DeviceCoordinateCache);
        self.setZValue(-1);
        
        self.setPos(vertex.position[0], vertex.position[1])
    
    def boundingRect(self):
        adjust = 2
        return QtCore.QRectF(-10 - adjust, -10 - adjust, 23 + adjust, 23 + adjust)
    
    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)
        painter.drawEllipse(-7, -7, 20, 20)
        
        gradient = QtGui.QRadialGradient(-3, -3, 10)
        
        if (option.state & QtGui.QStyle.State_Sunken):
            gradient.setCenter(3, 3)
            gradient.setFocalPoint(3, 3)
            gradient.setColorAt(1, QtGui.QColor(QtCore.Qt.yellow).light(120))
            gradient.setColorAt(0, QtGui.QColor(QtCore.Qt.darkYellow).light(120))
        else:
            gradient.setColorAt(0, QtCore.Qt.yellow)
            gradient.setColorAt(1, QtCore.Qt.darkYellow)

        painter.setBrush(gradient)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
        painter.drawEllipse(-10, -10, 20, 20)
    
    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)
