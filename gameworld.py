
# constante du module

from RRCONST import *


class GameWorld :
    """  la classe jeu regroupe les données décrivant 
    - le plateau de jeu   self.board
    - la liste des robots self.robots
    - l'objectif du jeu   self.goal
    - un tableau associatif { couleur : robot } permettant d'accéder 
        à un robot par sa couleur  self.robot_by_color
    
    """    
    def __init__(self, board , robots , goal) :
        """ renvoie un objet de type Game
        """        
        self.board = board        
        self.robots = robots
        self.goal = goal
        self.nb_robots = len(robots)  
        self.robot_by_color = dict()
        
        
        for robot in robots : 
            robot.world = self   
            if robot.color not in self.robot_by_color :
                self.robot_by_color [robot.color] = robot
            else :
                print("erreur, deux robots de la meme couleur")
            
                

       
        
            
           












