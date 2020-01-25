
# constante du module

from RRCONST import *
import robot 
import goal    
import board

class GameWorld :
    """  la classe jeu regroupe les données décrivant 
    - le plateau de jeu 
    - la liste des robots
    - l'objectif du jeu
    """    
    def __init__(self, board , robots , goal) :
        """ renvoie un objet de type Game
        """        
        self.board = board        
        self.robots = robots
        self.goal = goal

        self.nb_robots = len(robots)
        
        for robot in robots : robot.world = self
            
                

       
        
            
           












