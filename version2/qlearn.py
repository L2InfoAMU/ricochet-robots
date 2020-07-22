
""" Projet Maths Info pour le DU CCIE et la L3 Maths-Info
Chef de projet : CANALS Martin L3
Développeurs : AUBIN François DU CCIE, GIANI Théo L3

Module pour l'apprentissage par Q_learning'

"""
from robot import Game

class Q_learner :

    def __init__(self , game:Game) :
        self.game = game

    def learn(self) :

        # define the states 
        actions = self.game.actions_list()

