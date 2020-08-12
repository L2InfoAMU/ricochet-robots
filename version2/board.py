""" Projet Maths Info pour le DU CCIE et la L3 Maths-Info
Chef de projet : CANALS Martin L3
Développeurs : AUBIN François DU CCIE, GIANI Théo L3

fichier board.py 
définition de la classe Board, ayant la responsabilité de manipuler un plateau de jeu.
Le plateau est un tableau d'objets de type Cell.
    Les cases sont dans des listes de listes
    On stocke aussi la hauteur et la largeur du plateau.
"""

from directions import Direction, NORTH, SOUTH, EAST, WEST
from cell import Cell

GRID_PATH = './grids/'
CLASSIC_GRIDS = GRID_PATH+'classic_grids.json'

class Board :

    def __init__(self, data=[], check_conformity = False) :
        """ 
        Constructeur de la classe Board
            board = Board( data,check_conformity )
            data est une liste de listes d'entiers pour la construction des cellules.
            check_conformity est un booléen, False par défaut.
            si check_conformity = True, une vérification de la conformité de la grille est effectuée
        """

        self.height = len(data)
        if self.height > 0 :
            self.width = len(data[0])
        else : self.width = 0

        self.grid = [ [Cell(walls) for walls in line]for line in data]

        if check_conformity :
            if not self._grid_conforms() : print( "grille non conforme")
            else : print( "grille conforme")

    def __str__(self) :
        """
        renvoie une représentation de la grille sous forme de chaîne de caractères :
        ' "grid" : [ [int,..., int], ...]
        """
        string ='"grid" : ['
        n = 0
        for line in self.grid :
            if n > 0 : string += ","
            string += "\n["
            n += 1
            m = 0
            for cell in line :
                if m > 0 : string += ", "
                m += 1
                string += str(cell)
            string +="]"
        string += "]"
        return string

    def _grid_conforms(self, verbose = False) :
        """
            Méthode privée pour vérifier la conformité de la grille
            cohérence de la redondance
            si verbose = True, la méthode affiche des messages en cas d'erreurs
        """
        w = self.width
        h = self.height
        conforms = True
        for i in range(h) :
            for j in range(w) :
                cell = self.grid[i][j]
                if i < h-1 :
                    cell_south = self.grid[i+1][j]
                    if cell.wall_at(Direction.S) != cell_south.wall_at(Direction.N) :
                        conforms = False
                        if verbose :
                            print (" Grille non conforme au SUD en ",i," , ",j)
                if j < w-1 :
                    cell_east = self.grid[i][j+1]
                    if cell.wall_at(Direction.E) != cell_east.wall_at(Direction.W) :
                        conforms = False
                        if verbose :
                            print (" Grille non conforme à l'EST en ",i," , ",j)
        return conforms

    def cell_at(self, position) :
        """
        renvoie la référence de la cellule à la position donnée :
         exemple : cell = board.cell_at((0, 0))
        """
        i , j = position
        return self.grid[i][j]


    def save_as_json(self, filename) :
        """ 
        permet de sauvegarder la grille au format json dans le fichier
        dont le nom est passé en paramètre
        """
        with open(filename,'w') as fd :
            fd.write(f'{"{"}\n{str(self)}\n{"}"}')
        fd.close()

    @staticmethod
    def load_from_file(fd) :
        """ méthode ancienne à ne plus utiliser """

        data = []
        for line in fd :
            donnees = line.strip().split()
            if donnees == [] : continue
            data.append([ int (value) for value in donnees])
        return Board(data)

    @staticmethod
    def load_from_json(filename, *names) :
        """ charge des grille depuis un fichier json,
            usage  : boards =  Board.load_from_json( filename , names)
                    filename est un nom de fichier
                    names est une liste de noms , par défaut 'grid'
                    *** renvoie un tuple ***
                    Pour charger une seule grille :
                    board , = Board.load_from_json( filename , 'grid')
        """
        if len(names) == 0 : names =('grid',)
        import json

        with open(filename,'r') as fd :
            data = json.load(fd)
        boards = []
        for name in names :
            if name in data :
                boards.append(Board(data[name]))

        fd.close()
        return tuple(boards)

    def rotate_left(self) :
        nbcol , nblin = self.width , self.height
        turned_grid = [[ self.grid[i][nbcol-j-1].rotate_left() for i in range(nblin)] for j in range(nbcol)]

        self.grid = turned_grid
        self.width , self.height = nblin , nbcol
        return self

    def rotate_right(self) :
        nbcol , nblin = self.width , self.height
        turned_grid = [[ self.grid[nblin-1-i][j].rotate_right() for i in range(nblin)] for j in range(nbcol)]

        self.grid = turned_grid
        self.width , self.height = nblin , nbcol
        return self

    def rotate_half(self) :
        nbcol , nblin = self.width , self.height
        turned_grid = [[ self.grid[nblin-1-i][nbcol-1-j].rotate_half() for j in range(nbcol)] for i in range(nblin)]
        self.grid = turned_grid
        self.width , self.height = nbcol , nblin
        return self

    def __add__(self, board2) :
        """ juxtaposition horizontale de deux grilles """
        # dimensions
        nl1, nc1 = self.height, self.width
        nl2, nc2 = board2.height, board2.width

        #compatibilité
        assert( nl1 == nl2)

        # jonctions des grilles
        grid3 = []
        for num_line in range (nl1) :
            grid3.append(self.grid[num_line] + board2.grid[num_line])

        # suture
        for i in range (nl1) :
            if grid3[i][nc1-1].wall_at(EAST) or grid3[i][nc1].wall_at(WEST) :
                grid3[i][nc1-1].add_wall(EAST)
                grid3[i][nc1].add_wall(WEST)

        board = Board()
        board.grid = grid3
        board.height = nl1
        board.width = nc1 + nc2
        return board


    def __sub__(board1, board2) :
        """ juxtaposition horizontale de deux grilles """
        # dimensions
        nl1, nc1 = board1.height, board1.width
        nl2, nc2 = board2.height, board2.width

        #compatibilité
        assert( nc1 == nc2)

        # jonctions des grilles
        grid3 = board1.grid + board2.grid

        # suture
        for i in range (nc1) :
            if grid3[nl1-1][i].wall_at(SOUTH) or grid3[nl1][i].wall_at(NORTH) :
                grid3[nl1-1][i].add_wall(SOUTH)
                grid3[nl1][i].add_wall(NORTH)

        board = Board()
        board.grid = grid3
        board.height = nl1 + nl2
        board.width = nc1
        return board

    @staticmethod
    def new_classic():
        """génération d'une grille classique du jeu, par composition aléatoire de 4 morceaux de grille"""
        from random import randint, shuffle

        colors = ['red', 'blue', 'green', 'yellow']
        shuffle(colors)
        b1,b2,b3,b4 = Board.load_from_json(CLASSIC_GRIDS, colors[0] + str(randint(1,3)),colors[1] + str(randint(1,3)),
                    colors[2] + str(randint(1,3)),colors[3] + str(randint(1,3)))

        return (b1 + b2.rotate_right()) - (b3.rotate_left() + b4.rotate_half())
