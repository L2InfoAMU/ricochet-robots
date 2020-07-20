""" La classe GameDesign est responsable de dessiner le plateau de jeu avec les robots
ceci est une modification de test
"""

import sys
from PySide2.QtCore import QSize, Qt, QTimer
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLayout, QLabel
from PySide2.QtGui import QImage, QPixmap, QPainter
from robot import *
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt


PIXMAPS = [ QImage("icons/0.bmp"),
            QImage("icons/N.bmp"),
            QImage("icons/E.bmp"),
            QImage("icons/NE.bmp"),
            QImage("icons/S.bmp"),
            QImage("icons/NS.bmp"),
            QImage("icons/ES.bmp"),
            QImage("icons/NES.bmp"),
            QImage("icons/W.bmp"),
            QImage("icons/NW.bmp"),
            QImage("icons/EW.bmp"),
            QImage("icons/NEW.bmp"),
            QImage("icons/SW.bmp"),
            QImage("icons/NSW.bmp"),
            QImage("icons/ESW.bmp"),
            QImage("icons/NESW.bmp")]


class Pos(QWidget):


    def __init__(self, x, y, game):
        super().__init__()
        self.game = game

        self.setFixedSize(QSize(20, 20))
        self.x = x
        self.y = y




    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        r = event.rect()   #dessine juste dans le Qwidget
        p.drawPixmap(r, QPixmap(PIXMAPS[str(self.game.board.grid[x][y])]))
        p.end()

class WidgetTest(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel()
        canvas = QPixmap(400, 300)
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)

        self.draw_something()


    def draw_something(self):
        painter = QPainter(self.label.pixmap())

        names=["Empty","N","E","EN","S","NS","ES","ENS","W","NW","EW","ENW","SW","NSW","ESW","ENSW"]
        images = [QtGui.QPixmap("images/"+name+".bmp", format="bmp")  for name in names]
        painter.drawPixmap(QtCore.QPoint(0,0) , images[9])
        painter.drawPixmap(QtCore.QPoint(50,0) , images[3])
        painter.drawPixmap(QtCore.QPoint(0,50) , images[13])
        painter.drawPixmap(QtCore.QPoint(50,50) , images[6])
        painter.end()

class MainWindow(QMainWindow):

    def __init__(self, game):
        super().__init__()
        self.game = game


        # tag::grid[]
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        #self.grid.setSizeConstraint(QLayout.SetFixedSize)
        # end::grid[]
        a = WidgetTest()
        self.grid.addWidget(a, 0, 0)
        #self.init_map()
        widget = QWidget()
        widget.setLayout(self.grid)
        self.setCentralWidget(widget)



    def init_map(self):
        # Add positions to the map
        for x in range(0, self.game.board.width):
            for y in range(0, self.game.board.height):
                w = Pos(x, y, self.game)
                self.grid.addWidget(w, y, x)
                # Connect signal to handle expansion.
                # w.clicked.connect(self.select_robot)

        # Place resize on the event queue, giving control back to Qt before.
        QTimer.singleShot(0, lambda: self.resize(1, 1))




app = QApplication(sys.argv)

fd = open("test2.txt",'r')
A = Board.load_from_file(fd)
group = Robot_group()
r1 = Robot (group, RColors.RED, (0,0) )
r2 = Robot (group, RColors.GREEN, (1,0) )
game = Game(A,group,None)
window = MainWindow(game)
window.show()
print(game.get_state())
app.exec_()
