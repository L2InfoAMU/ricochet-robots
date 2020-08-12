import os
import sys
import unittest
import json
sys.path.insert(0, os.path.abspath('..'))

from board import Board

GRID_PATH = '../grids/'
CLASSIC_GRIDS = GRID_PATH+"classic_grids.json"
GAMES_PATH = '../games/'
GAME1 = GAMES_PATH +"game1.json"

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
        self.bad = [ [1,2,3],[4,5,6]]
        self.rectangular = [ [13,1,3],[13,6,14]]

        # les 12 grilles 8x8 classiques sont chargées dans un dictionnaire.
        fp = open(CLASSIC_GRIDS,'r')
        self.grids = json.load(fp)
        fp.close()

    def test_EmptyBoard(self) :

        b1 = Board(check_conformity = False)

        self.assertEqual( b1.width, 0)
        self.assertEqual (b1.height,0)
        self.assertEqual (b1.grid , [])

    def test_Board(self) :
        b1 = Board(self.square3, check_conformity = False)

        self.assertEqual( b1.width, 3)
        self.assertEqual (b1.height,3)

        b2 = Board(self.rectangular, check_conformity = False)
        self.assertEqual( b2.width, 3)
        self.assertEqual (b2.height,2)

    def test_conformity(self) :
        """ test la fonction de vérification de conformité"""

        b1 = Board(self.square3, check_conformity = False)
        b2 = Board(self.corner2, check_conformity = False)
        b3 = Board(self.bad, check_conformity = False)
        b4 = Board(self.bad, check_conformity = False)

        self.assertTrue(b1._grid_conforms(verbose = False))
        self.assertTrue(b2._grid_conforms(verbose = False))
        self.assertFalse(b3._grid_conforms(verbose = False))
        self.assertFalse(b4._grid_conforms(verbose = False))


    def test_str(self) :
        """ test de la représentation sous forme de chaine de caractères"""
        b1 = Board(self.square3, check_conformity = False)

        self.assertEqual(str(b1), '[\n[9, 1, 3],\n[8, 0, 2],\n[12, 4, 6]]')

    def test_load_from_json(self) :
        """ test du chargement d'une grille depuis un fichier json """
        print ("testing loading from json files ")
        print( "load 'red1' from "+CLASSIC_GRIDS)

        b1, = Board.load_from_json(CLASSIC_GRIDS,'red1')
        print (str(b1))

        print ("load 'grid' from" + GAME1)

        b2, = Board.load_from_json(GAME1)
        print (str(b2))

    def test_rotate_left(self) :
        """ test de la rotation à gauche d'une grille
            square3 est une grille invariante par rotation
            corner2
        """
        b1 = Board(self.square3)
        str1 = str(b1)
        b1.rotate_left()
        self.assertEqual(str1 , str(b1))

        b2 = Board(self.corner2)
        b2 = b2.rotate_left()
        self.assertEqual(str(b2) , str(Board([ [8,1],[12,4]])))

        b3 = Board(self.rectangular)
        b3.rotate_left()
        self.assertEqual(str(b3) , str(Board([[9,7],[8,3],[14,14]])) )

    def test_rotate_right(self) :
        """ test de la rotation à gauche d'une grille
            square3 est une grille invariante par rotation
            corner2
        """
        b1 = Board(self.square3)
        str1 = str(b1)
        b1.rotate_right()
        self.assertEqual(str1 , str(b1))

        b2 = Board(self.corner2)
        b2 = b2.rotate_right()
        self.assertEqual(str(b2) , str(Board([ [1,3],[4,2]])))

        b3 = Board(self.rectangular)
        b3.rotate_right()
        self.assertEqual(str(b3) , str(Board([[11,11],[12,2],[13,6]])) )

    def test_rotate_half(self) :
        """ test de la rotation d'un demi tour d'une grille
            square3 est une grille invariante par rotation

        """
        b1 = Board(self.square3)
        str1 = str(b1)
        b1.rotate_half()
        self.assertEqual(str1 , str(b1))

        b2 = Board(self.corner2)
        b2 = b2.rotate_half()
        self.assertEqual(str(b2) , str(Board([ [8,2],[4,6]])))

        b3 = Board(self.rectangular)
        b3.rotate_half()
        self.assertEqual(str(b3) , str(Board([[11,9,7],[12,4,7]])) )

    def test_add(self) :
        """ test de la fusion horizontale de deux grilles"""

        b1 = Board(self.corner2)
        b2 = Board(self.corner2)
        b3 = b1 + b2.rotate_right()
        self.assertEqual(str(b3) , str(Board([[9,1,1,3],[8,2,12,2]])) )

    def test_div(self) :
        """ test de la fusion verticale de deux grilles """
        b1 = Board(self.corner2)
        b2 = Board(self.corner2)
        b3 = b1 - b2.rotate_left()

        self.assertEqual(str(b3) , str(Board([[9,1],[8,6],[8,1],[12,4]])) )

    def test_complete(self) :
        """ teste la constitution d'un plateau de jeu classique """
        print ("testing grid construction ")

        b1,b2,b3,b4 = Board.load_from_json(CLASSIC_GRIDS,'red1','blue1','green1','yellow1')

        b = (b1 + b2.rotate_right()) - (b3.rotate_left() + b4.rotate_half())

        self.assertTrue(b._grid_conforms())
        print(str(b))


    def test_save_as_json(self) :
        """ teste la sauvegarde dans un fichier json """
        print ("teste la sauvegarde dans un fichier json")

        from random import randint
        filename="test"+str(randint(0,10000))+".json"

        b1,b2,b3,b4 = Board.load_from_json(CLASSIC_GRIDS,'red1','blue1','green1','yellow1')

        b = (b1 + b2.rotate_right()) - (b3.rotate_left() + b4.rotate_half())
        b.save_as_json(filename)
        print("donnees sauvegardées dans "+filename)

        print ("teste la lecture du fichier sauvegardé")
        board, = Board.load_from_json(filename)

        self.assertEqual(str(b), str(board))
        
unittest.main()
