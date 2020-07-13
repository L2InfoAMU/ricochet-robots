
# -*- coding : utf-8 -*-

""" Projet Maths Info pour le DU CCIE et la L3 Maths-Info
Chef de projet : CANALS Martin L3
Développeurs : AUBIN François DU CCIE, GIANI Théo L3
"""
#import numpy as np

# Enumération pour les directions
from enum import IntFlag
class Direction(IntFlag) :
    N = 1
    E = 2
    S = 4
    W = 8
NORTH = Direction.N
SOUTH = Direction.S
WEST = Direction.W
EAST = Direction.E

""" la classe Cell prend en charge la gestion des cases du plateau et de leurs murs
    a = Cell() : construit une case sans murs
    a = Cell(NORTH + EAST) construit une case avec des murs au nord et à l'est

    méthodes :
    wall_at(direction) : renvoie True si la case a un mur dans la direction donnée
    add_wall(direction) : permet de rajouter un mur à la case
"""
class Cell :

    def __init__(self, walls = 0 ) :
        assert (type(walls) is int )
        assert (0 <= walls <= 15)

        self.walls = Direction(walls)

    def __str__(self) : return str(int(self.walls))

    def wall_at(self, direction : int) :
        assert ( direction in [Direction.N, Direction.E, Direction.W, Direction.S])

        return self.walls & direction != 0

    def add_wall(self, direction) :
       assert ( direction in [Direction.N, Direction.E, Direction.W, Direction.S])

       self.walls = self.walls | direction


""" Board Class
    La classe Board prend en charge le plateau de jeu
    qui est un tableau d'objets de type Cell.
    Les cases sont dans des listes de listes

    Le constructeur permet la construction à partir de listes d'entiers

"""

class Board :

    def __init__(self, data) :
        self.height = len(data)
        self.width = len(data[0])

        self.grid = [ [Cell(walls) for walls in line]for line in data]
        if not self._grid_conforms() : print( "grille non conforme")
        else : print( "grille conforme")

    def __str__(self) :
        string =""
        for line in self.grid :
            for cell in line :
                string += str(cell)+" "
            string +="\n"
        return string

    """
    Méthode privée pour vérifier la conformité de la grille
            cohérence de la redondance
    """
    def _grid_conforms(self) :
        w = self.width
        h = self.height
        conforms = True
        for i in range(h) :
            for j in range(w) :
                cell = self.grid[i][j]
                if i < h-1 :
                    cell_south = self.grid[i+1][j]
                    if cell.wall_at(Direction.S) != cell_south.wall_at(Direction.N) :
                        conforms = False
                        print (" Grille non conforme au SUD en ",i," , ",j)
                if j < w-1 :
                    cell_east = self.grid[i][j+1]
                    if cell.wall_at(Direction.E) != cell_east.wall_at(Direction.W) :
                        conforms = False
                        print (" Grille non conforme à l'EST en ",i," , ",j)
        return conforms

    def cell_at(self, position) :
        i , j = position
        return self.grid[i][j]


    def save_to_file(self, fd) :
        fd.write(str(self))

    @staticmethod
    def load_from_file(fd) :
        data = []
        for line in fd :
            donnees = line.strip().split()
            if donnees == [] : continue
            data.append([ int (value) for value in donnees])
        return Board(data)



from enum import Enum
class RColors(Enum) :
    BLACK = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4


""" Class Robot
    r = Robot (RColors.RED ,group , position = (0,0) )

    Pour positionner un robot à une certaine position on utilise
    r.position = new_position

    pour déplacer un robot dans un jeu

    r.move(direction , game) avec
            direction est une du type Direction : Direction.N,
            game est une instance de la classe Game
"""

class Robot :
    def __init__(self, group, color, position ) :
        self.group = group
        self.color = color
        self.position = position

        self.group.add_robot(self)

    def __str__(self) :
        return "Robot"+str(self.color)+" at "+str(self.position)

    def move (self, dir, game) :
        robots = game.group
        board = game.board

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
    Robot_group() : crée un groupe vide de robots
    add_robot(robot) : ajoute le robot au groupe

    cell_occupied(pos) : renvoie True si un des robots du groupe
"""
class Robot_group :

    def __init__(self) :
        self.robots = dict()


    def add_robot(self, robot) :
        assert ( not self.cell_occupied(robot.position))
        assert (robot.color not in self.robots)

        self.robots[robot.color] = robot

    def cell_occupied(self, pos) :
        for _, robot in self.robots.items() :
            if robot.position == pos : return True
        return False

class Game :

    def __init__(self, board, group, goal) :
        self.board = board
        self.group = group
        self.goal = goal
        self.keys = [color for color in group.robots]

    def get_state(self) :
        return tuple([self.group.robots[key].position for key in self.keys])




a = Cell()
print(a)
print(a.wall_at(WEST))
b = Cell(SOUTH+NORTH)
print(b.wall_at(SOUTH))
print(b.wall_at(EAST))
"""
A = Board([[ 1,1,1],[2,2,2],[3,5,3]])
print(A)

fd = open("test.txt",'w')
A.save_to_file(fd)
fd.close()

fd = open("test2.txt",'r')
A = Board.load_from_file(fd)

print(A)
"""
"""
fd = open('D:/test.txt', 'r')
A = Board.load_from_file(fd)
group = Robot_group()
r1 = Robot (group, RColors.RED, (0,0) )
r2 = Robot (group, RColors.GREEN, (5,0) )

print(r1)
game = Game(A,group,None)

r1.move(SOUTH,game)
print(r1)
r1.move(EAST,game)
print(r1)
r1.move(NORTH,game)
print(r1)
r1.move(EAST,game)
print(r1)
print(game.get_state())
"""
