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
    # une référence au monde dans lequel évolue le robot : robot.world
    # robot.world.robots , robot.world.board
    # On accède aux champs par robot.position, robot.numero, 
    # 
    # to do , écrire des méthodes set et get pour chaque champ  ?
    """
    def __init__(self,position,color):
        
        assert(color in ROBOT_COLORS)
        self.position = position
#        self.numero = id_robot
        self.color = color    
        
    def __repr__(self):
        """ pour les besoins de test seulement"""
        return "r" + str(self.color) \
                + " à la position" + str(self.position)
                
    def cell_is_free(self, pos):
        """ renvoie True si la case cell est occupée par un robot """
        """ pos est un tuple (x,y) correspondant à une case de la grille """
        friends = self.world.robots
        for robot in friends :
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
        board = self.world.board
        target = self.position
        while board.cell_is_open(self.position, direction):
            target = next_position(self.position)
            if not self.cell_is_free(target): break
            else : 
                self.position = target
