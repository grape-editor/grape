from PyQt4 import QtCore, QtGui

class SelectionBox(QtGui.QRubberBand):
    def __init__(self, s, p=0):
        QtGui.QRubberBand.__init__(self, s, p)
 
    def paintEvent(self, event):
        pen = QtGui.QPen(QtGui.QColor(0, 83, 235))
        pen.setWidth(2)
         
        brush = QtGui.QBrush(QtGui.QColor(51, 122, 255))
        
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.setOpacity(0.5)
        painter.drawRect(event.rect())
        painter.end()
