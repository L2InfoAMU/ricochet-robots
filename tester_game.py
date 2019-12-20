# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 03:04:54 2019

@author: Martin
"""


#• test de la classe game

import game 

test_grid =[[9, 8, 8, 8, 10, 12],
            [1, 0, 2, 4,  9, 6],
            [3, 0, 8, 0,  0, 12],
            [9, 0, 0, 0,  0, 4],
            [1, 4, 1, 0, 6, 5],
            [7, 3, 2, 2, 10, 6]]


"""
 - - - - - -
| |
"""

r1 = game.Robot((3,0),1)
r2 = game.Robot((4,4),2)
jeutest=game.Game(test_grid,robots=[r1,r2])


print(jeutest.robots)
jeutest.move_robot(r1,game.NORTH)

print(jeutest.robots)
jeutest.move_robot(r2,game.SOUTH)
print(jeutest.robots)
jeutest.move_robot(r2,game.EAST)
print(jeutest.robots)
jeutest.move_robot(r2,game.NORTH)
print(jeutest.robots)
jeutest.move_robot(r2,game.WEST)

print(jeutest.robots)
jeutest.move_robot(r2,game.SOUTH)
print(jeutest.robots)
jeutest.move_robot(r2,game.EAST)
print(jeutest.robots)
jeutest.move_robot(r2,game.NORTH)
print(jeutest.robots)
jeutest.move_robot(r1,game.SOUTH)
print(jeutest.robots)
jeutest.move_robot(r1,game.EAST)
print(jeutest.robots)