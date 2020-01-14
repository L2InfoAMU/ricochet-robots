# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 23:03:49 2020

@author: Martin
"""

from RRCONST import *
from board import Board
from objectif import Objectif


class ClassicBoard(Board) :
    """ Les objets de cette classe contiennent une grille de jeu classique
        En plus de la grille avec les murs il y a les objectifs dessinés
        sur le plateau       
    """
    def __init__(self,grid,objectifs) :
        super().__init__(grid)
        self.objectifs = objectifs
    
    def rotate_left(self) :
        # On appelle la méthode sur la classe Parent pour tourner la grille
        super().rotate_left()
        
        # on tourne les objectifs
        dim = self.grid.shape
        for i in range(len(self.objectifs)) :
             self.objectifs[i].rotate_left(dim)   
        
     def rotate_half(self) :
        # On appelle la méthode sur la classe Parent pour tourner la grille
        super().rotate_half()
        
        # on tourne les objectifs
        dim = self.grid.shape
        for i in range(len(self.objectifs)) :
             self.objectifs[i].rotate_half(dim)  
             
     def rotate_right(self) :
        # On appelle la méthode sur la classe Parent pour tourner la grille
        super().rotate_right()
        
        # on tourne les objectifs
        dim = self.grid.shape
        for i in range(len(self.objectifs)) :
             self.objectifs[i].rotate_right(dim)      
  


from numpy import array , ndarray

rouge1 = [[ 9,  1, 1, 3,  9, 1, 1, 1],
              [10, 12, 0, 0, 0,  0, 4, 0],
              [  8,   1, 0, 0, 0,  0, 3, 8],
              [  8,   0, 0, 0, 0,  0, 0, 0],
              [  8, 0, 6, 8, 0,  0, 0, 4],
              [12, 0, 1, 0, 0,  0, 2, 9],
              [  9, 0, 0, 0, 0, 0, 0, 4],
              [  8, 0, 0, 0, 0,   0, 2, 9]] 

obj1 = Objectif(RED,(1,1))
obj2 = Objectif(BLUE ,(0,0))
board1 = ClassicBoard(rouge1, [obj1, obj2])
