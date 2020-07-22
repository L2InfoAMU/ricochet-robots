import os
import sys
import unittest
import json
sys.path.insert(0, os.path.abspath('..'))

from robot import Board

GRID_PATH = '../grids/'

class BoardTest(unittest.TestCase) :
    """ Test case de la classe Board """

    def setUp(self) :
        """ Initialisation des tests 
            Cette méthode est appelée avant chaque test.
            Voir la documentation unitest
        """
        # les figures de ces tests sont données dans la documentation
        self.square3 = [[9,1,3],        
                        [8,0,2],           
                        [12,4,6]] 
        self.corner2 = [ [9,1],[8,2]]
        
        # les 12 grilles 8x8 classiques sont chargées dans un dictionnaire.
        fp = open(GRID_PATH+"classic_grids.grd",'r')
        self.grids = json.load(fp)
        fp.close()

    def test_Board(self) :
        b1 = Board()

        self.assertEqual( b1.width, 0)
        self.assertEqual (b1.height,0)
        self.assertEqual (b1.grid , None)


unittest.main()
