

# testing the solveur

from solveur import solveur
from robot import *

fd = open('test2.txt','r')
A = Board.load_from_file(fd)
fd.close()
group = Robot_group()
r1 = Robot (group, RColors.RED, (0,0) )
r2 = Robot (group, RColors.GREEN, (4,0) )
r3 = Robot (group, RColors.BLUE, (3,4) )
r4 = Robot (group, RColors.YELLOW, (2,4) )
goal = Goal(RColors.RED, (0,4))
game = Game(A,group,goal)

solution = solveur(game).find_solution()
print (solution)

fd = open('grid3.txt','r')
board3x3 = Board.load_from_file(fd)
fd.close()
group = Robot_group()

r1 = Robot (group, RColors.RED, (0,0) )
r2 = Robot (group, RColors.GREEN, (2,0) )
r3 = Robot (group, RColors.BLUE, (0,2) )
r4 = Robot (group, RColors.YELLOW, (2,2) )
goal = Goal(RColors.YELLOW, (0,0))
game = Game(board3x3,group,goal)
solution = solveur(game).find_solution()
print (solution)

fd = open('square5.txt','r')
square5 = Board.load_from_file(fd)
fd.close()
group = Robot_group()

r1 = Robot (group, RColors.RED, (0,0) )
r2 = Robot (group, RColors.GREEN, (4,0) )
r3 = Robot (group, RColors.BLUE, (0,4) )
r4 = Robot (group, RColors.YELLOW, (4,4) )
goal = Goal(RColors.YELLOW, (3,2))
game = Game(square5,group,goal)
solution = solveur(game).find_solution()
print (solution)