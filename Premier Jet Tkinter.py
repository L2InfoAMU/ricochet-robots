from tkinter import*

# Les cloisons de chaque case sont codées par un entier compris entre 0 et 15
# cloison du haut : bit de poids 1   |  cloison de droite bit de poids 2
# cloison du bas : bit de poids 4     |  cloison de gauche bit de poids 8
# Attention : dans la lecture de la grille le premier indice est celui
# des ordonnées :  grille[y][x]
grille = [[ 9,  5, 1, 1, 3,  9, 1, 1, 3],
              [10, 9, 0, 2, 8,  6, 8, 0, 2],
              [ 8,  0, 0, 0, 0,  1, 0, 0, 6],
              [12, 0, 0, 4, 0,  4, 0, 0, 3],
              [  9, 6, 8, 1, 0,  3, 0, 0, 2],
              [12, 1, 0, 0, 0,  0, 0, 4, 2],
              [  9, 6, 8, 0, 2, 12, 0, 3, 10],
              [  8, 1, 0, 0, 0,   1, 0, 0, 2],
              [12, 4, 4, 6, 12,   4, 4, 4, 6]]

# un dictionnaire qui mémorise les positions de tous les robots
robotsPos = {}

class Robot(object):
    directions = ['N', 'E', 'S', 'W']
    
    def __init__(self, x = 0, y = 0, colour = 'black'):
        self.x = x
        self.y = y
        self.colour = colour
        robotsPos[self.colour]=(self.x,self.y)        
        can.create_oval(self.x*cote + 12, self.y*cote + 12, (1 + self.x)*cote - 8, (1 + self.y)*cote - 8, fill=self.colour, outline="#DDD", width=3)

    @staticmethod
    def move(rbt, direction):
        # on efface le robot
        can.create_oval(rbt.x*cote + 12, rbt.y*cote + 12, (1 + rbt.x)*cote - 8, (1 + rbt.y)*cote - 8, fill="ivory", outline="#DDD", width=3)
        
        # la direction choisie est convertie en un entier entre 0 et 15 : North = 1, South = 4, East = 2, West = 8
        masque = 2 ** rbt.directions.index(direction)
        dx = (masque == 2) - (masque == 8)
        dy = (masque == 4) - (masque == 1)

        # on avance dans la direction choisie jusqu'à rencontrer une cloison ou un robot
        while (grille [rbt.y][rbt.x] & masque == 0 and (rbt.x + dx, rbt.y + dy) not in robotsPos.values()):
            rbt.x += dx
            rbt.y += dy

        # on met à jour le dictionnaire des positions et on affiche le robot
        robotsPos[rbt.colour] = (rbt.x,rbt.y)
        can.create_oval(rbt.x*cote + 12, rbt.y*cote + 12, (1 + rbt.x)*cote - 8, (1 + rbt.y)*cote - 8, fill=rbt.colour, outline="#DDD", width=3)


# generation() dessine le plateau
def generation():
      global can, cote
      cote=min((Heigth-300) //hauteurJeu,(Width-400)//largeurJeu)
      can=Canvas(fen,width=cote*largeurJeu+2,height=largeurJeu*cote+2,bg='ivory',relief="groove")
      can.grid(row=1,rowspan=7,column=2)
      for i in range (hauteurJeu):
            for j in range(largeurJeu):
                  color="ivory"                 
                  can.create_rectangle(j*cote+3,i*cote+2,j*cote+cote+3,i*cote+cote+2,fill=color,outline="grey")

#Les Bords haut et gauche
      can.create_line(3 , 2 , 3 + cote*largeurJeu, 2, width = 6)
      can.create_line(2 , 2 , 2 , 1 + cote*hauteurJeu, width = 6)
      
      for i in range(largeurJeu):
          for j in range(hauteurJeu):
              # Les cloisons horizontales
              if grille[j][i] & 2: can.create_line(2 + cote*(i + 1), 2 + cote*(j), 3 + cote * (i + 1), 2 + cote* (j + 1), width = 6)
              # Les cloisons verticales
              if grille[j][i] & 4: can.create_line(3 + cote*(i), 1 + cote*(j + 1), 3 + + cote*(i + 1), 2 + + cote*(j + 1), width = 6)

def Switch():
    global rbtCourant
    if rbtCourant == robot1:
        rbtCourant = robot2
        boutonSwitch.config(font=('courrier',12,'bold'), bg = 'blue')
    elif rbtCourant == robot2:
        rbtCourant = robot3
        boutonSwitch.config(font=('courrier',12,'bold'), bg = 'red')
    else:
        rbtCourant = robot1
        boutonSwitch.config(font=('courrier',12,'bold'), bg = 'green')
        
    
        
fen=Tk()
Width = 1200
Heigth= 850

hauteurJeu = 9
largeurJeu = 9

fen.title('Plateau')
generation()

robot1 = Robot(0,3, 'green')
robot2 = Robot(2,3, 'blue')
robot3 = Robot(5,6, 'red')
rbtCourant = robot1

boutonQuitter=Button(fen,text='Quitter',command=fen.quit,bd=10,padx=14)
boutonQuitter.config(font=('courrier',12,'bold'))
boutonSouth=Button(fen,text='South',command=lambda: Robot.move(rbtCourant, "S"),bd=10,padx=14)
boutonSouth.config(font=('courrier',12,'bold'))
boutonNorth=Button(fen,text='North',command= lambda: Robot.move(rbtCourant, "N"),bd=10,padx=14)
boutonNorth.config(font=('courrier',12,'bold'))
boutonEast=Button(fen,text='East',command=lambda: Robot.move(rbtCourant, "E"),bd=10,padx=14)
boutonEast.config(font=('courrier',12,'bold'))
boutonWest=Button(fen,text='West',command=lambda: Robot.move(rbtCourant, "W"),bd=10,padx=14)
boutonWest.config(font=('courrier',12,'bold'))
boutonSwitch=Button(fen,text='Switch',command=Switch,bd=10,padx=14)
boutonSwitch.config(font=('courrier',12,'bold'), bg = 'green')


space=Label(fen)
space.grid(row=5,column=1,pady=188)
boutonQuitter.grid(row=7,column=1,sticky=S)
boutonSouth.grid(row=6,column=1,sticky=S)
boutonNorth.grid(row=5,column=1,sticky=S)
boutonEast.grid(row=4,column=1,sticky=S)
boutonWest.grid(row=3,column=1,sticky=S)
boutonSwitch.grid(row=2,column=1,sticky=S)
fen.mainloop()

fen.destroy()






