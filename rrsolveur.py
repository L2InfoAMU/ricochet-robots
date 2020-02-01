# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 22:24:39 2019

@author: Martin
"""


# Classe solveur pour le jeu ricochets robot

# Utilisation du type deque pour piles et files.

from collections import deque
import game as g


class RRSolveur :
    
    def __init__(game_controler , state_encoder) :
        self.gc = game_controler
        
        self.actions = game_controler.actions()
        node_0 = state_encoder.encode(game_controler.initial_state()) 
        
        
        
        
    def Solve(game) :
        """ game est un objet de classe Game """
        
        # Listes des actions possibles 
        
        
        actions = deque([])         # pile des actions
        
        initial_state = game.state()
        states = { initial_state : None}      # dictionnaire des états 
        
        node_queue = deque ([initial_state])
        
        
        
        
    
        
        