from app.controllers.action_controller import ActionController
from app.models.edge import Edge


class EdgesController(ActionController):

    def create(self, params):
        edge = Edge(params)

        return edge
