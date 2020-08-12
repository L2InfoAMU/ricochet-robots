# -*- coding : utf-8 -*-

""" Projet Maths Info pour le DU CCIE et la L3 Maths-Info
Chef de projet : CANALS Martin L3
Développeurs : AUBIN François DU CCIE, GIANI Théo L3

fichier cell.py 
définition de la classe Cell, ayant la responsabilité de manipuler
les cases du jeu.
"""

from directions import Direction, NORTH, SOUTH, EAST, WEST

""" la classe Cell prend en charge la gestion des cases du plateau et de leurs murs
    a = Cell() : construit une case sans murs
    a = Cell(NORTH + EAST) construit une case avec des murs au nord et à l'est

    méthodes :
    wall_at(direction) : renvoie True si la case a un mur dans la direction donnée
    add_wall(direction) : permet de rajouter un mur à la case
"""
class Cell :

    def __init__(self, walls = 0 ) :
        """ constructeur 
        cell = Cell(int|Direction) 
        a = Cell() : construit une case sans murs
        a = Cell(NORTH + EAST) construit une case avec des murs au nord et à l'est
        a = Cell(2) construit une case avec un mur à l'EST
        """

        assert (type(walls) is int or type(walls) is Direction)
        assert (0 <= walls <= 15)

        self.walls = Direction(walls)

    def __str__(self) : 
        """
        renvoie une représentation sous forme de chaîne de caractères de la case
        """
        return str(int(self.walls))
    

    def wall_at(self, direction : Direction) :
        """
        renvoie True si la cellule possède un mur à la direction donnée
        """

        assert ( direction in Direction)

        return self.walls & direction != 0

    def add_wall(self, direction) :
        """
        permet d'ajouter un mur à la cellule dans la direction donnée
        """ 
        assert ( direction in Direction)
        self.walls = self.walls | direction

    def rotate_left(self) :
        """ 
        effectue une rotation des murs de la cellule d'un quart de tour vers la gauche.
        L'objet est modifiée en place et  la méthode renvoie la référence de la cellule
        """
        walls = Direction(0)
        if self.wall_at(Direction.E) : walls = walls |Direction.N
        if self.wall_at(Direction.N) : walls = walls |Direction.W
        if self.wall_at(Direction.W) : walls = walls |Direction.S
        if self.wall_at(Direction.S) : walls = walls |Direction.E
        self.walls = walls
        return self

    def rotate_right(self) :
        """ 
        effectue une rotation des murs de la cellule d'un quart de tour vers la droite.
        L'objet est modifiée en place et  la méthode renvoie la référence de la cellule
        """
 
        walls = Direction(0)
        if self.wall_at(Direction.E) : walls = walls |Direction.S
        if self.wall_at(Direction.N) : walls = walls |Direction.E
        if self.wall_at(Direction.W) : walls = walls |Direction.N
        if self.wall_at(Direction.S) : walls = walls |Direction.W
        self.walls = walls
        return self

    def rotate_half(self) :
        """ 
        effectue une rotation des murs de la cellule d'un quart de tour vers la gauche.
        L'objet est modifiée en place et  la méthode renvoie la référence de la cellule
        """
 
        walls = Direction(0)
        if self.wall_at(Direction.E) : walls = walls |Direction.W
        if self.wall_at(Direction.N) : walls = walls |Direction.S
        if self.wall_at(Direction.W) : walls = walls |Direction.E
        if self.wall_at(Direction.S) : walls = walls |Direction.N
        self.walls = walls
        return self

