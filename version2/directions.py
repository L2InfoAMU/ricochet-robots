
# Enumération pour les directions
from enum import IntFlag
class Direction(IntFlag) :
    N = 1
    E = 2
    S = 4
    W = 8

    def __str__(self) :
        if self  in direction_names :
            return direction_names[self]
        return ''

    @classmethod
    def from_str(cls , string) : 
        assert string in direction_by_name
        return direction_by_name[string]

direction_names = {Direction.E : 'E',
                        Direction.S : 'S',
                        Direction.N : 'N',
                        Direction.W : 'W'}
direction_by_name = {'N' : Direction.N,
                            'E' : Direction.E,
                            'S' : Direction.S,
                            'W' : Direction.W}

# aliases
SOUTH = Direction.S
NORTH = Direction.N
EAST = Direction.E
WEST = Direction.W