""" La classe GameDesign est responsable de dessiner le plateau de jeu avec les robots
Pour cela on lui passe une boite à outils de dessin

"""
from numpy import array

class GameDesign :

    def __init__(self,game,tools) :
        self.game = game
        self.drawing_tools = tools
        pass

    def draw_grid() :
        nblines , nbrows = self.game.grid.shape

        # Dessin des lignes horizontales de la grille
        for i in range (nblines+1) :
            start = (i,0)
            end = (i,nbrows)
            self.drawing_tools.draw_grid_line(start, end)

        # Dessin des lignes verticales
        for i in range (nrows+1) :
            start = (0,i)
            end = (nblines,i)
            self.drawing_tools.draw_grid_line(start, end)
    
           