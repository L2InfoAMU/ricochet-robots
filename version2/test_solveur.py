

# testing the solveur

from solveur import solveur
from robot import *
from random import *
import time


"""
time_line = []
start = time.time()
time_inter = start
time_line.append(time_inter)
for x in range (7):
    for y in range(7):
        fd = open('./test3.txt','r')
        A = Board.load_from_file(fd)
        fd.close()
        group = Robot_group()
        a = randint(0, 3)
        while (a == x):
            a = randint(0, 3)
        b = randint(0, 3)
        while (b == x):
            b = randint(0, 3)
        r1 = Robot (group, RColors.RED, (a, b) )

        a = randint(4, 7)
        while (a == x):
            a = randint(4, 7)
        b = randint(4, 7)
        while (b == x):
            b = randint(4, 7)
        r2 = Robot (group, RColors.GREEN, (a, b) )
        a = randint(0, 3)
        while (a == x):
            a = randint(0, 3)
        b = randint(4, 7)
        while (b == x):
            b = randint(4, 7)
        r3 = Robot (group, RColors.BLUE, (a, b) )
        a = randint(4, 7)
        while (a == x):
            a = randint(4, 7)
        b = randint(0, 3)
        while (b == x):
            b = randint(0, 3)
        r4 = Robot (group, RColors.YELLOW, (a, b) )
        print(r1)
        print(r2)
        print(r3)
        print(r4)

        goal = Goal(RColors.RED, (x,y))
        game = Game(A,group,goal)


        solution = solveur(game).find_solution()
        print (solution)
        time_line.append(time.time() - time_inter)
        print (time.time() - time_inter)
        print()

        time_inter = time.time()
        time_line.append(time_inter)
print ("temps total : " + str(time_inter - start))

"""


fd = open('./version2/grid3.txt','r')
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

fd = open('./version2/square5.txt', 'r')
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
