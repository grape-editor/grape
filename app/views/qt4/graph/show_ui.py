# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/luan/Code/python/grape/script/../app/views/qt4/graph/show.ui'
#
# Created: Tue May 10 21:11:04 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_GraphShow(object):
    def setupUi(self, GraphShow):
        GraphShow.setObjectName(_fromUtf8("GraphShow"))
        GraphShow.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(GraphShow)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.graphicsView = GraphView(GraphShow)
        self.graphicsView.setAutoFillBackground(True)
        self.graphicsView.setSceneRect(QtCore.QRectF(-2500.0, -2500.0, 5000.0, 5000.0))
        self.graphicsView.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.TextAntialiasing)
        self.graphicsView.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.graphicsView.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.graphicsView.setViewportUpdateMode(QtGui.QGraphicsView.SmartViewportUpdate)
        self.graphicsView.setOptimizationFlags(QtGui.QGraphicsView.DontAdjustForAntialiasing|QtGui.QGraphicsView.DontClipPainter|QtGui.QGraphicsView.DontSavePainterState)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)

        self.retranslateUi(GraphShow)
        QtCore.QMetaObject.connectSlotsByName(GraphShow)

    def retranslateUi(self, GraphShow):
        GraphShow.setWindowTitle(QtGui.QApplication.translate("GraphShow", "Form", None, QtGui.QApplication.UnicodeUTF8))

from app.views.qt4.graph.view import GraphView
