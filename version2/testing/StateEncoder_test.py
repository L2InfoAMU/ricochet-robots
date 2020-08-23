import os
import sys
import unittest
import json
sys.path.insert(0, os.path.abspath('..'))

from game import Game
from stateencoder import StateEncoder, arrangement

GAMES_PATH = '../games/'
GAME1 = GAMES_PATH + "game1.json"
GAME2 = GAMES_PATH + "game3.json"
game1 = Game.load_from_json(GAME1)
game2 = Game.load_from_json(GAME2)

my_encoder = StateEncoder(game1)

position_to_int, int_to_position = my_encoder.position_encoder_functions()

class StateEncoderTest( unittest.TestCase) :

    def setUp(self) :
        pass

    def test_arrangement(self) :

        self.assertEqual( arrangement(1,1),1)
        self.assertEqual( arrangement(2,1),2)
        self.assertEqual( arrangement(3,2),6)
        self.assertEqual( arrangement(3,3),6)
        self.assertEqual( arrangement(4,2),12)
        self.assertEqual( arrangement(4,3),24)
        self.assertEqual( arrangement(4,4),24)

    def test_position_to_int(self) :

        game1 = Game.load_from_json(GAME1) 
        my_encoder = StateEncoder(game1)

        position_to_int, _ = my_encoder.position_encoder_functions()
        num = 0
        for i in range(game1.board.height) :
            for j in range(game1.board.width) :
                position = (i,j)
                self.assertEqual( position_to_int( position ), num)
                num +=1

    def test_int_to_position(self) :

        game1 = Game.load_from_json(GAME1) 
        my_encoder = StateEncoder(game1)

        _, int_to_position = my_encoder.position_encoder_functions()
        num = 0
        for i in range(game1.board.height) :
            for j in range(game1.board.width) :
                position = (i,j)
                self.assertEqual(position, int_to_position(num) )
                num +=1

    def test_encoder_decoder(self) :
        game = Game.load_from_json(GAME1) 
        my_encoder = StateEncoder(game)

        encoder , decoder = my_encoder.state_index_function()

        for i in range(my_encoder.state_number) :
            self.assertEqual (encoder(decoder(i)), i)

        
        # test sur le fichier game3
        # grille 16x16 avec 2 robots
        #  
        my_encoder = StateEncoder(game2)
        encoder , decoder = my_encoder.state_index_function()

        index = 256 * 255-1
        expected_state = ( (15,15),(15,14))
        self.assertEqual( expected_state, decoder(index))
        self.assertEqual (encoder(expected_state), index)

        index = 0
        expected_state = ( (0,0),(0,1))
        self.assertEqual( expected_state, decoder(index))
        self.assertEqual (encoder(expected_state), index)
 



    

unittest.main()
        
       



        