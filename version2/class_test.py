# test des classes

"""
a = Cell()
print(a)
print(a.wall_at(WEST))
b = Cell(SOUTH+NORTH)
print(b.wall_at(SOUTH))
print(b.wall_at(EAST))

A = Board([[ 1,1,1],[2,2,2],[3,5,3]])
print(A)

fd = open("test.txt",'w')
A.save_to_file(fd)
fd.close()

fd = open("test2.txt",'r')
A = Board.load_from_file(fd)

print(A)

"""

from robot import Board, Robot,Goal, RColors, Game, Robot_group

fd = open("test2.txt",'r')
A = Board.load_from_file(fd)
group = Robot_group()
r1 = Robot (group, RColors.RED, (0,0) )
r2 = Robot (group, RColors.GREEN, (4,0) )
r3 = Robot (group, RColors.BLUE, (3,4) )
r4 = Robot (group, RColors.YELLOW, (2,4) )
goal = Goal(RColors.GREEN, (4,2))
game = Game(A,group,goal)
print (game.actions_list() )

state = game.do_action("RS")
state = game.do_actions("RE","GN","RN","BW","BN","YS" )

"""
print(game.get_state())

print ("etat gagnant ? ", game.state_is_win(game.get_state()))
r1.move(SOUTH,game)
print(r1)
r1.move(EAST,game)
print(r1)
r1.move(NORTH,game)
print(r1)
r1.move(EAST,game)
r2.move(EAST, game)
r2.move(EAST, game)
print(game.get_state())
print ("etat gagnant ? ", game.state_is_win(game.get_state()))
state = ((1, 4), (4, 2), (3, 4), (2, 4))
game.set_state(state )
print(game.get_state())
"""

"""
import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(400, 300)
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw_something()


    def draw_something(self):
        painter = QtGui.QPainter(self.label.pixmap())
       
        names=["Empty","N","E","EN","S","NS","ES","ENS","W","NW","EW","ENW","SW","NSW","ESW","ENSW"]
        images = [QtGui.QPixmap("./images/"+name+".bmp", format="bmp")  for name in names]
        painter.drawPixmap(QtCore.QPoint(0,0) , images[9])
        painter.drawPixmap(QtCore.QPoint(50,0) , images[3])
        painter.drawPixmap(QtCore.QPoint(0,50) , images[13])
        painter.drawPixmap(QtCore.QPoint(50,50) , images[6])                               
        painter.end()
        
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
"""