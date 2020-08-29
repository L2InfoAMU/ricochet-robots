

# testing the solveur

from solveur import solveur
from robot import *
from random import *
from game import *
import time


GRIDS_PATH = "./grids/"

nb_robots = int(input("combien de robots voulez-vous sur votre jeu ? (1 - 4) "))


time_line = []
start = time.time()
time_inter = start
time_line.append(time_inter)
for x in range (5):
    for y in range(1,6):
        A, = Board.load_from_json(GRIDS_PATH + 'grid 14x14.json')
        group = Robot_group()
        a = randint(0, 3)
        while (a == x):
            a = randint(0, 3)
        b = randint(0, 3)
        while (b == x):
            b = randint(0, 3)
        r1 = Robot (group, RColors.RED, (a, b) )
        print(r1)
        if nb_robots > 1:
            a = randint(4, 7)
            while (a == x):
                a = randint(4, 7)
            b = randint(4, 7)
            while (b == x):
                b = randint(4, 7)
            r2 = Robot (group, RColors.GREEN, (a, b) )
            print(r2)
        if nb_robots > 2:
            a = randint(0, 3)
            while (a == x):
                a = randint(0, 3)
            b = randint(4, 7)
            while (b == x):
                b = randint(4, 7)
            r3 = Robot (group, RColors.BLUE, (a, b) )
            print(r3)
        if nb_robots > 3:
            a = randint(4, 7)
            while (a == x):
                a = randint(4, 7)
            b = randint(0, 3)
            while (b == x):
                b = randint(0, 3)
            r4 = Robot (group, RColors.YELLOW, (a, b) )
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
a = input("fini !")
"""


fd = open('grid3.txt','r')
board3x3 = Board.load_from_file(fd)
fd.close()
group = Robot_group()

r1 = Robot (group, RColors.RED, (0,0) )
r2 = Robot (group, RColors.GREEN, (2,0) )
r3 = Robot (group, RColors.BLUE, (0,2) )
# r4 = Robot (group, RColors.YELLOW, (2,2) )
goal = Goal(RColors.RED, (1,1))
game = Game(board3x3,group,goal)
solution = solveur(game).find_solution()
print (solution)

fd = open('square5.txt', 'r')
square5 = Board.load_from_file(fd)
fd.close()
group = Robot_group()

r1 = Robot (group, RColors.RED, (0,0) )
r2 = Robot (group, RColors.GREEN, (4,0) )
r3 = Robot (group, RColors.BLUE, (0,4) )
r4 = Robot (group, RColors.YELLOW, (4,4) )
goal = Goal(RColors.YELLOW, (2,2))
game = Game(square5,group,goal)


solution = solveur(game).find_solution()
print (solution)
"""
