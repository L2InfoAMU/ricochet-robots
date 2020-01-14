
# constante du module

from RRCONST import *
import robot 
import goal    
import board

class Game :
    """  la classe jeu regroupe les données décrivant 
    - le plateau de jeu 
    - la liste des robots
    - l'objectif du jeu
    """    
    def __init__(self, board, robots) :
        """ renvoie un objet de type Game
        """        
        self.board = board        
        self.robots = robots

        self.nb_robots = len(robots)
        
        for robot in robots :
            robot.board = board
            robot.friends = robots
                

       
        
            
           












