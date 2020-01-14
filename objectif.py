# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 01:24:31 2020

@author: Martin
"""


class Objectif :
    
    def __init__(self, color , target):
        self.color = color
        self.position = target
        
       
    def rotate_left(self, dim):
        """ Calcule la position de l'objectif après rotation 
        d'un 1/4 de tour vers la gauche dans une grille de dimension 
        dim =  (m,n) """
        m, n = dim
        x, y = self.position
        self.position = (n-1-y, x )
        
    def rotate_half(self, dim):
        """ Calcule la position de l'objectif après rotation 
        d'un 1/2  tour  une grille de dimension 
        dim =  (m,n) """
        m, n = dim
        x, y = self.position
        self.position = (m-1-x, n-1-y)

    def rotate_left(self, dim):
        """ Calcule la position de l'objectif après rotation 
        d'un 1/4 de tour vers la gauche dans une grille de dimension 
        dim =  (m,n) """
        m, n = dim
        x, y = self.position
        self.position = (y, m-1-x )