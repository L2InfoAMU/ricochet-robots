import os
import sys
import unittest
import json
sys.path.insert(0, os.path.abspath('..'))

from goal import Goal
from rcolors import RColors

class GameTest(unittest.TestCase) :
    
    def test_str(self) :
        goal1 = Goal(RColors.RED, (0,0))
        goal2 = Goal(RColors.GREEN, (7,7))
        print (" Test de la classe goal")
        print (goal1)
        print (goal2)

if __name__=="__main__":       
    unittest.main()
