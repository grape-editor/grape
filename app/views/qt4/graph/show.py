from app.views.qt4.graph.show_ui import Ui_GraphShow

import math
import pickle
from PyQt4 import QtCore, QtGui

from app.models import *
from app.controllers import GraphsController

class GraphShow(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.controller = GraphsController()

        self.graph = MultiDiGraph()
        self.graph.graph['title'] = 'Untitled'
        
        self.ui = Ui_GraphShow()
        self.ui.setupUi(self)
        self.ui.graphicsView.scene.graph = self.graph
        self.ui.graphicsView.scene.controller = self.controller

    def set_action(self, action):
        self.ui.graphicsView.set_action(action)
