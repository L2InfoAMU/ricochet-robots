""" Projet Maths Info pour le DU CCIE et la L3 Maths-Info
Chef de projet : CANALS Martin L3
Développeurs : AUBIN François DU CCIE, GIANI Théo L3

fichier game.py
définition de la classe Game, ayant la responsabilité de piloter le jeu.
Le jeu est composé d'un plateau, d'un groupe de robots et d'un objectif.
Les attributs sont
board : un plateau de jeu
robots : un groupe de robots, instance de la classe Robot_group
goal : l'objectif du jeu
record : booléen indiquant si l'on doit maintenir la pile des états du jeu
    par défaut record est à True, le mettre à False lorsqu'on est en recherche automatique de solution.
state_start : état initial du jeu, permettant de remettre le eju à son état initial
states_list : la liste de tous les états du jeu depuis le début,
            permettant de revenir en arrière
        Si le paramètre record est positionné à False, cette liste n'est pas maintenue
moves_list : la liste des actions effectuées depuis le début du jeu
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
from collections import deque
from directions import Direction, NORTH, SOUTH, EAST, WEST
from rcolors import RColors
from cell import Cell
from board import Board
from robot import Robot, Robot_group
from goal import Goal

class Game :

    def __init__(self, board, robots, goal, record = True):
        """ Constructeur
        game = Game(board, robots, goal, record)
        Si record est positionné à True, le jeu conserve les différents états dans une pile
        ce qui permet de revenir à un état précédent.
        """
        self.board = board
        self.robots = robots
        self.goal = goal
        self.record = record

        # table des entrées couleurs pour l'ordre des positions décrivant un état
        self.color_keys = [color for color in robots]

        # état de départ
        self.state_start = self.get_state()
        #self.states_list = []
        #self.states_list.append(self.get_state())
        # Pile des états

        self.states_list = deque( [self.state_start], maxlen = 100)
        self.moves_list = []


    def add_board(self, board):
        """ redéfinit la grille de jeu """
        self.board = board

    def add_goal(self, goal):
        """ redéfinit l'objectif du jeu """
        self.goal = goal
    def add_robots(self, robots):
        """ redéfinit le groupe de robots """
        self.robots = robots
        self.color_keys = [color for color in robots]

    def get_state(self) :
        """
        renvoie l'état du jeu sous forme d'un tuple dcontenant les positions
        des robots.
        L'ordre des robots dans ce tuple peut être obtenu par l'attribut color_keys
        """

        return tuple([self.robots[color].position for color in self.color_keys])

    def set_state(self, state) :
        """
        Met le jeu dans l'état décrit par le tuple de positions state
        """
        for r_color, position in zip(self.color_keys, state) :
            self.robots[r_color].position = position


    def state_is_won(self, state) :
        """
        renvoie True si state est un état gagnant
        """
        index = self.color_keys.index(self.goal.color)
        return state[index] == self.goal.position

    def is_won(self) :
        """
        renvoie True si le jeu est actuellement dans un etat gagnant
        """
        return self.robots[self.goal.color].position == self.goal.position

    def actions_list(self) :
        """
        Renvoie la liste des actions possibles.
        Chaque action est une chaîne de 2 caractères.
        Le premier caractère est la couleur du robot, le deuxième est la direction.
        Exemple : si game ne comporte qu'un robot rouge
        game.actions_list() renvoie ["RN","RE","RS","RW"]
        """
        actions = []
        for color in self.color_keys :
            color_name = str(color)
            for direction in Direction :
                actions.append(color_name+str(direction))
        return actions

    def do_action(self, action) :
        """
        Demande au jeu d'effectuer l'action décrite par la chaîne de caractères action
        Exemple :
            game.do_action("YN") demande au jeu de déplacer le robot Y (yellow) vers le Nord
        """
        color_name, dir_name = action[0], action[1]
        color = RColors.from_str(color_name)
        #print(color)    #pour le test/à enlever
        direction = Direction.from_str(dir_name)
        robot = self.robots[color]
        robot.move(direction, self.board)
        if self.record :
            self.states_list.append(self.get_state())
            self.moves_list.append(action)
        return self.get_state()

    def do_actions(self, *actions) :
        """
        Demande au jeu d'effectuer une liste d'actions les unes à la suite des autres
        Renvoie l'état final
        """
        for action in actions :
            state = self.do_action(action)
        return state

    def undo(self):
        """
        Demande au jeu de revenir à l'état précedent
        Pour utiliser cette fonctionnalité il faut avoir créé le jeu avec record = True
        """
        # on ne peut pas dépiler l'état initial
        if len(self.states_list) > 1 :
            self.states_list.pop()
            self.moves_list.pop()
            self.set_state(self.states_list[-1])
            return self.get_state()

    # deprecated method, use save_to_json instead
    def save_2_json(self, fp) :
        """ 
        méthode obsolète
        writing data to a text file, using json format

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

            fp.write(f'\n"{str(c)}" : [{r.position[0]} , {r.position[1]}] ')
            num_robot += 1
        fp.write("\n\t },")
        fp.write('\n"goal" : { ')
        color = self.goal.color
        position = self.goal.position
        fp.write(f'\n\t"color" : "{str(color)}",')
        fp.write(f'\n\t"position" : [{position[0]}, {position[1]}]')
        fp.write("\n\t}")
        fp.write("\n}")

    def save_to_json(self, filename) :
        """
        Ecrit les données de jeu dans un fichier texte, au format json.
        Le format est le suivant :
        {
        "grid" : [ [int, ..., int],
                            ...
                    [int, ..., int]
                    ] ,
        "robots" :  {
            "R" : [x, y],
            "Y" : [x, y]
            }
        "Goal" : {
            "color" : "R",
            "position" : [x , y]
            }
        }
        """
        with open(filename,'w') as fd :
            fd.write("{")
            fd.write("\n"+str(self.board))
            fd.write(",\n"+str(self.robots))
            fd.write(",\n"+str(self.goal))
            fd.write('\n}')


    @staticmethod
    def load_from_json(filename) :
        """
        Charge et renvoie un jeu chargé depuis un fichier texte au format json
        """

        import json

        board = None
        group = None
        goal = None
        with open(filename,'r') as fd :
            data = json.load(fd)

        if "grid" in data :
            data_grid = data["grid"]
            board = Board(data_grid)

        if "robots" in data :
            data_robots = data["robots"]
            group = Robot_group()
            for color_name, position in data_robots.items() :
                Robot(group,RColors.from_str(color_name),tuple(position))
        if "goal" in data :
            assert( "color" in data["goal"])
            assert (data["goal"]["color"] in {'R','G','B','Y'})
            color = RColors.from_str(data["goal"]["color"])

            assert ("position" in data["goal"])
            position = tuple(data["goal"]["position"])

            goal = Goal(color, position)
        return Game(board, group, goal)
