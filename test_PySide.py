import sys
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QPushButton, QMainWindow, QAction
from PySide2.QtGui import QKeySequence, QPainter, QColor, QBrush, QPaintEvent, QFont


import game as g

test_grid = [[9, 8, 8, 8, 10, 12],
             [1, 0, 2, 4, 9, 6],
             [3, 0, 8, 0, 0, 12],
             [9, 0, 0, 0, 0, 4],
             [1, 4, 1, 0, 6, 5],
             [7, 3, 2, 2, 10, 6]]


class MaFenetre(QMainWindow):
    GAMEZONE_SIZE = 300

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robot Ricochet")
        self.resize(800, 600)
        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.options_menu = self.menu.addMenu("Options")

        # New Qaction
        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.New)

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        self.file_menu.addAction(new_action)
        self.file_menu.addAction(exit_action)

        # Options QAction
        options_action = QAction("Op")

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Sur un jeu d'Alex Randolph")

        layout = QGridLayout()
        self.label = QLabel("Robot Ricochet", self)
        self.button = QPushButton("Cliquez ici pour commencer", self)
        self.button.setFont(QFont("Verdana", 25))

        layout.addWidget(self.label, 0, 0, 2, 3)
        layout.addWidget(self.button, 2, 1, 2, 4)

        self.button.setStyleSheet("color: blue; background-color: black")
        self.label.setStyleSheet("color: blue; background-color: black")

        # Add button signal to level_choice slot
        self.button.clicked.connect(self.level_choice)
        widget = QWidget()
        widget.setLayout(layout)
        widget2 = GameDesign(test_grid)
        widget2.resize(self.GAMEZONE_SIZE, self.GAMEZONE_SIZE)
        self.setCentralWidget(widget2)
        self.creation_interface()
        self.show()

    def creation_interface(self):
        self.show()

    def level_choice(self):
        """
        Affiche la page du menu de choix du niveau de difficulté """
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
        p.drawLine(self.scale_x(i), self.scale_y(j), self.scale_x(i + 1), self.scale_y(j))

    def _draw_vertical_wall_(self, p, start):
        """ Draw a vertical wall of length 1, starting from position start = (i,j)
                    Ending on position (i,j+1) """
        i, j = start
        p.drawLine(self.scale_x(i), self.scale_y(j), self.scale_x(i), self.scale_y(j + 1))

    def draw_walls(self, p):
        for i in range(self.grid_size_x):
            for j in range(self.grid_size_y):
                cell = self.grid[i][j]
                if cell & g.SOUTH:
                    self._draw_horizontal_wall_(p, (i, j))
                if cell & g.NORTH:
                    self._draw_horizontal_wall_(p, (i, j + 1))
                if cell & g.EAST:
                    self._draw_vertical_wall_(p, (i + 1, j))
                if cell & g.WEST:
                    self._draw_vertical_wall_(p, (i, j))

    def draw_robot(self):
        # On ajoute unbouton dans la zone de dessin
        robot = QPushButton("", self)
        robot.setGeometry(20, 20, 70, 70)
        # On choisit une image à mettre sur le bouton
        robot.setStyleSheet("background-image: url(robot rouge.png);");

    def paintEvent(self, e):
        p = QPainter(self)

        brush = QBrush(QColor(255, 0, 0))
        p.setBrush(brush)

        # self.draw_grid(p)
        print(p.brush())
        p.setBrush(QColor(120, 0, 10))
        print(p.brush())
        self.draw_walls(p)
        self.draw_robot()


app = QApplication(sys.argv)
fen = MaFenetre()
sys.exit(app.exec_())
