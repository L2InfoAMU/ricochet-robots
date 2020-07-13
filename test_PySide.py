import sys
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QPushButton, QMainWindow, QAction
from PySide2.QtGui import QKeySequence, QPainter, QColor, QBrush, QPaintEvent, QFont, QPen, QIcon, QImage, QPixmap
from PySide2.QtCore import Qt
from random import *
from ClassicBoard import *
from objectif import Objectif
from RRCONST import *

import game as g

test_grid = [[ 9,  1, 1, 1,  3, 9, 1, 1],
              [  8,   0, 6, 8, 0,  0, 0, 0],
              [  8,  0, 1, 0, 0,  0, 0, 0],
              [  10, 12, 0, 0, 0,  0, 4, 0],
              [ 12, 1, 0, 0, 0,  2, 9, 0],
              [ 9, 0, 0, 0, 0,  4, 0, 0],
              [ 8, 0, 0, 0, 0, 3, 8, 4],
              [  8, 0, 0, 6, 8, 0, 2, 9]]

test_board = ClassicBoard(test_grid, Objectif(RED,(1,1)))

RED_ROBOT = QImage("robot rouge.png")

class MaFenetre(QMainWindow):
    GAMEZONE_SIZE = 400

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robot Ricochet")
        self.resize(800, 600)
        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.options_menu = self.menu.addMenu("Options")
        self.size_fenetre = self.geometry()
        GAMEZONE_SIZE = min(self.size_fenetre.width(), self.size_fenetre.height()) / 2

        # New Qaction
        new_action = QAction("New", self) # à compléter
        new_action.setShortcut(QKeySequence.New)

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        self.file_menu.addAction(new_action)
        self.file_menu.addAction(exit_action)

        # Options QAction
        options_action1 = QAction("Une grille classique au hasard", self)
        self.options_menu.addAction(options_action1)
        options_action1.triggered.connect(self.level_choice())  # à modifier/compléter


        options_action2 = QAction("Une grille aléatoire", self)
        self.options_menu.addAction(options_action2)
        #à compléter

        options_action3 = QAction("choix d'une grille enregistrée", self)
        self.options_menu.addAction(options_action3)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Sur un jeu d'Alex Randolph")

        layout = QGridLayout()
        self.label = QLabel("Robot Ricochet", self)
        self.button = QPushButton("Cliquez ici pour commencer", self)
        # self.button.setFont(QFont("Verdana", 25))
        widget2 = GameDesign(test_grid)
        widget2.resize(self.GAMEZONE_SIZE, self.GAMEZONE_SIZE)

        layout.addWidget(self.label, 0, 0, 1, 1)
        layout.addWidget(widget2, 1, 1, 4, 4)
        layout.addWidget(self.button, 0, 1, 1, 1)

        self.button.setStyleSheet("color: blue; background-color: black")
        self.label.setStyleSheet("color: blue; background-color: black")

        # Add button signal to level_choice slot
        self.button.clicked.connect(self.level_choice)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.creation_interface()
        self.show()

    def creation_interface(self):
        self.show()




    def level_choice(self):
        """
        Affiche la page du menu de choix du niveau de difficulté """   #à faire/modifier
        self.close()


class GameDesign(QWidget):
    """ Classe chargée du dessin de la grille
    # et les robots
    # On lui passe une référence à une zone de dessin rectangulaire"""

    def __init__(self, grid, parent=None):
        super(GameDesign, self).__init__(parent)
        self.grid_size_x = len(grid)
        self.grid_size_y = len(grid[0])
        self.grid = grid
        self.repaint()
        self.setMinimumSize(200, 200)
        self.draw_robot()

    def scale_x(self, x):
        return x * MaFenetre.GAMEZONE_SIZE / self.grid_size_x

    def scale_y(self, y):
        return y * MaFenetre.GAMEZONE_SIZE / self.grid_size_y

    def draw_grid(self, p):
        # horizontal lines
        for i in range(self.grid_size_y + 1):
            p.drawLine(0, self.scale_y(i), self.scale_x(self.grid_size_x), self.scale_y(i))
        # vertical lines
        for i in range(self.grid_size_x + 1):
            p.drawLine(self.scale_x(i), 0, self.scale_x(i), self.scale_y(self.grid_size_y))

    def _draw_horizontal_wall_(self, p, start):
        """ Draw an horizontal wall of length 1, starting from position start = (i,j)
            Ending on position (i+1,j) """
        i, j = start
        p.drawLine(self.scale_x(i), self.scale_y(j), self.scale_x(i + 1), self.scale_y(j), )

    def _draw_vertical_wall_(self, p, start):
        """ Draw a vertical wall of length 1, starting from position start = (i,j)
                    Ending on position (i,j+1) """
        i, j = start
        p.drawLine(self.scale_x(i), self.scale_y(j), self.scale_x(i), self.scale_y(j + 1))

    def draw_walls(self, p):
        for i in range(self.grid_size_x):
            for j in range(self.grid_size_y):
                cell = self.grid[j][i]
                if cell & g.SOUTH:
                    self._draw_horizontal_wall_(p, (i, j+1))
                if cell & g.NORTH:
                    self._draw_horizontal_wall_(p, (i, j))
                if cell & g.EAST:
                    self._draw_vertical_wall_(p, (i + 1, j))
                if cell & g.WEST:
                    self._draw_vertical_wall_(p, (i, j))

    def draw_robot(self):
        # On ajoute un bouton dans la zone de dessin
        robot = QPushButton(QPixmap(RED_ROBOT), "", self)
        robot.setStatusTip("Cliquez sur le robot puis dirigez le avec les flèches")
        #button_action.triggered.connect(self.onMyToolBarButtonClick)
        robot.setCheckable(True)
        robot.setGeometry(10, 10, 35, 35)
        # On choisit une image à mettre sur le bouton
    #    robot.setStyleSheet("background-image: url(robot rouge.png);");

    def paintEvent(self, e):
        p = QPainter(self)

        brush = QBrush(QColor(0, 0, 0))
        p.setBrush(brush)

        self.draw_grid(p)
        wall_pen = QPen()
        wall_pen.setColor(QColor(0, 0, 0))
        wall_pen.setWidth(3)
        p.setPen(wall_pen)

        print(p.brush())
        self.draw_walls(p)


app = QApplication(sys.argv)
fen = MaFenetre()
sys.exit(app.exec_())
