""" La classe GameDesign est responsable de dessiner le plateau de jeu avec les robots

"""

import sys
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLayout
from PySide2.QtGui import QImage
from robot import *



PIXMAPS = [ QImage("./icons/0.bmp"),
            QImage("./icons/N.bmp"),
            QImage("./icons/E.bmp"),
            QImage("./icons/NE.bmp"),
            QImage("./icons/S.bmp"),
            QImage("./icons/NS.bmp"),
            QImage("./icons/ES.bmp"),
            QImage("./icons/NES.bmp"),
            QImage("./icons/W.bmp"),
            QImage("./icons/NW.bmp"),
            QImage("./icons/EW.bmp"),
            QImage("./icons/NEW.bmp"),
            QImage("./icons/SW.bmp"),
            QImage("./icons/NSW.bmp"),
            QImage("./icons/ESW.bmp"),
            QImage("./icons/NESW.bmp")]


class Pos(QWidget):


    def __init__(self, x, y, game):
        super().__init__()
        self.game = game

        self.setFixedSize(QSize(20, 20))
        self.x = x
        self.y = y
        self.reset()



    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        r = event.rect()   #dessine juste dans le Qwidget
        p.drawPixmap(r, QPixmap(PIXMAPS[str(self.game.board.grid[x][y])]))



class MainWindow(QMainWindow):

    def __init__(self, game):
        super().__init__()
        self.game = game


        # tag::grid[]
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setSizeConstraint(QLayout.SetFixedSize)
        # end::grid[]



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

fd = open("D:/test2.txt",'r')
A = Board.load_from_file(fd)
group = Robot_group()
r1 = Robot (group, RColors.RED, (0,0) )
r2 = Robot (group, RColors.GREEN, (5,0) )
game = Game(A,group,None)
window = MainWindow(game)
window.show()

app.exec_()
