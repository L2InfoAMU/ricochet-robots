from stateencoder import StateEncoder
from game import Game
from numpy import array, zeros


class Qlearner :

    def __init__(self, game) :
        self.game = game
        self.actions = self.game.actions_list()
        self.encoder = StateEncoder(self.game)
        self.state_number = self.encoder.state_number

        self.state_to_int, self.int_to_state = self.encoder.state_index_function()
        self.action_number = len(self.actions)
        self.qtable = zeros( (self.state_number,self.action_number),dtype = float)


    def reward_function(self) :
        """ 
        Cette methode renvoie la fonction qui calcule la récompense liée à une action
        """
        game = self.game
        actions = self.actions
        encoder, decoder = self.state_to_int, self.int_to_state 

        def reward(state_index, action_index) :
            """ 
            récompense liée à une action
            Si l'action ne fait pas changer d'état la récompense est -1
            Si l'action fait aboutir à un état final la récompense est 1
            Sino la récompense est 0
            """

            state = self.int_to_state(state_index)


