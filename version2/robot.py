
# -*- coding : utf-8 -*-

""" Projet Maths Info pour le DU CCIE et la L3 Maths-Info
Chef de projet : CANALS Martin L3
Développeurs : AUBIN François DU CCIE, GIANI Théo L3

"""
from collections import deque
from rcolors import RColors
from directions import Direction, NORTH, SOUTH, EAST, WEST
from cell import Cell
from board import Board
from goal import Goal

""" Class Robot
    r = Robot (RColors.RED ,group , position = (0,0) )

    __str__ : méthode de conversion en chaîne de caractères, format json
            str(r) renvoie '"R" : [0,0]'
            Rappel, les couleurs sont "R", "B", "Y", "G"

    Pour positionner un robot à une certaine position on utilise
    r.position = new_position

    pour déplacer un robot dans un jeu

    r.move(direction , board) avec
            direction est une du type Direction : Direction.N,
            board est une instance de la classe Board
"""

class Robot :
    def __init__(self, group, color, position ) :
        self.group = group
        self.color = color
        self.position = position

        self.group.add_robot(self)

    def __str__(self) :
        """ renvoie une représentation du robot sous forme de chaîne de caractères
            "R" : [x,y]
        """

        return f'"{str(self.color)}" : {str(list(self.position))}'

    def move (self, dir, board) :
        robots = self.group


        if dir == Direction.N :
            next_position = lambda pos : (pos[0]-1 , pos[1])
        if dir == Direction.S :
            next_position = lambda pos : (pos[0]+1 , pos[1])
        if dir == Direction.E :
            next_position = lambda pos : (pos[0] , pos[1]+1)
        if dir == Direction.W :
            next_position = lambda pos : (pos[0] , pos[1]-1)

        target = self.position

        while not board.cell_at(self.position).wall_at(dir) :
            target = next_position(self.position)
            if robots.cell_occupied(target) :
                 break
            else :
                self.position = target

""" classe qui gère un groupe de robots
    Un groupe de robots est un dictionnaire  { color : robot ,... }
    color est une instance de RColors
    robot est une instance de Robot
    Robot_group() : crée un groupe vide de robots
    add_robot(robot) : ajoute le robot au groupe en prenant comme clé d'entrée robot.color
        l'ajout d'un deuxième robot de même couleur provoque une AssertionError
        l'ajout d'un robot ayant une position identique à un autre robot provoque AssertionError

    la méthode
    cell_occupied(position :tuple(x,y)) : booleen
    renvoie True si un des robots du groupe occupe la position

    la méthode __str__ renvoie une chaîne de caractères pour le groupe de robots.
    robots : {
        'R' : [x, y],
        'B' : [x, y],
    }

"""
class Robot_group(dict) :

    def add_robot(self, robot) :
        assert ( not self.cell_occupied(robot.position))
        assert (robot.color not in self)
        self[robot.color] = robot

    def cell_occupied(self, pos) :
        for _, robot in self.items() :
            if robot.position == pos : return True
        return False
    def __str__(self) :
        string =  '"robots" : {'
        num_robot = 0
        for color in self :
            if num_robot > 0 : string +=','
            string = string+'\n\t'+str(self[color])
            num_robot += 1
        string+= "\n\t}"
        return string
