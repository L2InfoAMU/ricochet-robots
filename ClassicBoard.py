# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 23:03:49 2020

@author: Martin
"""

from RRCONST import *
from ClassicBoard_data import *
from board import Board
from objectif import Objectif
from numpy import hstack, vstack
from random import *

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
  
    def __add__(self,board2) :
        """ renvoie la fusion horizontale de deux objets de type cboard"""
        """ syntaxe :  board2 = board0 + board1 """
        
        grid1 = self.grid
        grid2 = board2.grid
        # Vérification des compatibilités des dimensions 
        nl1, nc1 = grid1.shape
        nl2, nc2 = grid2.shape
        
        # les deux grilles doivent avoir le même nombre de ligne
        assert(nl1 == nl2) 
        
        # construit la nouvelle grille               
        
        grid3 = hstack((grid1,grid2)) 
        
        # Opère la suture
        for i in range(nl1) :
            if grid3[i,nc1-1] & EAST  or grid3[i,nc1] & WEST: 
               grid3[i,nc1-1] |= EAST 
               grid3[i,nc1] |= WEST
        
        # construit la liste des objectif
        # les objectifs du board0 sont inchangés 
        # les objectifs du board1 sont translatés selon le vecteur (0, nc1)
        
        vecteur = (0, nc1)
        objs3 = [obj for obj in self.objectifs ] \
            + [obj.translate(vecteur) for obj in board2.objectifs]
              
        
        return ClassicBoard(grid3, objs3)

    def __sub__(self,board2) :
        """ renvoie la fusion verticale de deux board"""
        
        grid1 = self.grid
        grid2 = board2.grid
        # Vérification des compatibilités des dimensions 
        nl1, nc1 = grid1.shape
        nl2, nc2 = grid2.shape
          
        # les deux grilles doivent avoir le même nombre de colonnes
        assert(nc1 == nc2) 

        # construit la nouvelle grille               
        grid1 = self.grid
        grid2 = board2.grid
        grid3 = vstack((grid1,grid2)) 
         
        # Opère la suture
        for i in range(nc1) :
            if grid3[nl1-1,i] & SOUTH  or grid3[nl1,i] & NORTH: 
               grid3[nl1-1,i] |= SOUTH 
               grid3[nl1,i] |= NORTH
               
        # construit la liste des objectif
        # les objectifs du board0 sont inchangés 
        # les objectifs du board1 sont translatés selon le vecteur (nl1 , 0)
        
        vecteur = (nl1, 0)
        objs3 = [obj for obj in self.objectifs ] \
            + [obj.translate(vecteur) for obj in board2.objectifs]
                     
        return ClassicBoard(grid3, objs3)

    @staticmethod
    def random_classic_board(self):

        """ rend une grille 16 x 16 générée au hasard,
        en prenant 4 quarts de plateau assemblés aléatoirement.
        Tous les objectifs des quarts de plateau y sont insérés."""

        numj = randint(0, 2)
        jaune = boardsJaunes[numj]
        numv = randint(0, 2)
        vert = boardsVerts[numv]
        numb = randint(0, 2)
        bleu = boardsBleus[numb]
        numr = randint(0, 2)
        rouge = boardsRouges[numr]
        quarts = [jaune, vert, bleu, rouge]
        couleurs = ["jaune", "vert", "bleu", "rouge"]
        # de l'affichage pour suivre l'assemblage :
        print(couleurs)
        print(numj, numv, numb, numr)
        # On les assemble dans un certain ordre (en affichant cet ordre)
        chg = randint(0, 3)
        hg = quarts.pop(chg)
        print(couleurs.pop(chg), end=" : ")

        chd = randint(0, 2)
        hd = quarts.pop(chd)
        hd.rotate_right()
        print(couleurs.pop(chd), end=" : ")

        cbd = randint(0, 1)
        bd = quarts.pop(cbd)
        print(couleurs.pop(cbd), end=" : ")
        bd.rotate_half()

        bg = quarts.pop(0)
        bg.rotate_left()
        print(couleurs[0])

        return (hg + hd) - (bg + bd)


boardsBleus = [None] * 3
for j in range(3):
    objectifs = [None] * 4
    for i in range(4):
        objectifs[i] = Objectif(ROBOT_COLORS[i], objectifsBleus[j][i])
    boardsBleus[j] = ClassicBoard(bleus[j], objectifs)

boardsJaunes = [None] * 3
for j in range(3):
    objectifs = [None] * 4
    for i in range(4):
        objectifs[i] = Objectif(ROBOT_COLORS[i], objectifsJaunes[j][i])
    boardsJaunes[j] = ClassicBoard(jaunes[j], objectifs)

boardsRouges = [None] * 3
for j in range(3):
    objectifs = [None] * 4
    for i in range(4):
        objectifs[i] = Objectif(ROBOT_COLORS[i], objectifsRouges[j][i])
    boardsRouges[j] = ClassicBoard(rouges[j], objectifs)

boardsVerts = [None] * 3
for j in range(3):
    objectifs = [None] * 4
    for i in range(4):
        objectifs[i] = Objectif(ROBOT_COLORS[i], objectifsVerts[j][i])
    boardsVerts[j] = ClassicBoard(verts[j], objectifs)


if __name__ == "__main__":
    grid1 = [[9,1,3],
             [8,6,8],
             [8,1,0]]
    objs1 = [ Objectif(RED,(1,1))]
    board1=ClassicBoard(grid1,objs1)
    grid2 = [[9,1,3],
             [2,8,2],
             [8,4,2]]
    objs2 = [ Objectif(BLUE,(1,1))]
    board2 = ClassicBoard(grid2, objs2)

    board3 = ClassicBoard(grid1,objs1)
    board3.rotate_left()
    board4 = ClassicBoard(grid2,objs2)
    board4.rotate_right()
    board = (board1 + board2) - (board3 + board4)
    board2 = ClassicBoard.random_classic_board(ClassicBoard)

#    board1 = ClassicBoard(rouge1, [obj1, obj2])
