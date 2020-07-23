import os
import sys
import unittest
import json
sys.path.insert(0, os.path.abspath('..'))

from rcolors import RColors

class RColorsTest(unittest.TestCase) :
    """ Test case de la classe RColors """

    def testRColors(self) :
        red = RColors.RED
        blue = RColors.BLUE 
        yellow = RColors.YELLOW 
        green = RColors.GREEN 

        self.assertEqual(str(red) , 'R')
        self.assertEqual(str(blue) , 'B')
        self.assertEqual(str(yellow) , 'Y')
        self.assertEqual(str(green) , 'G')

        self.assertEqual(red, RColors.from_str('R'))
        self.assertEqual(green, RColors.from_str('G'))
        self.assertEqual(yellow,RColors.from_str('Y'))
        self.assertEqual(blue,RColors.from_str('B'))
             
unittest.main()