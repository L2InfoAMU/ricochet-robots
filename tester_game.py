# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 03:04:54 2019

@author: Martin
"""


#• test de la classe game

import game 

test_grid =[[12, 10, 12, 4, 5, 6],
            [10, 9, 0, 0, 6, 10],
            [8, 4, 0, 0, 0, 2],
            [8, 2,8, 0, 1, 2],
            [8, 0, 0, 0, 4, 3],
            [9, 1, 3, 9, 1, 7]]

"""
 - - - - - -
| |
"""

r1 = game.Robot((5,3),1)
r2 = game.Robot((1,4),2)
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