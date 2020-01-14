# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 00:27:25 2020

@author: François Aubin, Martin Canals, Théo Giani
"""

from RRCONST import *
from numpy import array , ndarray , zeros

class Board :
    """ Données et méthodes pour un plateau
        Un plateau consiste en une grille + des méthodes 
        rotation de la grille
        vérification de la conformité de la grille (utile pour les tests)
        détermination des murs entourant une cellule
    """
    
    def __init__(self, data) :
        """ Construit un objet Board à partir des données
        Le constructeur sert essentiellement à typer les données en tableau 
        numpy si ce n'est pas déjà le cas
        """
        if not isinstance (data, ndarray) :
            data = array(data, dtype = int)
        
        self.grid = data 
        # self.height, self.width = data.shape        
        
        if not self.grid_conforms() :
            print("Erreur grille")
            
    def cell_is_open(self,pos,side) :
        """ renvoie True si il n'y a pas de cloison du côté side
            pos est un tuple (x,y) donnant la position de la case dans la grille
            voir documentation technique page .............
        """
        assert(side in [SOUTH, NORTH, EAST, WEST])
        nblin, nbcol = self.grid.shape
        x, y = pos
        assert (0 <= x < nbcol)
        assert (0 <= y < nblin)
      
        return self.grid[pos] & side == 0 
    
    def grid_conforms(self):
        """     vérifie la conformité de la grille (redondance des murs) """
        nblin, nbcol = self.grid.shape
        # test murs verticaux
        for i in range(nblin):
            for j in range(nbcol - 1):
                if self.cell_is_open((i,j),EAST) != self.cell_is_open((i,j+1),WEST):                    
                    print("problème vertical à ", i , " , ", j)
                    return False

        # test murs horizontaux
        for i in range(nbcol - 1):
            for j in range(nblin):
                if self.cell_is_open((i,j),SOUTH) != self.cell_is_open((i+1,j),NORTH):
                    print("problème horizontal à ", i, " , ", j)
        return True 
    
    @staticmethod
    def __rotate_cell_left(cell) :
        """ tourne une case d'un quart de tour vers la droite """
        turned_cell = 0
        if cell & SOUTH : turned_cell += EAST
        if cell & EAST : turned_cell += NORTH
        if cell & NORTH : turned_cell += WEST
        if cell & WEST : turned_cell += SOUTH        
        return turned_cell
    
    def rotate_left(self) :
        """ cette méthode tourne la grille d'un quart de tour vers la gauche
        """
        
        nbcol , nblin = self.grid.shape
        turned_grid = zeros((nblin,nbcol),dtype=int)
        for i in range(nblin) :
            for j in range(nbcol):
                turned_grid[i,j] = self.__rotate_cell_left(self.grid[j,nblin-1-i])
        self.grid = turned_grid

    def rotate_half(self) : 
        """ cette méthode tourne la grille d'un demi tour """
        
        self.rotate_left()
        self.rotate_left()
        
    def rotate_right(self) : 
        """ cette méthode tourne la grille d'un demi tour """
        
        self.rotate_left()
        self.rotate_left()
        self.rotate_left()
           
# Testing

"""
table = [[ 9,  1, 1, 3,  9, 1, 1, 1],
              [10, 12, 0, 0, 0,  0, 4, 0],
              [  8,   1, 0, 0, 0,  0, 3, 8],
              [  8,   0, 0, 0, 0,  0, 0, 0],
              [  8, 0, 6, 8, 0,  0, 0, 4],
              [12, 0, 1, 0, 0,  0, 2, 9],
              [  9, 0, 0, 0, 0, 0, 0, 4],
              [  8, 0, 0, 0, 0,   0, 2, 9]] 
myBoard = Board(table)
myBoard.rotate_left()  
myBoard.rotate_right()      

"""
