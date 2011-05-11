from app.models.active_model import ActiveModel
from app.controllers.vertices_controller import VerticesController
from PyQt4 import QtCore, QtGui

class Edge(ActiveModel):
    validate = {
        'presence' : {'id': True, 'position': True},
        'length'   : {'title': 25, 'name': 11}
    }

    def __init__(self, params):
        self.id = None
    
        self.title = ""
        self.color = [0, 0, 0]
        self.width = 1
        
        self.start = None
        self.end = None
        self.bidirectional = None
        
        self.vertices_controller = VerticesController()
        
        ActiveModel.__init__(self, params)
        
        self.start.touching_edges.append(self)
        self.end.touching_edges.append(self)

        self.vertices_controller.add_edge(self.start, self)

        if self.bidirectional:
            self.vertices_controller.add_edge(self.end, self)

    def touches(self, vertex):
        return vertex == self.start or vertex == self.end

