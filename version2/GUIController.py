# -*- coding : utf-8 -*-

""" Projet Maths Info pour le DU CCIE et la L3 Maths-Info
Chef de projet : CANALS Martin L3
Développeurs : AUBIN François DU CCIE, GIANI Théo L3

"""

import sys
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow , QGridLayout, QLabel, QPushButton, QMainWindow, QAction, QToolBar, QVBoxLayout, QComboBox, QHBoxLayout, QCheckBox, QRadioButton, QDialog, QMessageBox, QDialogButtonBox
from PySide2.QtGui import QKeySequence, QPainter, QColor, QBrush, QPaintEvent, QFont, QPen, QIcon, QImage, QPixmap
from PySide2.QtCore import Qt, QPoint
from directions import Direction, NORTH, SOUTH, EAST, WEST
from rcolors import RColors
from robot import Robot, Robot_group
from board import Board
from game import Game
from random import *
from solveur import solveur

ICON_PATH = "./icons/"
IMAGES_PATH = "./images/"
GAMES_PATH = './games/'
DEFAULT_GAME = "game1.json"

class MainWindow(QMainWindow):
    DIMENSION = 560
    placement_aleatoire = True
    nb_robots = 0

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.initial_game_state = self.game.get_state()
        print(self.game.get_state())
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
        layout2.addWidget(widget3)
        layout2.setContentsMargins(0,0,0,0)
        layout2.setSpacing(0)
        widget2 = QWidget()
        widget2.setLayout(layout2)


        layout.addWidget(widget2)
        layout.addWidget(self.label)

        layout0.addLayout(layout)



        # liste des mouvement effectués et indice :
        layout3 = QVBoxLayout()
        layout3.setContentsMargins(0,0,0,0)
        layout3.setSpacing(0)

        self.moves_label = QLabel()
        self.print_moves_list()

        self.tip_label = QLabel()


        layout3.addWidget(self.moves_label)
        layout3.addWidget(self.tip_label)


        layout0.addLayout(layout3)
        widget = QWidget()
        widget.setLayout(layout0)
        self.setCentralWidget(widget)


        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.help_menu = self.menu.addMenu("Aide et instructions")    # A faire
        self.size_fenetre = self.geometry()

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        # Play QAction
        play_action = QAction("Jouer !", self)
        self.number_moves = 0
        play_action.triggered.connect(self.draw_grid)
        self.file_menu.addAction(play_action)


        self.toolbar_menus()

        #Le robot rouge est sélectionné par défaut
        self.selected_robot = 'R'

        #self.choix_nb_robots(3)
        self.draw_robots_and_goal()


    def toolbar_menus(self):
        """ Affiche la barre d'icônes permettant de diriger les robots et de les sélectionner
        """
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

        toolbar.addWidget(button_Red)
        toolbar.addWidget(button_Green)
        toolbar.addWidget(button_Blue)
        toolbar.addWidget(button_Yellow)
        toolbar.addWidget(button_undo)
        toolbar.addWidget(button_tip)


    def print_moves_list(self):
        self.moves_label.setText("Mouvements effectués : \n" + str(self.game.moves_list).replace(', ', '\n'))
        self.moves_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

    def print_tip(self):
        self.tip_label.setText("Et si vous essayiez ce mouvement : \n" + str(self.tip) + " ?")
        self.tip_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

    def unprint_tip(self):
        self.tip_label.setText(" ")
        self.tip_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

    def choice_of_grid_menu(self):
        self.grid_choice = QComboBox()
        self.grid_choice.insertItems(0,("Grille aléatoire ","Grille 1","Grille 2" ,"Grille 3"))
        self.grid_choice.setGeometry(0,0,180,40)
        self.grid_choice.activated.connect(self.choix_grille)

    def choix_grille(self,i) :
        # pour ouvrir les vieux .txt
        #name_grid = './test' + str(i + 1) + '.txt'
        #fd = open(name_grid,'r')
        # A = Board.load_from_json(fd)

        # pour ouvrir les nouveaux .json


        """name_grid = './test' + str(i + 1) + '.json'
        A, = Board.load_from_json(name_grid)"""

        #Pour ouvrir une grille aléatoire classique
        A = Board.new_classic()

        self.game.add_board(A)
        print(self.game.get_state())
        self.number_moves = 0
        self.group = Robot_group()
        print(self.game.get_state())
        self.game = Game(self.game.board, self.group, self.game.goal)
        print(self.game.get_state())
        self.draw_grid()


        # choix du nombre de robots
    def nb_robots_choice_menu(self):
        self.nb_robots_choice = QComboBox()
        self.nb_robots_choice.insertItems(0,("1 robot","2 robots","3 robots" ,"4 robots"))
        self.nb_robots_choice.setGeometry(0,0,40,40)
        self.nb_robots_choice.activated.connect(self.choix_nb_robots)

    def choix_nb_robots(self,i) :
        self.group = Robot_group()
        self.game = Game(self.game.board, self.group, self.game.goal)
        print(self.game.get_state())

        self.nb_robots = i + 1

        self.robots_pos = [0] * self.nb_robots
        self.robots_list = [0] * self.nb_robots
        self.robots_colors = [i for i in RColors]
        if self.placement_aleatoire:

            for i in range(self.nb_robots):
                x = randint(0, self.game.board.width - 1)
                y = randint(0, self.game.board.height - 1)
                while ((x, y) in self.robots_pos):
                    x = randint(0, self.game.board.width - 1)
                    y = randint(0, self.game.board.height - 1)
                self.robots_pos[i] = (x,y)
                self.robots_list[i] = Robot(self.game.robots, self.robots_colors[i], (x, y))

            x = randint(0, self.game.board.width - 1)
            y = randint(0, self.game.board.height - 1)
            goal = Goal(RColors(randint(1, self.nb_robots )), (x, y))
            self.game = Game(self.game.board, self.group, self.game.goal)
            self.game.add_goal(goal)
            self.initial_game_state = self.game.get_state()
            print(self.game.get_state())
            self.draw_robots_and_goal()

        else:
            fp = open(GAMES_PATH + DEFAULT_GAME,'r')
            self.game = Game.load_from_json(fp)
            fp.close()

    def draw_grid(self):

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

        goal_img_name = ICON_PATH + "/goal_"+ game.color_names[self.game.goal.color] +".png"
        painter.drawPixmap(QPoint(self.DIMENSION/ self.game.board.height * self.game.goal.position[1] , self.DIMENSION / self.game.board.width * self.game.goal.position[0]) , QPixmap(goal_img_name, format="png").scaled(self.DIMENSION / self.game.board.width * 0.9, self.DIMENSION/ self.game.board.height * 0.9))

        #images = [QPixmap(ICON_PATH + "robot_"+ game.color_names[color] +".png", format="png")  for color in self.robots_colors]
        images = [QPixmap(ICON_PATH + "robot_"+ game.color_names[color] +".png", format="png")  for color in self.game.color_keys]

        for i, robot in enumerate(self.game.robots):

            painter.drawPixmap(QPoint(self.DIMENSION/ self.game.board.height * self.game.robots[robot].position[1] , self.DIMENSION / self.game.board.width * self.game.robots[robot].position[0]) , images[i].scaled(self.DIMENSION / self.game.board.width * 0.8, self.DIMENSION/ self.game.board.height))

        self.update()
        painter.end()

    def onButtonEastClick(self, s):
        self.game.do_action(self.selected_robot + 'E')
        print(self.game.get_state())

        self.draw_robots_and_goal()
        self.number_moves  += 1
        self.print_moves_list()
        self.unprint_tip()
        if self.game.is_won():
            self.game_is_won()

    def onButtonWestClick(self, s):
        self.game.do_action(self.selected_robot + 'W')
        print(self.game.get_state())
        self.draw_robots_and_goal()
        self.number_moves  += 1
        self.print_moves_list()
        self.unprint_tip()
        if self.game.is_won():
            self.game_is_won()

    def onButtonNorthClick(self, s):
        self.game.do_action(self.selected_robot + 'N')
        print(self.game.get_state())
        self.draw_robots_and_goal()
        self.number_moves  += 1
        self.print_moves_list()
        self.unprint_tip()
        if self.game.is_won():
            self.game_is_won()

    def onButtonSouthClick(self, s):
        self.game.do_action(self.selected_robot + 'S')
        print(self.game.get_state())
        self.draw_robots_and_goal()
        self.number_moves  += 1
        self.print_moves_list()
        self.unprint_tip()
        if self.game.is_won():
            self.game_is_won()

    def placer_aleatoirement(self):   # inverse la sélection de la checkBox
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

        if self.number_moves != 0:
            self.game.undo()
            self.number_moves  -= 1
            self.print_moves_list()
            self.unprint_tip()
            self.draw_robots_and_goal()
        print("number_moves = " + str(self.number_moves))
        print(self.game.get_state())


    def onButtonTipClick(self, s):
        fp = open('tip_game.json', 'w')     #tip_game contient le jeu courant, pour l'utiliser par le solveur
        self.game.save_2_json(fp)
        fp.close()
        fp = open('tip_game.json', 'r')
        self.tip_game = Game.load_from_json(fp)
        fp.close()
        solution = solveur(self.tip_game).find_solution()
        self.tip = solution[1][0]
        self.print_tip()

    def game_is_won(self):
        self.exit_windows = Exit_window()
        #self.exit_windows.show()
        self.exit_windows.exec_()

        if self.exit_windows.retStatus == 1:     #replay : on remet l'état initial du jeu
            print(self.game.get_state())
            self.game.set_state(self.initial_game_state)
            print(self.game.get_state())
            self.draw_robots_and_goal()

        elif self.exit_windows.retStatus == 2:   #new game : on choisit une grille aleatoire
            self.choix_grille(1)
            self.choix_nb_robots(3)
            #self.draw_robots_and_goal()
        elif self.exit_windows.retStatus == 3:  #exit : on quitte le jeu
            exit()

class Exit_window(QDialog):
    #Fenêtre apparaissant lorsqu'on a gagné

    def __init__(self):
        super(Exit_window, self).__init__()
        self.setWindowTitle("Bravo !")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.end_msg = QLabel("Vous avez gagné en  coups ! Que voulez-vous faire ?")  #" + str(main_game.number_moves) + "
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
        # define window		xLoc,yLoc,xDim,yDim
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
fp = open(GAMES_PATH + DEFAULT_GAME,'r')
game = Game.load_from_json(fp)
fp.close()
#game = Game(None, group, None)
fen = MainWindow(game)
fen.show()
app.exec_()

"""penser à afficher la liste des actions déjà faites

charger un game par défaut depuis un json : fait
générer une grille aléatoire : fait
régler le problème des robots qui apparaissent au centre de la classic grid
placer les robots (de manière aléatoire ou pas)
jouer inclut déplacer un robot et annuler une action, recommencer la même partie

dans le rapport, rajouter les recherches sur les réseaux de neurones, le qlearning( sur une grille avec un point de départ)

bouton undo : fait mais ne fonctionne pas : le get_state() renvoie du vide : pas la bonne instance de game??
corrigé : il faut créer le game avec un group plein, sinon quand on crée un nouveau robot,
il ne met pas à jour game.color_keys.

reste un problème : au 1er clic sur undo, il  supprime juste l'état courant mais ne revient pas en arrière. : RESOLU

fenêtre finale : bouton replay ne fonctionne pas : il redessine avant qu'on ait cliqué et sans fermer : RESOLU

"""
