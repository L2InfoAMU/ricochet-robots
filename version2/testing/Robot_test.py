import os
import sys
import unittest
import json
sys.path.insert(0, os.path.abspath('..'))

from robot import Robot, Robot_group
from board import Board
from directions import Direction
from rcolors import RColors

GRID_PATH = '../grids/'
CLASSIC_GRID = GRID_PATH+"classic16x16.json"

class RobotTest(unittest.TestCase) :
    """ Test case des classes Robot et Robot_group """

    def test_Robot(self) :
        robots = Robot_group()
        r1 = Robot(robots, RColors.RED, (0,0))
        r2 = Robot(robots, RColors.BLUE, (1,1))
        r3 = Robot(robots, RColors.GREEN, (2,1))

        self.assertTrue(r1.color in robots)
        self.assertEqual(r1 , robots[r1.color])
        self.assertTrue(r2.color in robots)
        self.assertTrue(r3.color in robots)
        
        # tentative d'ajout d'un robot de même couleur
        with  self.assertRaises(AssertionError ) :
            r4 = Robot(robots, RColors.GREEN, (2,2))
        
        # tentative d'ajout d'un robot a une position déjà occupée
        with  self.assertRaises(AssertionError ) :
            r4 = Robot(robots, RColors.YELLOW, (2,1))      

        r4 = Robot(robots, RColors.YELLOW, (2,2))
        self.assertTrue(r4.color in robots)

    def test_str(self) :
        robots = Robot_group()
        r1 = Robot(robots, RColors.RED, (0,0))
        r2 = Robot(robots, RColors.BLUE, (1,1))
        r3 = Robot(robots, RColors.GREEN, (2,1))
        r4 = Robot(robots, RColors.YELLOW, (2,2))

        self.assertEqual(str(r1) ,'"R" : [0, 0]')
        self.assertEqual(str(r2) ,'"B" : [1, 1]')
        self.assertEqual(str(r3) ,'"G" : [2, 1]')
        self.assertEqual(str(r4) ,'"Y" : [2, 2]')

        print(" Test affichage d'un ensemble de robots format json")
        print(robots)

    def test_cell_occupied(self) :
        """ test de la fonction cell_occupied """

        robots = Robot_group()
        Robot(robots, RColors.RED, (0,0))
        Robot(robots, RColors.BLUE, (1,1))
        Robot(robots, RColors.GREEN, (2,1))
        Robot(robots, RColors.YELLOW, (2,2))

        for position in [(0,0) , (1,1), (2,1) , (2,2)] :
            self.assertTrue(robots.cell_occupied( position))

        for position in [(1,0) , (1,2), (2,5) , (10,10)] :
            self.assertFalse(robots.cell_occupied( position))

    def test_move1(self) :
        """ test de la fonction move d'un robot sur la grille carrée simple 3x3"""

        square3 = Board([[9,1,3],[8,0,2],[12,4,6]] )
        robots = Robot_group()
        r1 = Robot(robots, RColors.RED, (0,0))

        r1.move(Direction.N,square3)
        self.assertEqual(r1.position, (0,0))
        r1.move(Direction.W,square3)
        self.assertEqual(r1.position, (0,0))
        r1.move(Direction.S,square3)
        self.assertEqual(r1.position, (2,0))
        r1.move(Direction.E,square3)
        self.assertEqual(r1.position, (2,2))
        r1.move(Direction.N,square3)
        self.assertEqual(r1.position, (0,2))

        r1.position = (0,1)
        r1.move(Direction.S,square3)
        self.assertEqual(r1.position, (2,1))

    def test_move2(self) :
        """ test de la fonction move avec plusieurs robots"""

        # test sur la grille carrée simple 3x3
        square3 = Board([[9,1,3],[8,0,2],[12,4,6]] )

        # on positionne un robot à chaque coin
        robots = Robot_group()
        r1 = Robot(robots, RColors.RED, (0,0))
        r2 = Robot(robots, RColors.BLUE, (0,2))
        r3 = Robot(robots, RColors.GREEN, (2,0))
        r4 = Robot(robots, RColors.YELLOW, (2,2))

        r1.move(Direction.S,square3)
        self.assertEqual(r1.position, (1,0))
        r2.move(Direction.S,square3)
        self.assertEqual(r2.position, (1,2))
        r2.move(Direction.W,square3)
        self.assertEqual(r2.position, (1,1))
        r4.move(Direction.N,square3)
        self.assertEqual(r4.position, (0,2))
        r3.move(Direction.E,square3)
        self.assertEqual(r3.position, (2,2))

    def test_move3(self) :
        """ test de la fonction move avec plusieurs robots"""

        # test sur la grille classic16x16
        classic, = Board.load_from_json(CLASSIC_GRID )

        # on positionne un robot à chaque coin
        robots = Robot_group()
        r1 = Robot(robots, RColors.RED, (0,0))
        r2 = Robot(robots, RColors.BLUE, (0,7))
        r3 = Robot(robots, RColors.GREEN, (7,0))
        r4 = Robot(robots, RColors.YELLOW, (7,7))

unittest.main()
