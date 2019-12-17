import PySimpleGUI as sg
import game as g



test_grid =[[9, 8, 8, 8, 10, 12],
            [1, 0, 2, 4,  9, 6],
            [3, 0, 8, 0,  0, 12],
            [9, 0, 0, 0,  0, 4],
            [1, 4, 1, 0, 6, 5],
            [7, 3, 2, 2, 10, 6]]


class GameDesign :
    # Classe qui a la responsabilité de dessiner le plateau de jeu 
    # et les robots
    # On lui passe une référence à une zone de dessin rectangulaire
    
    GAMEZONE_SIZEX = 400
    GAMEZONE_SIZEY = 400
    BACKGROUND_COLOR='white'
    @classmethod
    def game_zone(cls,grid) :
        cls.grid_size_x=len(test_grid)
        cls.grid_size_y=len(test_grid[0])
        
        cls.game_zone = sg.Graph( \
                canvas_size = (GAMEZONE_SIZEX,GAMEZONE_SIZEY),\
                graph_bottom_left = (0,0),\
                graph_top_right =(cls.grid_size_x,cls.grid_size_y),\
                background_color = BACKGROUND_COLOR,\
                enable_events = True,\
                key = '-GAME_ZONE-' 
                )
        
        
    
        
        
        
        




sg.change_look_and_feel('DarkAmber')    # Remove line if you want plain gray windows

game_zone=sg.Graph(canvas_size=(400,400) ,\
                   graph_bottom_left = (-1,-1),\
                   graph_top_right=(grid_size_x+1,grid_size_y+1),\
                   background_color='White',\
                   enable_events = True,\
                   key='graph',\
                   float_values=True)                     # identifiant de la zone


layout = [[game_zone],
          [sg.Input(key='-IN-')],      
          [sg.Button('Read'), sg.Exit()]]      


window = sg.Window('Window that stays open', layout) 
window.Finalize()  

for i in range(grid_size_x) :
    game_zone.DrawLine((0,i), (grid_size_x,i),width=1,color='grey') 
    game_zone.DrawLine((i,0), (i,grid_size_y),width=1,color='grey') 
 
"""    
game_zone.DrawLine( (0,0),(grid_size_x,0),width = 4, color='black')
game_zone.DrawLine( (grid_size_x,0),(grid_size_x,grid_size_y),width = 4, color='black')   
game_zone.DrawLine( (grid_size_x,grid_size_y),(0,grid_size_y),width = 4, color='black')
game_zone.DrawLine( (0,0),(0,grid_size_y),width = 4,color='black')
"""

r1=game_zone.draw_circle((4.5,4.5),radius=10,fill_color='blue')
#walls
for i in range(grid_size_x) :
    for j in range(grid_size_y) :
        cell =test_grid[i][j]
        if cell & g.SOUTH : game_zone.DrawLine( (i,j) , (i+1,j),width=4)
        if cell & g.EAST : game_zone.DrawLine( (i+1,j) , (i+1,j+1),width=4)
        if cell & g.NORTH : game_zone.DrawLine( (i,j+1) , (i+1,j+1),width=4)
        if cell & g.WEST : game_zone.DrawLine( (i,j) , (i,j+1),width=4)
        
            
            
            
    
while True:                             # The Event Loop
    event, values = window.read() 
    print(event, values)

    game_zone.MoveFigure(r1,-1,0)       
    if event in (None, 'Exit'):      
        break      

window.close()