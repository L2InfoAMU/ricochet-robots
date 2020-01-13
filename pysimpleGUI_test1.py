# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import game as g
from itertools import cycle


GAMEZONE_SIZEX = 400
GAMEZONE_SIZEY = 400

# couleurs
WHITE = '#fff'
BLACK = '#000'

BLUE = '#00f'
DARK_BLUE = '#3b3bd1'
RED = '#f00'
DARK_RED = '#d13b3b'
GREEN = '#0f0'
DARK_GREEN = '#00d100'
YELLOW = '#ff0'
DARK_YELLOW = '#b3b34b'
BLACK = '#000'
GREY = '#888'
BACKGROUND_COLOR='white'
GRID_COLOR='grey'
WALLS_WIDTH = 4
WALLS_COLOR = 'black'
PASSIVE_BOT_SIZE = 0.3
ACTIVE_BOT_SIZE=0.4
# sg.change_look_and_feel('DarkAmber')    # Remove line if you want plain gray windows
class GameDesign :
    # Classe qui a la responsabilité de dessiner le plateau de jeu 
    # et les robots
    # On lui passe une référence à une zone de dessin rectangulaire
    
    BOT_COLORS={0: (DARK_RED,RED),
                1: (DARK_BLUE,BLUE),
                2: (DARK_GREEN,GREEN),
                3: (DARK_YELLOW,YELLOW),
                4: (GREY, BLACK) }
    @classmethod
    def GameZone(cls,grid) :
        cls.grid_size_x=len(grid)
        cls.grid_size_y=len(grid[0])
        cls.grid=grid
        cls.game_zone = sg.Graph( \
                canvas_size = (GAMEZONE_SIZEX,GAMEZONE_SIZEY),\
                graph_bottom_left = (0,0),\
                graph_top_right =(cls.grid_size_x,cls.grid_size_y),\
                background_color = BACKGROUND_COLOR,\
                enable_events = True,\
                key = '-GAME-ZONE-' 
                )
        
    @classmethod   
    def DrawGrid(cls):
        # horizontal lines
        for i in range(cls.grid_size_y+1) :
            cls.game_zone.DrawLine(
                    (0,i), 
                    (cls.grid_size_x,i),
                    width=1,
                    color=GRID_COLOR
                    )
        # vertical lines
        for i in range(cls.grid_size_x+1) :           
            cls.game_zone.DrawLine(
                    (i,0), 
                    (i,cls.grid_size_y),
                    width=1,
                    color=GRID_COLOR
                    )
    @classmethod
    def _draw_horizontal_wall_(cls,start) :
        """ Draw an horizontal wall of length 1, starting from position start = (i,j)
            Ending on position (i+1,j) """
        i,j = start
        cls.game_zone.DrawLine((i,j), (i+1,j), 
                               width=WALLS_WIDTH, 
                               color=WALLS_COLOR
                              )
    @classmethod
    def _draw_vertical_wall_(cls,start) :
        """ Draw a vertical wall of length 1, starting from position start = (i,j)
            Ending on position (i,j+1) """
        i,j = start
        cls.game_zone.DrawLine((i,j), (i,j+1), 
                               width=WALLS_WIDTH, 
                               color=WALLS_COLOR
                              )
    @classmethod        
    def DrawWalls(cls) :
        for i in range(cls.grid_size_x) :
            for j in range(cls.grid_size_y) :
                cell =cls.grid[i][j]
                if cell & g.SOUTH : cls._draw_horizontal_wall_((i,j))
                if cell & g.NORTH : cls._draw_horizontal_wall_((i,j+1))
                if cell & g.EAST : cls._draw_vertical_wall_((i+1,j))
                if cell & g.WEST : cls._draw_vertical_wall_((i,j))
                
                
    @classmethod    
    def __draw_passive_robot__(cls,r):
        """ crée un objet de type cercle pour dessiner un robot """
        i,j= r.position
        color = cls.BOT_COLORS[r.numero][0]
        return cls.game_zone.DrawCircle(
                            (i+.5,j+.5),
                            radius=PASSIVE_BOT_SIZE,
                            fill_color= color #r.color
                          )
    @classmethod    
    def __draw_active_robot__(cls,r):
        """ crée un objet de type cercle pour dessiner un robot """
        i,j= r.position
        color = cls.BOT_COLORS[r.numero][1]
        return cls.game_zone.DrawCircle(
                            (i+.5,j+.5),
                            radius=ACTIVE_BOT_SIZE,
                            fill_color= color
                          )
    
    @classmethod 
    def DrawRobots(cls, robots):
    
        assert ( len(robots) > 0)
        cls.design_robots = []
        cls.bot_number = len(robots)
        cls.bot_focused = 0
        cls.design_robots.append(cls.__draw_active_robot__(robots[0]))
        for robot in robots[1:] :
            cls.design_robots.append(cls.__draw_passive_robot__(robot))
        
        
            
grid =[[9, 8, 8, 8, 10, 12],
       [1, 0, 2, 4,  9, 6],
       [3, 0, 8, 0,  0, 12],
       [9, 0, 0, 0,  0, 4],
       [1, 4, 1, 0, 6, 5],
       [7, 3, 2, 2, 10, 6]]        
        
        
        
GameDesign.GameZone(grid)
layout = [[GameDesign.game_zone],
          [ sg.Exit()]]      

window = sg.Window('Window that stays open',
                    layout,
                    return_keyboard_events=True
                    ) 
window.Finalize()  

GameDesign.DrawGrid()
GameDesign.DrawWalls()
r1 = g.Robot((3,0),1)
r2 = g.Robot((4,4),2)
r3 = g.Robot((0,3),3)
GameDesign.DrawRobots([r1,r2,r3])

    
while True:                             # The Event Loop
    event, values = window.read() 
    print(event, values)

    if event in (None, 'Exit'):      
        break      

window.close()