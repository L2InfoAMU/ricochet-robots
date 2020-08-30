import os
import sys
import unittest
import json
sys.path.insert(0, os.path.abspath('..'))


from rcolors import RColors
from robot import Robot, Robot_group
from board import Board
from goal import Goal
from game import  Game

GAMES_PATH = '../games/'
GAME1 = GAMES_PATH + "game1.json"
GRID_PATH = '../grids/'
GRID_FILENAME = GRID_PATH+"classic16x16.json"
class GameTest(unittest.TestCase) :

    def setUp(self) :
        board, = Board.load_from_json(GRID_FILENAME)
        robots = Robot_group()
        r1 = Robot(robots, RColors.RED, (5,0))
        r2 = Robot(robots, RColors.BLUE, (11,1))
        r3 = Robot(robots, RColors.GREEN, (2,15))
        r4 = Robot(robots, RColors.YELLOW, (10,13))   
        goal = Goal(RColors.RED, (0,7)) 
        self.game = Game(board,robots,goal)

    def test_save_to_json(self) :
        from random import randint
        filename="test_saving_game"+str(randint(0,10000))+".json"
        # self.game.save_to_json(filename)

    def test_load_from_json(self) :
        game = Game.load_from_json(GAME1)

        print("Test du chargement d'un jeu à partir d'un fichier json")
        print(" Lecture du fichier "+GAME1)
        print( "Grille :")
        print(game.board)
        print ("Robots :")
        print(game.robots)
        print ("Goal :")
        print(game.goal)

    def test_getstate(self) :
        
        state = self.game.get_state()
        self.assertEqual(state, ( (5,0),(11,1),(2,15),(10,13)))
        
        
        game = Game.load_from_json(GAME1)
        state = game.get_state()
        self.assertEqual(state, ( (0,3),(0,0),(1,0),(4,4)))

    def test_setstate(self) :

        # on teste 
        state = ((0,0),(4,0),(0,4),(4,4))
        self.game.set_state(state)
        self.assertEqual(state, self.game.get_state() )

        state = ((5,0),(11,1),(2,15),(10,13))
        self.game.set_state(state)
        self.assertEqual(state, self.game.get_state() )
       
    def test_state_is_won(self) :
        state = ((0,7),(11,1),(2,15),(10,13) )
        self.assertTrue( self.game.state_is_won(state))

        state = ((0,6),(11,1),(2,15),(10,13) )
        self.assertFalse( self.game.state_is_won(state))

    def test_is_won(self) :
        # test de la méthode is_won

        self.assertFalse( self.game.is_won())

        state = ((0,7),(11,1),(2,15),(10,13) )
        self.game.set_state(state)
        self.assertTrue(self.game.is_won())

        state = ((11,1),(0,7),(2,15),(10,13))
        self.game.set_state(state)
        self.assertFalse(self.game.is_won())

    def test_actions_list(self) :

        actions_list =  self.game.actions_list() 
        expected_list= ["RN","RE","RS","RW", "BN","BE","BS","BW","GN","GE","GS","GW", "YN","YE","YS","YW"]
        self.assertEqual (actions_list, expected_list)

    def test_doaction(self) :

        game = self.game

        initial_state = game.get_state()

        state = game.do_action( "RS")
        self.assertEqual( initial_state, state)

        state = game.do_action( "RW")
        self.assertEqual( initial_state, state)

        state = game.do_action( "RN")
        expected = ( (0,0),(11,1),(2,15),(10,13))
        self.assertEqual(expected, state)

        state = game.do_action( "RE")
        expected = ( (0,3),(11,1),(2,15),(10,13))
        self.assertEqual(expected, state)


        state = game.do_action( "GS")
        expected = ( (0,3),(11,1),(3,15),(10,13))
        self.assertEqual(expected, state)

        state = game.do_action( "GW")
        expected = ( (0,3),(11,1),(3,0),(10,13))
        self.assertEqual(expected, state)
       
        state = game.do_action( "GN")
        expected = ( (0,3),(11,1),(0,0),(10,13))
        self.assertEqual(expected, state)

        state = game.do_action( "GE")
        expected = ( (0,3),(11,1),(0,2),(10,13))
        self.assertEqual(expected, state)
  

        state = game.do_action( "BE")
        expected = ( (0,3),(11,10),(0,2),(10,13))
        self.assertEqual(expected, state)

        state = game.do_action( "YS")
        expected = ( (0,3),(11,10),(0,2),(15,13))
        self.assertEqual(expected, state)

        state = game.do_action( "YE")
        expected = ( (0,3),(11,10),(0,2),(15,15))
        self.assertEqual(expected, state)

    def test_do_actions(self) :


        game = self.game
        state = game.do_actions( "RS","RW","RN","RE","GS","GW","GN","GE","BE","YS","YE")       
        expected = ( (0,3),(11,10),(0,2),(15,15))
        self.assertEqual(expected, state)

if __name__=="__main__":       
    unittest.main()
