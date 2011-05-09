from app.models.active_model import ActiveModel
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
        
        ActiveModel.__init__(self, params)
        
        start.touching_edges.append(self)
        end.touching_edges.append(self)

        start.add_edge(self)

        if self.bidirectional:
            end.add_edge(self)

    def touches(self, vertex):
        return vertex == self.start or vertex == self.end

