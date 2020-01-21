# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 00:16:45 2020

robot.py
@author: François Aubin,Martin Canals, Théo Giani
"""

from RRCONST import *
import board


class Robot:
    """ Classe robot
    # qui contient la position du robot : tuple(x , y)
    # un identificateur
    # une référence au plateau sur laquelle il se déplace robot.board
    # la liste des robots sur le plaeau : robot.friends
    # On accède aux champs par robot.position, robot.numero, 
    # 
    # to do , écrire des méthodes set et get pour chaque champ  ?
    """
    def __init__(self,position,id_robot):
        
        assert(0 <= id_robot < MAX_ROBOT)
        self.position = position
        self.numero = id_robot
    #    self.color = color    mauvaise idée , 
        
    def __repr__(self):
        """ pour les besoins de test seulement"""
        return "r" + str(self.numero) \
                + " à la position" + str(self.position)
                
    def cell_is_free(self, pos):
        """ renvoie True si la case cell est occupée par un robot """
        """ pos est un tuple (x,y) correspondant à une case de la grille """
       
        for robot in self.friends :
           if robot.position == pos : return False
        return True
    
    def move_to(self, position) : 
        """ déplace le robot à la position donnée """
        # La méthode est-elle insdispensable ?
        self.position = position
        
    
    def move(self, direction) :
        """ deplace robot sur le plateau suivant la direction
            la position de robot est changée """
    
        def step_builder(direction):
            """ renvoie une fonction qui calcule la prochaine position"""
            if direction == SOUTH:
                return lambda pos: (pos[0]+1, pos[1])
            if direction == NORTH:
                return lambda pos: (pos[0]-1, pos[1])
            if direction == EAST:
                return lambda pos: (pos[0], pos[1]+1)
            if direction == WEST:
                return lambda pos: (pos[0], pos[1]-1)
    
        next_position = step_builder(direction)
    
        while self.world.cell_is_open(self.position, direction):
            target = next_position(self.position)
            if not self.cell_is_free(target): break
         
        robot.position = target