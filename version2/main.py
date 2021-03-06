# -*- coding : utf-8 -*-

""" Projet Maths Info pour le DU CCIE et la L3 Maths-Info
Chef de projet : CANALS Martin L3
Développeurs : AUBIN François DU CCIE, GIANI Théo L3

Ce contrôleur graphique permet de jouer à ricochet robot de manière complète, par appel au moteur interne du jeu.

"""

import sys
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow , QLabel, QPushButton, QMainWindow, QAction, QToolBar, QVBoxLayout, QComboBox, QHBoxLayout, QCheckBox, QDialog, QDialogButtonBox, QPlainTextEdit, QFileDialog
from PySide2.QtGui import QKeySequence, QPainter, QColor, QIcon, QPixmap
from PySide2.QtCore import Qt, QPoint
from directions import Direction, NORTH, SOUTH, EAST, WEST
from rcolors import RColors
from robot import Robot, Robot_group
from board import Board
from game import Game
from goal import Goal
from random import *
from solveur import solveur
from collections import deque

ICON_PATH = "./icons/"
IMAGES_PATH = "./images/"
GAMES_PATH = './games/'
DEFAULT_GAME = "game1.json"
GRIDS_PATH = "./grids/"

class MainWindow(QMainWindow):
    DIMENSION = 560
    placement_aleatoire = True
    nb_robots = 0

    def __init__(self, game):
        """
        La fenêtre principale est initialisée avec l'organisation suivante :

        +--------------------------------------------------------------------------+
        |              self.menu = self.menuBar()                                  |
        |                                                                          |
        +--------------------------------------------------------------------------+
        |       toolbar = QToolBar()  (déplacement/sélection des robots,           |
        |                     boutons annuler, indice et solution)                 |
        +------------------------layout0 = QHBoxLayout()---------------------------+
        |    layout2 = QHBoxLayout()                  +      moves_label           |
        | l                    +                      |                            |
        | a  grid_choice       |  nb_robots_choice    |     (affichage des         |
        +-y--------------------+----------------------+  L                         |
        | o                                           |  a  mouvements effectués)  |
        | u                                           |  y                         |
        | t                                           +--o-------------------------+
        | =          label = QLabel()                 |  u                         |
        | Q                                           |  t     tip_label           |
        | V          contient la grille de jeu        |  3                         |
        | B                                           |      (Affichage de l'indice|
        | o                                           |  =                         |
        | x                                           |      si demandé)           |
        | L                                           |  Q                         |
        | a                                           +--V+------------------------+
        | y                                           |  B     solution_label      |
        | o                                           |  o                         |
        | u                                           |  x   (Affichage de la      |
        | t                                           |                            |
        |                                             |      solution si demandée) |
        +---------------------------------------------+----------------------------+

        """

        super().__init__()
        self.game = game
        self.initial_game_state = self.game.get_state()
        self.number_moves = 0
        self.setWindowTitle("Robot Ricochet")
        self.resize(self.DIMENSION + 150, self.DIMENSION + 100)

        # label contient la grille de jeu
        self.label = QLabel()
        canvas = QPixmap(self.DIMENSION , self.DIMENSION)
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)

        # layout0 contient, à gauche, les barres d'outils et la grille,
        # et à droite, la liste des états et l'indice affiché par le solveur

        layout0 = QHBoxLayout()
        layout0.setContentsMargins(0,0,0,0)
        layout0.setSpacing(0)

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout2 = QHBoxLayout()

        # Choix de la grille
        self.choice_of_grid_menu()

        # choix du nombre de robots
        self.nb_robots_choice_menu()

        # CheckBox placement aléatoire
        widget3 = QCheckBox("Placement aléatoire des robots et de l'objectif")
        widget3.setCheckState(Qt.Checked)
        widget3.stateChanged.connect(self.placer_aleatoirement)


        # layout2 contient les 3 widgets horizontaux de choix de grille, robots et aléa
        layout2.addWidget(self.grid_choice)
        layout2.addWidget(self.nb_robots_choice)
        #layout2.addWidget(widget3)
        layout2.setContentsMargins(0,0,0,0)
        layout2.setSpacing(0)
        widget2 = QWidget()
        widget2.setLayout(layout2)

        layout.addWidget(widget2)
        layout.addWidget(self.label)


        # liste des mouvement effectués, indice et solution:
        layout3 = QVBoxLayout()
        layout3.setContentsMargins(0,0,0,0)
        layout3.setSpacing(0)

        self.moves_label = QLabel()
        self.print_moves_list()
        self.tip_label = QLabel()
        self.solution_label = QLabel()

        layout3.addWidget(self.moves_label)
        layout3.addWidget(self.tip_label)
        layout3.addWidget(self.solution_label)

        layout0.addLayout(layout)
        layout0.addLayout(layout3)
        widget = QWidget()
        widget.setLayout(layout0)
        self.setCentralWidget(widget)


        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.help_menu = self.menu.addMenu("Aide et instructions")    # A faire
        self.size_fenetre = self.geometry()

        # Play QAction
        play_action = QAction("Réinitialiser !", self)
        play_action.triggered.connect(self.replay)
        self.file_menu.addAction(play_action)

        # Open_grid QAction
        open_grid_action = QAction("Ouvrir une grille", self)
        open_grid_action.setShortcut('Ctrl+O')
        open_grid_action.triggered.connect(self.open_grid)
        self.file_menu.addAction(open_grid_action)

        # Open_game QAction
        open_game_action = QAction("Ouvrir un jeu", self)
        open_game_action.triggered.connect(self.open_game)
        self.file_menu.addAction(open_game_action)

        # Save_grid QAction
        save_grid_action = QAction("Enregistrer cette grille", self)
        save_grid_action.triggered.connect(self.save_grid)
        self.file_menu.addAction(save_grid_action)

        # Save_game QAction
        save_game_action = QAction("Enregistrer ce jeu", self)
        save_game_action.triggered.connect(self.save_game)
        self.file_menu.addAction(save_game_action)

        # Exit QAction
        exit_action = QAction("Quitter", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        # Help QAction
        help_action = QAction("Aide", self)
        help_action.triggered.connect(self.help)
        self.help_menu.addAction(help_action)
        self.toolbar_menus()

        #Le robot rouge est sélectionné par défaut
        self.selected_robot = 'R'

        self.draw_robots_and_goal()

    def replay(self):
        """ on remet l'état initial du jeu """
        self.game.set_state(self.initial_game_state)
        self.game.moves_list = []
        self.game.states_list = deque( [self.game.state_start], maxlen = 100)
        self.unprint_moves_list()
        self.number_moves = 0
        self.draw_robots_and_goal()

    def help(self):
        """ Ouvre une fenêtre d'aide"""
        self.help_windows = Help_window()
        self.help_windows.exec_()

    def toolbar_menus(self):
        """ Affiche la barre d'icônes permettant de diriger les robots et de les sélectionner"""

        # Toolbar
        toolbar = QToolBar("Game toolbar")
        self.addToolBar(toolbar)

        # Flèche gauche
        button_West = QAction(QIcon(ICON_PATH + "arrow-180.png"), "West", self)
        button_West.setStatusTip("Aller à gauche")
        button_West.triggered.connect(self.onButtonWestClick)
        button_West.setCheckable(False)
        button_West.setShortcut(QKeySequence("Left"))
        toolbar.addAction(button_West)

        # Flèche droite
        button_East = QAction(QIcon(ICON_PATH + "arrow.png"), "Est", self)
        button_East.setStatusTip("Aller à droite")
        button_East.triggered.connect(self.onButtonEastClick)
        button_East.setCheckable(False)
        button_East.setShortcut(QKeySequence("Right"))
        toolbar.addAction(button_East)

        # Flèche Haut
        button_North = QAction(QIcon(ICON_PATH + "arrow-090.png"), "North", self)
        button_North.setStatusTip("Aller vers le haut")
        button_North.triggered.connect(self.onButtonNorthClick)
        button_North.setCheckable(False)
        button_North.setShortcut(QKeySequence("Up"))
        toolbar.addAction(button_North)

        # Flèche Bas
        button_South = QAction(QIcon(ICON_PATH + "arrow-270.png"), "South", self)
        button_South.setStatusTip("Aller vers le Bas")
        button_South.triggered.connect(self.onButtonSouthClick)
        button_South.setCheckable(False)
        button_South.setShortcut(QKeySequence("Down"))
        toolbar.addAction(button_South)

        # Selection robot actif
        button_Red = QPushButton("&Red")
        button_Red.setIcon(QIcon(ICON_PATH + "icon_R.png"))
        button_Red.setAutoExclusive(True)
        button_Red.setCheckable(True)
        button_Red.setShortcut(QKeySequence("R"))
        button_Red.toggled.connect(self.onButtonRedClick)


        button_Green = QPushButton("&Green")
        button_Green.setIcon(QIcon(ICON_PATH + "icon_G.png"))
        button_Green.setAutoExclusive(True)
        button_Green.setCheckable(True)
        button_Green.setShortcut(QKeySequence("G"))
        button_Green.toggled.connect(self.onButtonGreenClick)


        button_Blue = QPushButton("&Blue")
        button_Blue.setIcon(QIcon(ICON_PATH + "icon_B.png"))
        button_Blue.setAutoExclusive(True)
        button_Blue.setCheckable(True)
        button_Blue.setShortcut(QKeySequence("B"))
        button_Blue.toggled.connect(self.onButtonBlueClick)


        button_Yellow = QPushButton("&Yellow")
        button_Yellow.setIcon(QIcon(ICON_PATH + "icon_Y.png"))
        button_Yellow.setAutoExclusive(True)
        button_Yellow.setCheckable(True)
        button_Yellow.setShortcut(QKeySequence("Y"))
        button_Yellow.toggled.connect(self.onButtonYellowClick)

        # Boutton d'annulation (revient en arrière d'un coup)
        button_undo = QPushButton("&Undo")
        button_undo.setIcon(QIcon(ICON_PATH + "undo.jpg"))
        button_undo.setAutoExclusive(False)
        button_undo.setCheckable(False)
        button_undo.setShortcut(QKeySequence("U"))
        button_undo.clicked.connect(self.onButtonUndoClick)

        # Boutton d'indice : lance le solveur pour donner l'indice du prochain coup à effectuer
        button_tip = QPushButton("&Tip")
        button_tip.setIcon(QIcon(ICON_PATH + "icon_tip.png"))
        button_tip.setAutoExclusive(False)
        button_tip.setCheckable(False)
        button_tip.setShortcut(QKeySequence("T"))
        button_tip.clicked.connect(self.onButtonTipClick)

        # Boutton Solution : lance le solveur pour afficher une liste d'actions à effectuer pour résoudre le jeu
        button_solution = QPushButton("&Solution")
        button_solution.setIcon(QIcon(ICON_PATH + "icon_solution.png"))
        button_solution.setAutoExclusive(False)
        button_solution.setCheckable(False)
        button_solution.setShortcut(QKeySequence("S"))
        button_solution.clicked.connect(self.onButtonSolutionClick)


        toolbar.addWidget(button_Red)
        toolbar.addWidget(button_Green)
        toolbar.addWidget(button_Blue)
        toolbar.addWidget(button_Yellow)
        toolbar.addWidget(button_undo)
        toolbar.addWidget(button_tip)
        toolbar.addWidget(button_solution)

    def open_grid(self):
        """ Ouvre une boîte de dialogue permettant de charger une grille existante sur le disque dur"""

        filename, filter = QFileDialog.getOpenFileName(self , 'selectionner un fichier contenant une grille','./grids','*.json')
        board, = Board.load_from_json(filename)
        self.game.add_board(board)
        self.number_moves = 0
        self.group = Robot_group()
        self.game = Game(self.game.board, self.group, self.game.goal)
        self.unprint_moves_list()
        self.draw_grid()

    def open_game(self):
        """ Ouvre une boîte de dialogue permettant de charger un jeu existant sur le disque dur"""

        filename, filter = QFileDialog.getOpenFileName(self , 'selectionner un fichier contenant un jeu','./games','*.json')
        self.game = Game.load_from_json(filename)
        self.initial_game_state = self.game.get_state()
        self.number_moves = 0
        self.unprint_moves_list()
        self.draw_robots_and_goal()

    def save_grid(self):
        """ Ouvre une boîte de dialogue permettant d'enregistrer la grille affichée sur le disque dur"""

        filename, _ = QFileDialog.getSaveFileName(self, "Save Grid As","","JSON (*.JSON *.json);;" "All files(*.*)", )
        if filename:
            self.game.board.save_as_json(filename)

    def save_game(self):
        """ Ouvre une boîte de dialogue permettant d'enregistrer le jeu actuel sur le disque dur
            Si le joueur entre ou sélectionne un nom de fichier, le eju est sauvegardé dans ce fichier
            """

        filename, _ = QFileDialog.getSaveFileName(self, "Save game As","","JSON (*.JSON *.json);;" "All files(*.*)", )
        if filename:
            self.game.save_to_json(filename)


    def print_moves_list(self):
        """ Affichage de la liste des mouvements effectués dans le label "moves_label" """

        self.moves_label.setText("Mouvements effectués : \n"  + str(self.game.moves_list).replace(', ', '\n'))
        self.moves_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

    def unprint_moves_list(self):
        """ réinitialisation du label "moves_label" pour cacher la liste des mouvements effectués. """
        self.moves_label.setText(" ")
        self.moves_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

    def print_tip(self):
        """ Affichage du conseil généré par le solveur  dans le label "tip_label" """

        self.tip_label.setText("Et si vous essayiez ce mouvement : \n" + str(self.tip) + " ?")
        self.tip_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

    def unprint_tip(self):
        """ réinitialisation du label "tip_label" pour cacher le conseil généré par le solveur. """
        self.tip_label.setText(" ")
        self.tip_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.solution_label.setText(" ")

    def choice_of_grid_menu(self):

        self.grid_choice = QComboBox()
        self.grid_choice.insertItems(0,("Grille 6x6","Grille 8x8","Grille 10x10" ,"Grille 12x12" ,"Grille 14x14", "Grille 16x16","Grille aléatoire 16x16"))
        self.grid_choice.setGeometry(0,0,180,40)
        self.grid_choice.activated.connect(self.choix_grille)

    def choix_grille(self,i) :
        """
        Lors du choix d'une nouvelle grille, le jeu est réinitialisé et redessiné, les robots et l'objectif sont masqués.
        """

        # pour ouvrir les vieux .txt
        # name_grid = './test' + str(i + 1) + '.txt'
        # fd = open(name_grid,'r')
        # A = Board.load_from_json(fd)

        if i == 0:
            A, = Board.load_from_json(GRIDS_PATH + 'grid 6x6.json')
        elif i == 1:
            A, = Board.load_from_json(GRIDS_PATH + 'grid 8x8.json')
        elif i == 2:
            A, = Board.load_from_json(GRIDS_PATH + 'grid 10x10.json')
        elif i == 3:
            A, = Board.load_from_json(GRIDS_PATH + 'grid 12x12.json')
        elif i == 4:
            A, = Board.load_from_json(GRIDS_PATH + 'grid 14x14.json')
        elif i == 5:
            A, = Board.load_from_json(GRIDS_PATH + 'grid 16x16.json')
        else :
            # Pour ouvrir une grille aléatoire classique
            A = Board.new_classic()

        self.game.add_board(A)
        self.number_moves = 0
        self.group = Robot_group()
        self.game = Game(self.game.board, self.group, self.game.goal)
        self.draw_grid()


        # choix du nombre de robots
    def nb_robots_choice_menu(self):
        self.nb_robots_choice = QComboBox()
        self.nb_robots_choice.insertItems(0,("1 robot","2 robots","3 robots" ,"4 robots"))
        self.nb_robots_choice.setGeometry(0,0,40,40)
        self.nb_robots_choice.activated.connect(self.choix_nb_robots)

    def choix_nb_robots(self,i) :
        """
        Les robots et l'objectif sont placés aléatoirement. L'extension
        """

        self.group = Robot_group()
        self.game = Game(self.game.board, self.group, self.game.goal)

        self.nb_robots = i + 1

        robots_pos = [0] * self.nb_robots
        robots_list = [0] * self.nb_robots
        robots_colors = [i for i in RColors]
        if self.placement_aleatoire:

            for i in range(self.nb_robots):
                x = randint(0, self.game.board.width - 1)
                y = randint(0, self.game.board.height - 1)
                while ((x, y) in robots_pos):
                    x = randint(0, self.game.board.width - 1)
                    y = randint(0, self.game.board.height - 1)
                robots_pos[i] = (x,y)
                robots_list[i] = Robot(self.game.robots, robots_colors[i], (x, y))

            x = randint(0, self.game.board.width - 1)
            y = randint(0, self.game.board.height - 1)
            goal = Goal(RColors(randint(1, self.nb_robots )), (x, y))
            self.game = Game(self.game.board, self.group, self.game.goal)
            self.game.add_goal(goal)
            self.initial_game_state = self.game.get_state()
            self.draw_robots_and_goal()

        else:
            fp = open(GAMES_PATH + DEFAULT_GAME,'r')
            self.game = Game.load_from_json(fp)
            fp.close()

    def draw_grid(self):
        """
        Dessine la grille de jeu en juxtaposant les images contenant chaque case. Chaque image est redimensionnée et ajustée à la taille de la grille.
        """
        painter = QPainter(self.label.pixmap())
        names=["Empty","N","E","EN","S","NS","ES","ENS","W","NW","EW","ENW","SW","NSW","ESW","ENSW"]
        images = [QPixmap(IMAGES_PATH + name+".bmp", format="bmp")  for name in names]

        for x in range(0, self.game.board.width):
            for y in range(0, self.game.board.height):
                painter.drawPixmap(QPoint(self.DIMENSION/ self.game.board.height * y ,self.DIMENSION / self.game.board.width * x) ,
                images[int(str(self.game.board.grid[x][y]))].scaled(self.DIMENSION / self.game.board.width, self.DIMENSION/ self.game.board.height))

        self.update()
        painter.end()

    def draw_robots_and_goal(self):
        self.draw_grid()

        painter = QPainter(self.label.pixmap())

        goal_img_name = ICON_PATH + "/goal_"+ str(self.game.goal.color) +".png"
        painter.drawPixmap(QPoint(self.DIMENSION/ self.game.board.height * self.game.goal.position[1] , self.DIMENSION / self.game.board.width * self.game.goal.position[0]) , QPixmap(goal_img_name, format="png").scaled(self.DIMENSION / self.game.board.width * 0.9, self.DIMENSION/ self.game.board.height * 0.9))

        images = [QPixmap(ICON_PATH + "robot_"+ str(color)+".png", format="png")  for color in self.game.color_keys]

        for i, robot in enumerate(self.game.robots):

            painter.drawPixmap(QPoint(self.DIMENSION/ self.game.board.height * self.game.robots[robot].position[1] , self.DIMENSION / self.game.board.width * self.game.robots[robot].position[0]) , images[i].scaled(self.DIMENSION / self.game.board.width * 0.8, self.DIMENSION/ self.game.board.height))

        self.update()
        painter.end()

    def onButtonEastClick(self, s):
        self.game.do_action(self.selected_robot + 'E')

        self.draw_robots_and_goal()
        self.number_moves  += 1
        self.print_moves_list()
        self.unprint_tip()
        if self.game.is_won():
            self.game_is_won()

    def onButtonWestClick(self, s):
        self.game.do_action(self.selected_robot + 'W')
        self.draw_robots_and_goal()
        self.number_moves  += 1
        self.print_moves_list()
        self.unprint_tip()
        if self.game.is_won():
            self.game_is_won()

    def onButtonNorthClick(self, s):
        self.game.do_action(self.selected_robot + 'N')
        self.draw_robots_and_goal()
        self.number_moves  += 1
        self.print_moves_list()
        self.unprint_tip()
        if self.game.is_won():
            self.game_is_won()

    def onButtonSouthClick(self, s):
        self.game.do_action(self.selected_robot + 'S')
        self.draw_robots_and_goal()
        self.number_moves  += 1
        self.print_moves_list()
        self.unprint_tip()
        if self.game.is_won():
            self.game_is_won()

    def placer_aleatoirement(self):
        """ inverse la sélection de la checkBox """
        self.placement_aleatoire = not(self.placement_aleatoire)

    def onButtonRedClick(self, s):
        if s:
            self.selected_robot = 'R'

    def onButtonGreenClick(self, s):
        if s:
            self.selected_robot = 'G'

    def onButtonBlueClick(self, s):
        if s:
            self.selected_robot = 'B'

    def onButtonYellowClick(self, s):
        if s:
            self.selected_robot = 'Y'

    def onButtonUndoClick(self, s):
        """ Annule le dernier coup effectué """
        if self.number_moves != 0:
            self.game.undo()
            self.number_moves  -= 1
            self.print_moves_list()
            self.unprint_tip()
            self.draw_robots_and_goal()


    def solve(self):
        """tip_game contient une copie du jeu courant, pour l'utiliser par le solveur"""

        self.game.save_to_json('tip_game.json')
        self.tip_game = Game.load_from_json('tip_game.json')
        return(solveur(self.tip_game).find_solution())

    def onButtonTipClick(self, s):
        """ La solution renvoyée par le solveur est de la forme (True/False, liste d'actions à effectuer).
        On récupère ici la première action."""
        self.tip = self.solve()[1][0]
        self.print_tip()

    def onButtonSolutionClick(self, s):
        self.solution = self.solve()[1]
        self.solution_label.setText("Pour gagner, vous auriez pu effectuer cette suite de mouvements : \n" + str(self.solution) + ".")
        self.solution_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

    def game_is_won(self):
        """ Fonction lancée quand l'objectif est atteint. On génère une fonction exit_windows dont le code de retour 1, 2 ou 3 valide le choix :
        1 : replay : on remet l'état initial du jeu
        2 : new game : on choisit une grille aleatoire
        3 : exit : on quitte le jeu.
        """
        self.exit_windows = Exit_window(self.number_moves)

        self.exit_windows.exec_()

        if self.exit_windows.retStatus == 1:     #replay : on remet l'état initial du jeu
            self.replay()

        elif self.exit_windows.retStatus == 2:   #new game : on choisit une grille aleatoire
            self.choix_grille(1)
            self.choix_nb_robots(3)
            self.unprint_moves_list()

        elif self.exit_windows.retStatus == 3:  #exit : on quitte le jeu
            exit()

class Help_window(QDialog):
    def __init__(self):
        super(Help_window, self).__init__()
        self.setWindowTitle("Aide")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.resize(650, 400)
        help_msg = QPlainTextEdit()

        text = "<br /><h1>A propos du jeu</h1>"
        text += "<p><a href='Ricochet Robots'></a>Ricochet Robots est un jeu de société créé par Alex Randolph en 1999</p>"
        text += "<p>Le jeu est composé d'un plateau, de tuiles représentant chacune une des cases du plateau, et de pions appelés « robots »."
        text += "La partie est décomposée en tours de jeu, un tour consistant à déplacer les robots sur un plateau afin d'en amener un sur l'une des cases du plateau.</p>"
        text += "<p>Les robots se déplacent en ligne droite et avancent toujours jusqu'au premier mur qu'ils rencontrent.</p>"
        text += "<br /><h1>Utilisation du jeu</h1>"
        text += "<p>Pour débuter un nouveau jeu, vous pouvez : "
        text += "<ul><li>jouer avec le plateau par défaut (très simple)</li>"
        text += "<li>sélectionner un plateau existant ou générer un plateau aléatoire, réalisé comme dans le jeu physique :"
        text += " on mélange 4 quarts de plateaux choisis au hasard</li></ul>"
        text += "<br /><p>Pour sélectionner un robot, cliquez sur le bouton ou sur l'initiale de sa couleur (en anglais).</p>"
        text += "<br /><p>pour déplacer un robot, utilisez les flèches du clavier ou les icônes de la fenêtre.</p>"
        text += "<br /><p>Vous pouvez annuler la dernière action effectuée grâce au bouton Undo, ou obtenir un conseil grâce au bouton Tip.</p>"
        text += "<br /><br /><br />"
        text += "<p>Réalisé par Martin Canals, Théo Giani et François Aubin dans le cadre de l'UE projet Math-Info du DU CCIE</p>"
        help_msg.appendHtml(text)
        help_msg.setReadOnly(True)
        help_msg.setUndoRedoEnabled(False)
        text = ""
        help_msg.appendHtml(text)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(help_msg)
        self.setLayout(mainLayout)


class Exit_window(QDialog):
    """ Fenêtre apparaissant lorsqu'on a gagné. On génère une fonction exit_windows dont le code de retour 1, 2 ou 3 valide le choix :
    1 : replay : on remet l'état initial du jeu
    2 : new game : on choisit une grille aleatoire
    3 : exit : on quitte le jeu.
    """

    def __init__(self, number_moves):
        super(Exit_window, self).__init__()
        self.setWindowTitle("Bravo !")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.end_msg = QLabel("Vous avez gagné en " + str(number_moves) + " coups ! Que voulez-vous faire ?")
        mainLayout = QVBoxLayout()

        replay_button = QPushButton("Rejouer cette partie")
        replay_button.clicked.connect(self.replay)
        new_game_button = QPushButton("Un nouveau jeu")
        new_game_button.clicked.connect(self.new_game)
        exit_button = QPushButton("Quitter")
        exit_button.clicked.connect(self.exit_game)

        buttonBox = QDialogButtonBox(Qt.Horizontal)
        buttonBox.addButton(replay_button, QDialogButtonBox.ActionRole)
        buttonBox.addButton(new_game_button, QDialogButtonBox.ActionRole)
        buttonBox.addButton(exit_button, QDialogButtonBox.ActionRole)

        mainLayout.addWidget(self.end_msg)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setGeometry(	250, 250, 0, 50)


    def replay(self):
        self.retStatus = 1
        self.close()

    def new_game(self):
        self.retStatus = 2

        self.close()

    def exit_game(self):
        self.retStatus = 3
        self.close()



app = QApplication(sys.argv)
group = Robot_group()
game = Game.load_from_json(GAMES_PATH + DEFAULT_GAME)
fen = MainWindow(game)
fen.show()
app.exec_()
