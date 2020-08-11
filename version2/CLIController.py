# -*- coding : utf-8 -*-

""" Projet Maths Info pour le DU CCIE et la L3 Maths-Info
Chef de projet : CANALS Martin L3
Développeurs : AUBIN François DU CCIE, GIANI Théo L3

"""


from robot import*
from random import *


rejouer = True
while rejouer :
    number_grid = input("Sur quelle grille voulez-vous jouer ? (entrez un numéro entre 1 et 4)")
    name_grid = './test' + number_grid + '.txt'
    fd = open(name_grid,'r')
    A = Board.load_from_file(fd)
    group = Robot_group()
    nb_robots = int(input("Combien de robots voulez-vous installer? (max 4 plz)"))
    placement_aleatoire = not(input("Voulez-vous placer les robots vous-même? (sinon on s'en charge) oui/non") in ["oui", "o"])
    robots_pos = [0] * nb_robots
    robots_list = [0] * nb_robots
    robots_colors = [i for i in RColors]

    if placement_aleatoire:

        for i in range(nb_robots):
            x = randint(0, A.width - 1)
            y = randint(0, A.height - 1)
            while ((x, y) in robots_pos):
                x = randint(0, A.width - 1)
                y = randint(0, A.height - 1)
            robots_pos[i] = (x,y)
            robots_list[i] = Robot(group, robots_colors[i], (x, y))

        x = randint(0, A.width - 1)
        y = randint(0, A.height - 1)

        goal = Goal(RColors(randint(0, nb_robots - 1)), (x, y))
    else :
        for i in range(nb_robots):
            print("entrez les coordonnées du robot sous la forme (x, y)")
            x, y = tuple(map(int,input().split()))
            while ((x, y) in robots_pos):
                print("attention, il y a déjà un robot ici !")
                x, y = tuple(map(int, input().split()))
            robots_pos[i] = (x, y)
            robots_list[i] = Robot(group, robots_colors[i], (x, y))
        num_robot = int(input("Quel est le numero de la couleur du robot choisi ? 1 : RED 2 : BLUE 3 : GREEN 4 : YELLOW  ? "))

        print("entrez les coordonnées du but sous la forme (x, y)")
        x, y=tuple(map(int, input().split()))
        goal = Goal(RColors(num_robot), (x, y))
    game=Game(A, group, goal)

    print("C'est parti !")
    for i in range(nb_robots):
        print(robots_list[i])
    initial_state = game.get_state()
    print("etat initial :")
    print(initial_state)
    print("le robot ", game.color_names[goal.color],
          " doit aller au point ", goal.position)

    number_moves = 0

    while (not game.is_won()):
        action = input("Entrez un déplacement sous la forme couleur/direction, par exemple RN ou YE ou BW (ou tapez undo pour annuler le dernier coup, ou rejouer pour remettre l'état initial):  ")
        if action == "undo":
            game.undo()
            number_moves -= 1
        elif action =="rejouer":
            game.set_state(initial_state)
            numer_moves = 0
        else:
            game.do_action(action)
            number_moves += 1
        print(game.get_state())
    print("Bravo ! Vous avez gagné en ", number_moves , "coups.")


    rejouer = not(input("Voulez-vous rejouer? (oui/non)") in ["oui", "o"])
