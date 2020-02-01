# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 09:59:40 2020

@author: Martin
"""


from RRCONST import *
from robot import*

class GameControler :
    
    
    def __init__(self, game_world) :
        
        self.world = game_world
        pass
    
    def actions():
        """renvoie la liste des actions possibles
            les actions sont données sous la forme de tuples (Couleur, Direction) """
        robots = self.game_world.robots
        liste_actions = []
        for robot in robots :
            color = robot.
            liste_actions += [