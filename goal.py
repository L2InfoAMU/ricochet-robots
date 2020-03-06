# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 00:30:28 2020

@author: François Aubin, Martin canals, Théo Giani
"""
from RRCONST import *


class Goal:
    """ crée un objet Goal qui correspond à l'objectif du jeu
        Amener robot à sur la case target, 
        robot est un objet de la classe Robot 
        target est un tuple (i,j) d'entiers """
        
    def __init__(self, robot, target):
        self.robot = robot
        self.target = target
        
    def is_complete(self):
        """ renvoie True si l'objectif du jeu est rempli, False sinon"""
        return self.robot.position == self.target
