from gui.MainScreen import MainScreen
from gui.DrawArea import DrawArea
from lib.Graph import Vertex


class ControllerGUI:
    
    def __init__(self):
        main_screen = MainScreen()
        main_screen.draw_area.graph = Graph()
        

