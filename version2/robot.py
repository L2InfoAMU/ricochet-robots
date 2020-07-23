
# -*- coding : utf-8 -*-

""" Projet Maths Info pour le DU CCIE et la L3 Maths-Info
Chef de projet : CANALS Martin L3
Développeurs : AUBIN François DU CCIE, GIANI Théo L3

"""


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

    def rotate_left(self) :
        walls = Direction(0)
        if self.wall_at(Direction.E) : walls = walls |Direction.N
        if self.wall_at(Direction.N) : walls = walls |Direction.W
        if self.wall_at(Direction.W) : walls = walls |Direction.S
        if self.wall_at(Direction.S) : walls = walls |Direction.E
        self.walls = walls
        return self
    
    def rotate_right(self) :
        walls = Direction(0)
        if self.wall_at(Direction.E) : walls = walls |Direction.S
        if self.wall_at(Direction.N) : walls = walls |Direction.E
        if self.wall_at(Direction.W) : walls = walls |Direction.N
        if self.wall_at(Direction.S) : walls = walls |Direction.W
        self.walls = walls
        return self
    
    def rotate_half(self) :
        walls = Direction(0)
        if self.wall_at(Direction.E) : walls = walls |Direction.W
        if self.wall_at(Direction.N) : walls = walls |Direction.S
        if self.wall_at(Direction.W) : walls = walls |Direction.E
        if self.wall_at(Direction.S) : walls = walls |Direction.N
        self.walls = walls
        return self
  



""" Board Class
    La classe Board prend en charge le plateau de jeu
    qui est un tableau d'objets de type Cell.
    Les cases sont dans des listes de listes

    Le constructeur permet la construction à partir de listes d'entiers

"""

class Board :

    def __init__(self, data=[], check_conformity = False) :
        self.height = len(data)
        if self.height > 0 :
            self.width = len(data[0])
        else : self.width = 0

        self.grid = [ [Cell(walls) for walls in line]for line in data]

        if check_conformity :
            if not self._grid_conforms() : print( "grille non conforme")
            else : print( "grille conforme")

    def __str__(self) :
        string ="["
        n = 0
        for line in self.grid :
            if n > 0 : string += ","
            string += "\n["
            n += 1
            m = 0
            for cell in line :
                if m > 0 : string += ", "
                m += 1
                string += str(cell)
            string +="]"
        string += "]"
        return string

    """
    Méthode privée pour vérifier la conformité de la grille
            cohérence de la redondance
    """
    def _grid_conforms(self, verbose = False) :
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
                        if verbose :
                            print (" Grille non conforme au SUD en ",i," , ",j)
                if j < w-1 :
                    cell_east = self.grid[i][j+1]
                    if cell.wall_at(Direction.E) != cell_east.wall_at(Direction.W) :
                        conforms = False
                        if verbose :
                            print (" Grille non conforme à l'EST en ",i," , ",j)
        return conforms

    def cell_at(self, position) :
        i , j = position
        return self.grid[i][j]


    def write_to_file(self, fd) :
        fd.write(str(self))



    @staticmethod
    def load_from_file(fd) :         
        """ méthode ancienne à ne plus utiliser """   
        
        data = []
        for line in fd :
            donnees = line.strip().split()
            if donnees == [] : continue
            data.append([ int (value) for value in donnees])
        return Board(data)

    @staticmethod
    def load_from_json(fd, *names) :
        """ charge des grille depuis un fichier json, 
            usage  : boards =  Board.load_from_json( fd , names)
                    fd est un descripteur de fichier
                    names est une liste de noms , par défaut 'grid'
                    *** renvoie un tuple ***
                    Pour charger une seule grille :
                    board , = Board.load_from_json( fd , 'grid')
        """
        if len(names) == 0 : names =('grid',)
        import json

        data = json.load(fd)
        boards = []
        for name in names :
             if name in data :
                 boards.append(Board(data[name]))
        return tuple(boards)

    def rotate_left(self) :
        nbcol , nblin = self.width , self.height
        turned_grid = [[ self.grid[i][nbcol-j-1].rotate_left() for i in range(nblin)] for j in range(nbcol)]

        self.grid = turned_grid
        self.width , self.height = nblin , nbcol
        return self

    def rotate_right(self) :
        nbcol , nblin = self.width , self.height
        turned_grid = [[ self.grid[nblin-1-i][j].rotate_right() for i in range(nblin)] for j in range(nbcol)]
        
        self.grid = turned_grid
        self.width , self.height = nblin , nbcol
        return self

    def rotate_half(self) :
        nbcol , nblin = self.width , self.height
        turned_grid = [[ self.grid[nblin-1-i][nbcol-1-j].rotate_half() for j in range(nbcol)] for i in range(nblin)]
        self.grid = turned_grid
        self.width , self.height = nbcol , nblin
        return self

    def __add__(self, board2) :
        """ juxtaposition horizontale de deux grilles """
        # dimensions
        nl1, nc1 = self.height, self.width
        nl2, nc2 = board2.height, board2.width

        #compatibilité
        assert( nl1 == nl2)

        # jonctions des grilles
        grid3 = []
        for num_line in range (nl1) :
            grid3.append(self.grid[num_line] + board2.grid[num_line])
        
        # suture
        for i in range (nl1) :
            if grid3[i][nc1-1].wall_at(EAST) or grid3[i][nc1].wall_at(WEST) :
                grid3[i][nc1-1].add_wall(EAST)
                grid3[i][nc1].add_wall(WEST)
        
        board = Board()
        board.grid = grid3
        board.height = nl1
        board.width = nc1 + nc2
        return board

   #@staticmethod
    def __sub__(board1, board2) :
        """ juxtaposition horizontale de deux grilles """
        # dimensions
        nl1, nc1 = board1.height, board1.width
        nl2, nc2 = board2.height, board2.width

        #compatibilité
        assert( nc1 == nc2)

        # jonctions des grilles
        grid3 = board1.grid + board2.grid
        
        # suture
        for i in range (nc1) :
            if grid3[nl1-1][i].wall_at(SOUTH) or grid3[nl1][i].wall_at(NORTH) :
                grid3[nl1-1][i].add_wall(SOUTH)
                grid3[nl1][i].add_wall(NORTH)
        
        board = Board()
        board.grid = grid3
        board.height = nl1 + nl2
        board.width = nc1 
        return board




 



from enum import Enum
class RColors(Enum) :
   # BLACK = 0
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
        return "Robot"+str(self.color.name)+" at "+str(self.position)

    def move (self, dir, game) :
        robots = game.robots
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
    un robot est une couleur, par exemple RColors.RED

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
robots : un groupe de robots, instance de la classe Robot_group
goal : l'objectif du jeu
states_list : la liste de tous les états du jeu depuis le début,
            permettant de revenir en arrière
Méthodes :
    get_state() :
        renvoie un tuple contenant les positions des robots.
        L'ordre des positions est dans la liste keys.
    set_state(state) :
        positionne les robots dans d'après les positions de state
    state_is_won (state) :
        renvoie True si l'état est gagnant , False sinon
    is_won() :
        renvoie True si le jeu est en état gagnant
    actions_list() :
        renvoie la liste des actions possibles pour un agent
    do_action(action) :
        effectue l'action donnée sur le jeu et renvoie l'état du jeu
    undo() :
        annule la dernière action

"""

class Game :
    color_names = {
                    RColors.RED : 'R',
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
    #    self.group = robots
        self.robots = robots
        self.goal = goal
        self.states_list = []
        self.color_keys = [color for color in robots]

    def add_board(self, board):
        self.board = board

    def add_goal(self, goal):
        self.goal = goal

    def add_robots(self, robots):
        self.robots = robots
        self.color_keys = [color for color in robots]

    def get_state(self) :
        return tuple([self.robots[color].position for color in self.color_keys])

    def set_state(self, state) :
        for r_color, position in zip(self.color_keys, state) :
            self.robots[r_color].position = position

    def state_is_won(self, state) :
        index = self.color_keys.index(self.goal.color)
        return state[index] == self.goal.position

    def is_won(self) :
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
        #print(color)    #pour le test/à enlever
        direction = self.direction_by_name[dir_name]
        robot = self.robots[color]
        robot.move(direction, self)
        self.states_list.append(self.get_state)
        return self.get_state()

    def do_actions(self, *actions) :
        for action in actions :
            state = self.do_action(action)
        return state

    def undo(self):
        self.set_state(self.states_list.pop())
    
    def save_2_json(self, fp) :
        """ writing data to a text file, using json format 
        {       
        "grid" : [ [int, ..., int],
                            ...
                    [int, ..., int]
                    ] ,
        "robots" :  {
            "R" : [x , y],

            }               
        "Goal" : {
            "color" : "R",
            "position" : [x , y]
            }
        }
        """
        fp.write("{\n")
        fp.write('"grid" : [')
        nblines = len (self.board.grid)
        for num_line in range(nblines):
            if num_line > 0 : fp.write(",")
            fp.write("\n\t[")
            line = self.board.grid[num_line]
            nbcells = len (line)
            for num_cell in range (nbcells) :
                if num_cell > 0 : fp.write(", ")
                fp.write(str(line[num_cell]))
            fp.write(" ]")
        fp.write("\n\t],")
        fp.write('\n"robots" : { ')
        
        num_robot = 0
        for c, r in self.robots.items() :
            if num_robot > 0 : fp.write(",")
            
            fp.write(f'\n"{Game.color_names[c]}" : [{r.position[0]} , {r.position[1]}] ')
            num_robot += 1
        fp.write("\n\t },")
        fp.write('\n"goal" : { ')
        color = self.goal.color
        position = self.goal.position
        fp.write(f'\n\t"color" : "{Game.color_names[color]}",')
        fp.write(f'\n\t"position" : [{position[0]}, {position[1]}]')
        fp.write("\n\t}")
        fp.write("\n}")

    @staticmethod
    def load_from_json(fp) :
        import json

        board = None
        group = None
        goal = None 

        data = json.load(fp)
        if "grid" in data :
            data_grid = data["grid"]
            board = Board(data_grid)

        if "robots" in data :
            data_robots = data["robots"]
            group = Robot_group()
            for color_name, position in data_robots.items() :
                Robot(group,Game.color_by_name[color_name],tuple(position))
        if "goal" in data :
            color = Game.color_by_name[data["goal"]["color"]]
            position = tuple(data["goal"]["position"])
            goal = Goal(color, position)
        return Game(board, group, goal)




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
