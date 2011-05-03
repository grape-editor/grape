from app.controllers.action_controller import ActionController
from app.controllers.vertices_controller import VerticesController
from app.models.edge import Edge


class EdgesController(ActionController):

    def __init__(self):
        self.vertices_controller = VerticesController()
        ActionController.__init__(self)

    def create(self, params):
        edge = Edge(params)

        return edge
    
    def destroy(self, edge):
        self.vertices_controller.remove_edge(edge.start, edge)
        
        if edge.bidirectional:
            self.vertices_controller.remove_edge(edge.end, edge)

        del(edge)
