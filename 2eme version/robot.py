
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
class Robot_group(dict) :

    def add_robot(self, robot) :
        assert ( not self.cell_occupied(robot.position))
        assert (robot.color not in self)
        self[robot.color] = robot

    def cell_occupied(self, pos) :
        for _, robot in self.items() :
            if robot.position == pos : return True
        return False
""" 
La classe Game a pour rôle la gestion des actions sur le plateau de jeu
Les attributs sont 
board : un plateau de jeu
group : un groupe de robots
goal : l'objectif du jeu
Méthodes :
    get_state() : 
        renvoie un tuple contenant les positions des robots.
        L'ordre des positions est dans la liste keys.
    set_state(state) : 
        positionne les robots dans d'après les positions de state
    state_is_win (state) : 
        renvoie True si l'état est gagnant , False sinon
    game_is_win() :
        renvoie True si le jeu est en état gagnant
    actions_list() :
        renvoie la liste des actions possibles pour un agent
    do_action(action) :
        effectue l'action donnée sur le jeu et renvoie l'état du jeu

"""

class Game :
    color_names = { RColors.RED : 'R',
                    RColors.BLUE : 'B',
                    RColors.YELLOW :'Y',
                    RColors.GREEN : 'G'}
    color_by_name = {'R' : RColors.RED,
                      'B' : RColors.BLUE,
                      'Y' : RColors.YELLOW,
                      'G' : RColors.GREEN}
    direction_names = {Direction.E : 'E',
                        Direction.S : 'S',
                        Direction.N : 'N',
                        Direction.W : 'W'}
    direction_by_name = {'N' : Direction.N,
                            'E' : Direction.E,
                            'S' : Direction.S,
                            'W' : Direction.W}

    def __init__(self, board, robots, goal ):
        self.board = board
        self.group = robots
        self.robots = robots
        self.goal = goal
        self.color_keys = [color for color in robots]

    def get_state(self) :
        return tuple([self.robots[color].position for color in self.color_keys])

    def set_state(self, state) :
        for r_color, position in zip(self.color_keys, state) :
            self.robots[r_color].position = position
    
    def state_is_win(self, state) :
        index = self.color_keys.index(self.goal.color)
        return state[index] == self.goal.position

    def is_win(self) :
        return self.robots[self.goal.color].position == self.goal.position

    def actions_list(self) :
        actions = [] 
        for color in self.color_keys :
            color_name = self.color_names[color]
            for direction in Direction :
                dir_name = self.direction_names[direction]
                actions.append(color_name+dir_name)
        return actions

    def do_action(self, action) :
        color_name, dir_name = action[0], action[1]
        color = self.color_by_name[color_name]
        direction = self.direction_by_name[dir_name]
        robot = self.robots[color]
        robot.move(direction, self)
        return self.get_state()

    def do_actions(self, *actions) :
        for action in actions :
            state = self.do_action(action)
        return state



""" 
la classe Goal permet de créer des objets pour l'objectif du jeu.
Un objectif est la donnée d'une couleur et d'une position
    goal = Goal(RColors.GREEN, (0,4))

    On accède aux champs par :
    goal.color
    goal.position
"""
class Goal :
    def __init__(self, color, position) :
        self.color = color
        self.position = position


"""
a = Cell()
print(a)
print(a.wall_at(WEST))
b = Cell(SOUTH+NORTH)
print(b.wall_at(SOUTH))
print(b.wall_at(EAST))

A = Board([[ 1,1,1],[2,2,2],[3,5,3]])
print(A)

fd = open("test.txt",'w')
A.save_to_file(fd)
fd.close()

fd = open("test2.txt",'r')
A = Board.load_from_file(fd)

print(A)

"""
fd = open("test2.txt",'r')
A = Board.load_from_file(fd)
group = Robot_group()
r1 = Robot (group, RColors.RED, (0,0) )
r2 = Robot (group, RColors.GREEN, (4,0) )
r3 = Robot (group, RColors.BLUE, (3,4) )
r4 = Robot (group, RColors.YELLOW, (2,4) )
goal = Goal(RColors.GREEN, (4,2))
game = Game(A,group,goal)
print (game.actions_list() )

state = game.do_action("RS")
state = game.do_actions("RE","GN","RN","BW","BN","YS" )

"""
print(game.get_state())

print ("etat gagnant ? ", game.state_is_win(game.get_state()))
r1.move(SOUTH,game)
print(r1)
r1.move(EAST,game)
print(r1)
r1.move(NORTH,game)
print(r1)
r1.move(EAST,game)
r2.move(EAST, game)
r2.move(EAST, game)
print(game.get_state())
print ("etat gagnant ? ", game.state_is_win(game.get_state()))
state = ((1, 4), (4, 2), (3, 4), (2, 4))
game.set_state(state )
print(game.get_state())
"""

"""
import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(400, 300)
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw_something()


    def draw_something(self):
        painter = QtGui.QPainter(self.label.pixmap())
       
        names=["Empty","N","E","EN","S","NS","ES","ENS","W","NW","EW","ENW","SW","NSW","ESW","ENSW"]
        images = [QtGui.QPixmap("./images/"+name+".bmp", format="bmp")  for name in names]
        painter.drawPixmap(QtCore.QPoint(0,0) , images[9])
        painter.drawPixmap(QtCore.QPoint(50,0) , images[3])
        painter.drawPixmap(QtCore.QPoint(0,50) , images[13])
        painter.drawPixmap(QtCore.QPoint(50,50) , images[6])                               
        painter.end()
        
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
"""