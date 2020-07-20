# -*- coding : utf-8 -*-

""" Projet Maths Info pour le DU CCIE et la L3 Maths-Info
Chef de projet : CANALS Martin L3
Développeurs : AUBIN François DU CCIE, GIANI Théo L3

"""

import sys
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow , QGridLayout, QLabel, QPushButton, QMainWindow, QAction, QToolBar, QVBoxLayout, QComboBox, QHBoxLayout, QCheckBox, QRadioButton, QDialog, QMessageBox
from PySide2.QtGui import QKeySequence, QPainter, QColor, QBrush, QPaintEvent, QFont, QPen, QIcon, QImage, QPixmap
from PySide2.QtCore import Qt, QPoint
from robot import*
from random import *


class MainWindow(QMainWindow):
    DIMENSION = 600
    placement_aleatoire = True
    nb_robots = 0

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.setWindowTitle("Robot Ricochet")
        self.resize(self.DIMENSION, self.DIMENSION + 100)
        self.label = QLabel()
        canvas = QPixmap(self.DIMENSION , self.DIMENSION)
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)
        #self.setCentralWidget(self.label)

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout2 = QHBoxLayout()

        # Choix de la grille
        grid_choice = QComboBox()
        grid_choice.insertItems(0,("Grille 1 ","Grille 2","Grille 3" ,"Grille 4"))
        grid_choice.setGeometry(0,0,180,40)
        grid_choice.activated.connect(self.choix_grille)


        # choix du nombre de robots
        nb_robots_choice = QComboBox()
        nb_robots_choice.insertItems(0,("1 robot","2 robots","3 robots" ,"4 robots"))
        nb_robots_choice.setGeometry(0,0,40,40)
        nb_robots_choice.activated.connect(self.choix_nb_robots)

        # CheckBox placement aléatoire
        widget3 = QCheckBox("Placement aléatoire des robots et de l'objectif")
        widget3.setCheckState(Qt.Checked)
        widget3.stateChanged.connect(self.placer_aleatoirement)


        # layout2 contient les 3 widgets horizontaux de choix de grille, robots et aléa
        layout2.addWidget(grid_choice)
        layout2.addWidget(nb_robots_choice)
        layout2.addWidget(widget3)
        layout2.setContentsMargins(0,0,0,0)
        layout2.setSpacing(0)
        widget2 = QWidget()
        widget2.setLayout(layout2)


        layout.addWidget(widget2)
        layout.addWidget(self.label)
        widget = QWidget()
        widget.setLayout(layout)
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

        # Toolbar
        toolbar = QToolBar("Game toolbar")
        self.addToolBar(toolbar)

        # Flèche gauche
        button_West = QAction(QIcon("./version2/icons/arrow-180.png"), "West", self)
        button_West.setStatusTip("Aller à gauche")
        button_West.triggered.connect(self.onButtonWestClick)
        button_West.setCheckable(False)
        button_West.setShortcut(QKeySequence("Left"))
        toolbar.addAction(button_West)

        # Flèche droite
        button_East = QAction(QIcon("./version2/icons/arrow.png"), "Est", self)
        button_East.setStatusTip("Aller à droite")
        button_East.triggered.connect(self.onButtonEastClick)
        button_East.setCheckable(False)
        button_East.setShortcut(QKeySequence("Right"))
        toolbar.addAction(button_East)

        # Flèche Haut
        button_North = QAction(QIcon("./version2/icons/arrow-090.png"), "North", self)
        button_North.setStatusTip("Aller vers le haut")
        button_North.triggered.connect(self.onButtonNorthClick)
        button_North.setCheckable(False)
        button_North.setShortcut(QKeySequence("Up"))
        toolbar.addAction(button_North)

        # Flèche Bas
        button_South = QAction(QIcon("./version2/icons/arrow-270.png"), "South", self)
        button_South.setStatusTip("Aller vers le Bas")
        button_South.triggered.connect(self.onButtonSouthClick)
        button_South.setCheckable(False)
        button_South.setShortcut(QKeySequence("Down"))
        toolbar.addAction(button_South)

        # Selection robot actif
        button_Red = QPushButton("&Red")
        button_Red.setIcon(QIcon("./version2/icons/icon_R.png"))
        button_Red.setAutoExclusive(True)
        button_Red.setCheckable(True)
        button_Red.setShortcut(QKeySequence("R"))
        button_Red.toggled.connect(self.onButtonRedClick)


        button_Green = QPushButton("&Green")
        button_Green.setIcon(QIcon("./version2/icons/icon_G.png"))
        button_Green.setAutoExclusive(True)
        button_Green.setCheckable(True)
        button_Green.setShortcut(QKeySequence("G"))
        button_Green.toggled.connect(self.onButtonGreenClick)


        button_Blue = QPushButton("&Blue")
        button_Blue.setIcon(QIcon("./version2/icons/icon_B.png"))
        button_Blue.setAutoExclusive(True)
        button_Blue.setCheckable(True)
        button_Blue.setShortcut(QKeySequence("B"))
        button_Blue.toggled.connect(self.onButtonBlueClick)


        button_Yellow = QPushButton("&Yellow")
        button_Yellow.setIcon(QIcon("./version2/icons/icon_Y.png"))
        button_Yellow.setAutoExclusive(True)
        button_Yellow.setCheckable(True)
        button_Yellow.setShortcut(QKeySequence("Y"))
        button_Yellow.toggled.connect(self.onButtonYellowClick)


        toolbar.addWidget(button_Red)
        toolbar.addWidget(button_Green)
        toolbar.addWidget(button_Blue)
        toolbar.addWidget(button_Yellow)


        #Le robot rouge est sélectionné par défaut
        self.selected_robot = 'R'

    def choix_grille(self,i) :
        name_grid = './version2/test' + str(i + 1) + '.txt'
        fd = open(name_grid,'r')
        A = Board.load_from_file(fd)
        self.game.add_board(A)
        self.number_moves = 0
        group = Robot_group()
        self.game = Game(self.game.board, group, self.game.goal)
        self.draw_grid()

    def choix_nb_robots(self,i) :
        group = Robot_group()
        self.game = Game(self.game.board, group, self.game.goal)

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
                self.robots_list[i] = Robot(self.game.group, self.robots_colors[i], (x, y))
            # self.game.add_robots(self.robots_list)  inutile????

            x = randint(0, self.game.board.width - 1)
            y = randint(0, self.game.board.height - 1)
            goal = Goal(RColors(randint(1, self.nb_robots )), (x, y))
            self.game.add_goal(goal)
            self.draw_robots_and_goal()

    def draw_grid(self):
        group = Robot_group()
        painter = QPainter(self.label.pixmap())
        names=["Empty","N","E","EN","S","NS","ES","ENS","W","NW","EW","ENW","SW","NSW","ESW","ENSW"]
        images = [QPixmap("./version2/images/"+name+".bmp", format="bmp")  for name in names]

        for x in range(0, self.game.board.width):
            for y in range(0, self.game.board.height):
                painter.drawPixmap(QPoint(self.DIMENSION/ self.game.board.height * y ,self.DIMENSION / self.game.board.width * x) ,
                images[int(str(self.game.board.grid[x][y]))].scaled(self.DIMENSION / self.game.board.width, self.DIMENSION/ self.game.board.height))

        self.update()
        painter.end()

    def draw_robots_and_goal(self):
        self.draw_grid()

        painter = QPainter(self.label.pixmap())

        goal_img_name = "./version2/icons/goal_"+ game.color_names[self.game.goal.color] +".png"
        painter.drawPixmap(QPoint(self.DIMENSION/ self.game.board.height * self.game.goal.position[1] , self.DIMENSION / self.game.board.width * self.game.goal.position[0]) , QPixmap(goal_img_name, format="png").scaled(self.DIMENSION / self.game.board.width * 0.9, self.DIMENSION/ self.game.board.height * 0.9))

        images = [QPixmap("./version2/icons/robot_"+ game.color_names[color] +".png", format="png")  for color in self.robots_colors]

        for i, robot in enumerate(self.game.robots):

            painter.drawPixmap(QPoint(self.DIMENSION/ self.game.board.height * self.game.robots[robot].position[1] , self.DIMENSION / self.game.board.width * self.game.robots[robot].position[0]) , images[i].scaled(self.DIMENSION / self.game.board.width * 0.8, self.DIMENSION/ self.game.board.height))

        self.update()
        painter.end()

    def onButtonEastClick(self, s):
        self.game.do_action(self.selected_robot + 'E')
        self.draw_robots_and_goal()
        self.number_moves  += 1
        if self.game.is_won():
            self.game_is_won()

    def onButtonWestClick(self, s):
        self.game.do_action(self.selected_robot + 'W')
        self.draw_robots_and_goal()
        self.number_moves  += 1
        if self.game.is_won():
            self.game_is_won()

    def onButtonNorthClick(self, s):
        self.game.do_action(self.selected_robot + 'N')
        self.draw_robots_and_goal()
        self.number_moves  += 1
        if self.game.is_won():
            self.game_is_won()

    def onButtonSouthClick(self, s):
        self.game.do_action(self.selected_robot + 'S')
        self.draw_robots_and_goal()
        self.number_moves  += 1
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

    def game_is_won(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Bravo!")
        dlg.setText("Vous avez gagné en " + str(self.number_moves) + " coups ! Voulez-vous rejouer ?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = dlg.exec_()
        dlg.setIcon(QMessageBox.Question)
        if button == QMessageBox.Yes:
            self.draw_grid()
        else:
            exit()






app = QApplication(sys.argv)
group = Robot_group()
game = Game(None, group, None)
fen = MainWindow(game)
fen.show()
app.exec_()
