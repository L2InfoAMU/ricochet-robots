# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 22:48:38 2019
Exemple de la note technique
@author: Martin
"""

import PySimpleGUI as sg
game_zone=sg.Graph(canvas_size=(400,400) ,\
                   graph_bottom_left = (-1,-1),\
                   graph_top_right=(11,11),\
                   background_color='White',\
                   enable_events = True,\
                   key='graph',\
                   float_values=False)    

layout = [[game_zone]]
window = sg.Window('grid', layout,return_keyboard_events=True
                   ) 
window.Finalize()  

#drawing the grid
for i in range(11) :
    game_zone.DrawLine((0,i), (10,i),width=1,color='grey') 
    game_zone.DrawLine((i,0), (i,10),width=1,color='grey') 
    game_zone.DrawCircle( (1.5,1.5) ,radius=0.4,fill_color='blue')
while True:                             # The Event Loop
    event, values = window.read() 
#   print(event)
    print(values) 