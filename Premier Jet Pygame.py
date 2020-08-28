# -*- coding: utf-8 -*-


import pygame


class Grille :

    dimensionGrille = 6
    # On indique les positions des murs sur chaque ligne/colonne, en partant du coin supérieur gauche.
#    mursVerticaux = [[0, 2, 6] , [0, 1, 5, 6], [0, 6], [0, 2, 6], [0, 6], [0, 3, 6] ]
#    mursHorizontaux = [ [0, 6] , [0, 2, 6] , [0, 6], [0, 6], [0, 1, 4, 6], [0, 5, 6] ]

#ou alors on dessine carrément les murs, pour séparer les problèmes
    #MurHorizontaux est codé ligne par ligne
    mursHorizontaux2 = [['-', '-', '-', '-', '-', '-'],
                        [' ', ' ', ' ', ' ', '-', ' '],
                        [' ', '-', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', '-', ' '],
                        [' ', ' ', ' ', ' ', ' ', '-'],
                        ['-', '-', '-', '-', '-', '-']]

    #MursVerticaux2 est codé colonne par colonne
    mursVerticaux2 =    [['|', '|', '|', '|', '|', '|'],
                        [' ', '|', ' ', ' ', ' ', ' '],
                        ['|', ' ', ' ', '|', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', '|'],
                        [' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', '|', ' ', ' ', ' ', ' '],
                        ['|', '|', '|', '|', '|', '|']]

    positionsDesRobots = {}


class Robot :

    def __init__(self, x , y, name): #la case de coordonnées (1,1) est en haut à gauche
        self.x = x
        self.y = y
        self.name = name
        Grille.positionsDesRobots[self.name] = (x, y)

    def move(self, direction):
        while "on peut avancer":
            if direction == 'Nord':
                caseDevant = (self.x, self.y - 1)
                murDevant = Grille.mursHorizontaux2[self.y - 1][self.x - 1] == '-'
            elif direction == 'Sud':
                caseDevant = (self.x, self.y + 1)
                murDevant = Grille.mursHorizontaux2[self.y ][self.x - 1] == '-'
            elif direction == 'Ouest':
                caseDevant = (self.x - 1, self.y)
                murDevant = Grille.mursVerticaux2[self.x - 1][self.y - 1] == '|'
            elif direction =='Est':
                caseDevant = (self.x + 1, self.y)
                murDevant = Grille.mursVerticaux2[self.x ][self.y - 1] == '|'
            if caseDevant not in Grille.positionsDesRobots.values() and not murDevant:
                self.x = caseDevant[0]
                self.y = caseDevant[1]
                Grille.positionsDesRobots[self.name] = (self.x, self.y)
                print("je suis le robot " + self.name + " à la position" , self.x , " ",  self.y)
            else:
                break


choixTest = int(input('Entrez le numéro du test à effectuer ( \n1 : ordinateur\n2 : vous-même \n3 : graphique \n'))
if choixTest == 1:
    r1 = Robot(4,6,'r1')
    r2 = Robot(5,2,'r2')
    r1.move('Nord')
    r1.move('Est')
    r1.move('Sud')
    r2.move('Sud')
    r2.move('Ouest')
    r2.move('Nord')
    r2.move('Est')
    r2.move('Sud')
    r2.move('Ouest')
    print(Grille.positionsDesRobots)

elif choixTest == 2:
    print("Entrez les coordonnées du robot 1 et son nom, sous la forme x y nom")
    saisie = input().split()
    r1 = Robot(int(saisie[0]), int(saisie[1]), saisie[2])
    print("Faites de même pour le robot 2")
    saisie = input().split()
    r2 = Robot(int(saisie[0]), int(saisie[1]), saisie[2])
    print('Entrez une suite de de déplacements des robots, sous la forme nom, direction. Entrez 0,0 pour arrêter')
    test = tuple(input().split(','))
    print(test[0])
    print(test[1])
    while test != (0,0):
        if test[0] == r1.name:
            r1.move(test[1])
        elif test[0] == r2.name:
            r2.move(test[1])
        test = tuple(input().split(','))
elif choixTest == 3:
    r1 = Robot(4, 6, 'r1')
    r2 = Robot(5, 4, 'r2')

pygame.init()
fenetre = pygame.display.set_mode((640,640))
pygame.display.set_caption("Ricochet Robot - étape 1")
fond = pygame.image.load("fond.jpg")
fond2 = pygame.transform.scale(fond, (640, 640))
fenetre.blit(fond2, (0,0))


robot1 = pygame.image.load("robot bleu.png")
rob1 = pygame.transform.scale(robot1, (76, 100))
robot2 = pygame.image.load("robot rouge.png")
rob2 = pygame.transform.scale(robot2, (76, 100))
fenetre.blit(rob1, (640 * r1.x / 6 - 640/6,640 * r1.y / 6- 640/6))
fenetre.blit(rob2, (640 * r2.x / 6- 640/6,640 * r2.y / 6- 640/6))

police = pygame.font.Font(None, 28)
texte1 = police.render("Tapez 1 ou 2 pour sélectionner le robot actif (1 par défaut), ", 1, (0,0,255))
texte2 = police.render("puis utilisez les flèches du clavier pour les déplacements", 1, (0,0,255))
texte3 = police.render("Appuyez sur echap pour fermer la fenêtre", 1, (0,0,255))
fenetre.blit(texte1, (20, 120))
fenetre.blit(texte2, (20, 160))
fenetre.blit(texte3, (20, 200))

robotActif = r1
pygame.display.flip()

continuer = True

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP1:
                robotActif = r1
            if event.key == pygame.K_KP2:
                robotActif = r2
            if event.key == pygame.K_UP:
                robotActif.move('Nord')
            if event.key == pygame.K_DOWN:
                robotActif.move('Sud')
            if event.key == pygame.K_RIGHT:
                robotActif.move('Est')
            if event.key == pygame.K_LEFT:
                robotActif.move('Ouest')
            if event.key == pygame.K_ESCAPE:
                continuer = False
    fenetre.blit(fond2, (0, 0))
    fenetre.blit(rob1, (620 * r1.x / 6 - 90, 620 * r1.y / 6 - 100))
    fenetre.blit(rob2, (620 * r2.x / 6 - 90, 620 * r2.y / 6 - 100))
    pygame.display.flip()

pygame.quit()
