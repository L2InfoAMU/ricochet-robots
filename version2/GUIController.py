# -*- coding : utf-8 -*-

""" Projet Maths Info pour le DU CCIE et la L3 Maths-Info
Chef de projet : CANALS Martin L3
Développeurs : AUBIN François DU CCIE, GIANI Théo L3

"""

import sys
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow , QGridLayout, QLabel, QPushButton, QMainWindow, QAction, QToolBar, QVBoxLayout, QComboBox, QHBoxLayout, QCheckBox, QRadioButton, QDialog, QMessageBox, QDialogButtonBox, QPlainTextEdit, QFileDialog
from PySide2.QtGui import QKeySequence, QPainter, QColor, QBrush, QPaintEvent, QFont, QPen, QIcon, QImage, QPixmap
from PySide2.QtCore import Qt, QPoint
from directions import Direction, NORTH, SOUTH, EAST, WEST
from rcolors import RColors
from robot import Robot, Robot_group
from board import Board
from game import Game
from goal import Goal
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
        self.number_moves = 0
        play_action.triggered.connect(self.draw_grid)
        self.file_menu.addAction(play_action)

        # Open QAction
        open_action = QAction("Ouvrir une grille", self)
        open_action.setShortcut('Ctrl+O')
        self.number_moves = 0
        open_action.triggered.connect(self.open_grid)
        self.file_menu.addAction(open_action)

        # Save QAction
        save_action = QAction("Enregistrer cette grille", self)
        save_action.triggered.connect(self.save_grid)
        self.file_menu.addAction(save_action)

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

        #self.choix_nb_robots(3)
        self.draw_robots_and_goal()

    def help(self):
        self.help_windows = Help_window()
        #self.exit_windows.show()
        self.help_windows.exec_()

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

    def open_grid(self) :
        filename, filter = QFileDialog.getOpenFileName(self , 'selectionner un fichier contenant une grille','./grids','*.json')
        print(filename)
        board, = Board.load_from_json(filename)
        self.game.add_board(board)
        self.number_moves = 0
        self.group = Robot_group()
        self.game = Game(self.game.board, self.group, self.game.goal)
        self.draw_grid()

    def save_grid(self) :
        pass

    def print_moves_list(self):
        self.moves_label.setText("Mouvements effectués : \n"  + str(self.game.moves_list).replace(', ', '\n'))
        self.moves_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

    def print_tip(self):
        self.tip_label.setText("Et si vous essayiez ce mouvement : \n" + str(self.tip) + " ?")
        self.tip_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

    def unprint_tip(self):
        self.tip_label.setText(" ")
        self.tip_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.solution_label.setText(" ")

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
        self.group = Robot_group()
        self.game = Game(self.game.board, self.group, self.game.goal)

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

        goal_img_name = ICON_PATH + "/goal_"+ str(self.game.goal.color) +".png"
        painter.drawPixmap(QPoint(self.DIMENSION/ self.game.board.height * self.game.goal.position[1] , self.DIMENSION / self.game.board.width * self.game.goal.position[0]) , QPixmap(goal_img_name, format="png").scaled(self.DIMENSION / self.game.board.width * 0.9, self.DIMENSION/ self.game.board.height * 0.9))

        #images = [QPixmap(ICON_PATH + "robot_"+ game.color_names[color] +".png", format="png")  for color in self.robots_colors]
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


    def solve(self):
        #tip_game contient le jeu courant, pour l'utiliser par le solveur

        self.game.save_to_json('tip_game.json')
        self.tip_game = Game.load_from_json('tip_game.json')
        return(solveur(self.tip_game).find_solution())

    def onButtonTipClick(self, s):

        self.tip = self.solve()[1][0]
        self.print_tip()

    def onButtonSolutionClick(self, s):
        self.solution = self.solve()[1]
        self.solution_label.setText("Pour gagner, vous auriez pu effectuer cette suite de mouvements : \n" + str(self.solution) + ".")
        self.solution_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

    def game_is_won(self):
        self.exit_windows = Exit_window()
        #self.exit_windows.show()
        self.exit_windows.exec_()

        if self.exit_windows.retStatus == 1:     #replay : on remet l'état initial du jeu
            self.game.set_state(self.initial_game_state)
            self.draw_robots_and_goal()

        elif self.exit_windows.retStatus == 2:   #new game : on choisit une grille aleatoire
            self.choix_grille(1)
            self.choix_nb_robots(3)
            #self.draw_robots_and_goal()
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

game = Game.load_from_json(GAMES_PATH + DEFAULT_GAME)

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

bouton solution ajouté.
"""
