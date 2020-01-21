# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 03:04:54 2019

@author: Martin
"""


#• test de la classe game

import grid
import goal
import robot
import game

SOUTH = grid.SOUTH
EAST = grid.EAST
NORTH = grid.NORTH    
WEST = grid.WEST

table =[[9, 8, 8, 8, 10, 12],
            [1, 0, 2, 4,  9, 6],
            [3, 0, 8, 0,  0, 12],
            [9, 0, 0, 0,  0, 4],
            [1, 4, 1, 0, 6, 5],
            [7, 3, 2, 2, 10, 6]]


test_grid = grid.Grid(table)
r0 = robot.Robot((3,0),0)
r1 = robot.Robot((4,4),1)
robots=[r0,r1]
goal = goal.Goal(r0 ,(1,1))

jeutest=game.Game(test_grid,robots,goal)

print(robots)
r0.move(NORTH)

print(robots)
r1.move(SOUTH)
print(jeutest.robots)

