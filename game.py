
# constante du module

MAX_ROBOT   = 5
SOUTH       = 0b0001
EAST        = 0b0010
NORTH       = 0b0100
WEST        = 0b1000


class Robot:
    # un robot est une structure passive
    # qui contient la position du robot : tuple(x , y)
    # son numéro 
    # 
    
    # On accède aux champs par robot.position, robot.numero, 
    # to do , écrire des méthodes set et get pour chaque champ  ?
    
        def __init__(self,position,numero):
            assert(0 < numero <= MAX_ROBOT)
            self.position = position
            self.numero = numero
            
        def __repr__(self):
            """ pour les besoins de test seulement"""
            return "r" + str(self.numero) \
                    + " à la position" + str(self.position)





class Game :
    # la classe jeu regroupe les données décrivant la grille de jeu
    # et la liste des robots
    # elle est chargée de déplacer les robots
    
    
    def __init__(self, grid, robots) :
        self.grid = grid.copy()        
        self.robots = robots.copy()
        self.width = len(grid[0])
        self.height = len(grid)
    
    def __cell_is_free__(self, pos):
        """ renvoie True si la case cell est occupée par un robot """
        """ pos est un tuple (x,y) correspondant à une case de la grille """
       
        for robot in self.robots :
           if robot.position == pos : return False
        return True
   
    def __cell_is_open__(self,pos,side) :
        """ renvoie True si il n'y a pas de cloison empêchant la sortie
            du côté side
            pos est un tuple (x,y) donnant la position de la case dans la grille
            voir documentation technique page .............
        """
        assert(side in [SOUTH, NORTH, EAST, WEST])

        x, y = pos
        assert (0 <= x < self.width)
        assert (0 <= y < self.height)
      
        return self.grid[x][y] & side == 0

    def move_robot(self, robot, direction):
        """ deplace robot sur le plateau suivant la direction
        la position de robot est changée """
        
        def step_builder(direction):
            """ renvoie une fonction qui calcule la prochaine position"""
            
            if direction == SOUTH:
                return lambda pos: (pos[0]+1, pos[1])
            if direction == NORTH:
                return lambda pos: (pos[0]-1, pos[1])
            if direction == EAST:
                return lambda pos: (pos[0], pos[1]+1)
            if direction == WEST:
                return lambda pos: (pos[0], pos[1]-1)
        
        next_position = step_builder(direction)
        
        while self.__cell_is_open__(robot.position, direction):
             
            target = next_position(robot.position)
             
            if not self.__cell_is_free__(target):
                break
             
            robot.position = target
             
    def get_game_state(self):
        """ renvoie l'etat du jeu  """
        
        # to do 
        
        pass
       
        
            
           












