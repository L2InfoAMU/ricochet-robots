import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# print(sys.path)

 
from directions import Direction, NORTH, SOUTH, WEST, EAST
from cell import Cell
import unittest

class CellTest(unittest.TestCase) :
    """ Test case de la classe Cell """

    def test_Cell(self) :
        """ test le fonctionnement du constructeur """
        empty_cell = Cell(0)
        self.assertEqual( empty_cell.walls, Direction(0) )

        full_cell = Cell(15)
        self.assertEqual( full_cell.walls, Direction(15) )

        cell1 = Cell(NORTH+SOUTH)
        self.assertEqual( cell1.walls, Direction(5) )

    def test_add_wall(self) :
        """ teste la méthode add_wall"""
        empty_cell = Cell(0)
        empty_cell.add_wall(Direction.N)
        self.assertEqual( empty_cell.walls, Direction.N )
        empty_cell.add_wall(Direction.N)
        self.assertEqual( empty_cell.walls, Direction.N )
        empty_cell.add_wall(Direction.S)
        self.assertEqual( empty_cell.walls, Direction(5) )
        empty_cell.add_wall(Direction.E)
        self.assertEqual( empty_cell.walls, Direction(7) )
        empty_cell.add_wall(Direction.W)
        self.assertEqual( empty_cell.walls, Direction(15) )

    def test_str(self) :
        """ test la fonction __str__  """
        for i in range(16) :
            cell = Cell(i)
            self.assertEqual( str(cell), str(i))

    def test_wall_at(self) :
        """ test de la méthode wall_at """
        empty_cell = Cell(0)
        full_cell = Cell(15)
        for dir in Direction :
            self.assertFalse(empty_cell.wall_at(dir))
            self.assertTrue(full_cell.wall_at(dir))

    def test_rotate_left(self) :
        
            cell = Cell(0)
            cell.rotate_left()
            self.assertFalse (cell.wall_at(Direction.N))
            self.assertFalse (cell.wall_at(Direction.W))
            self.assertFalse(cell.wall_at(Direction.S))          
            self.assertFalse(cell.wall_at(Direction.E))

            cell = Cell(1) #
            cell.rotate_left()
            self.assertTrue (cell.wall_at(Direction.W))
            self.assertFalse(cell.wall_at(Direction.S))
            self.assertFalse(cell.wall_at(Direction.N))
            self.assertFalse(cell.wall_at(Direction.E))


            cell = Cell(3)  # NE
            cell.rotate_left()
            self.assertTrue (cell.wall_at(Direction.N))
            self.assertTrue (cell.wall_at(Direction.W))
            self.assertFalse(cell.wall_at(Direction.S))          
            self.assertFalse(cell.wall_at(Direction.E))
           
            cell = Cell(15) # NESW
            cell.rotate_left()
            self.assertTrue (cell.wall_at(Direction.N))
            self.assertTrue (cell.wall_at(Direction.W))
            self.assertTrue(cell.wall_at(Direction.S))          
            self.assertTrue(cell.wall_at(Direction.E))

    def test_rotate_right(self) :
        
            cell = Cell(0)
            cell.rotate_right()
            self.assertFalse (cell.wall_at(Direction.N))
            self.assertFalse (cell.wall_at(Direction.W))
            self.assertFalse(cell.wall_at(Direction.S))          
            self.assertFalse(cell.wall_at(Direction.E))

            cell = Cell(8) # W
            cell.rotate_right()
            self.assertFalse (cell.wall_at(Direction.W))
            self.assertFalse(cell.wall_at(Direction.S))
            self.assertTrue(cell.wall_at(Direction.N))
            self.assertFalse(cell.wall_at(Direction.E))


            cell = Cell(3)  # NE
            cell.rotate_right()
            self.assertFalse (cell.wall_at(Direction.N))
            self.assertFalse (cell.wall_at(Direction.W))
            self.assertTrue(cell.wall_at(Direction.S))          
            self.assertTrue(cell.wall_at(Direction.E))
           
            cell = Cell(15) # NESW
            cell.rotate_right()
            self.assertTrue (cell.wall_at(Direction.N))
            self.assertTrue (cell.wall_at(Direction.W))
            self.assertTrue(cell.wall_at(Direction.S))          
            self.assertTrue(cell.wall_at(Direction.E))

    def test_rotate_half(self) :
        
            cell = Cell(0)
            cell.rotate_half()
            self.assertFalse (cell.wall_at(Direction.N))
            self.assertFalse (cell.wall_at(Direction.W))
            self.assertFalse(cell.wall_at(Direction.S))          
            self.assertFalse(cell.wall_at(Direction.E))

            cell = Cell(8) # W
            cell.rotate_half()
            self.assertFalse (cell.wall_at(Direction.W))
            self.assertFalse(cell.wall_at(Direction.S))
            self.assertTrue(cell.wall_at(Direction.E))
            self.assertFalse(cell.wall_at(Direction.N))


            cell = Cell(3)  # NE
            cell.rotate_half()
            self.assertFalse (cell.wall_at(Direction.N))
            self.assertFalse (cell.wall_at(Direction.E))
            self.assertTrue(cell.wall_at(Direction.S))          
            self.assertTrue(cell.wall_at(Direction.W))
           
            cell = Cell(15) # NESW
            cell.rotate_half()
            self.assertTrue (cell.wall_at(Direction.N))
            self.assertTrue (cell.wall_at(Direction.W))
            self.assertTrue(cell.wall_at(Direction.S))          
            self.assertTrue(cell.wall_at(Direction.E))
        
if __name__=="__main__":       
    unittest.main()
