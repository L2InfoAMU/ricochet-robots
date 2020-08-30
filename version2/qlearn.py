from stateencoder import StateEncoder
from game import Game
from numpy import array, zeros
from random import randint,choice


class Qlearner :

    def __init__(self, game) :
        self.game = game
        self.actions = self.game.actions_list()
        self.encoder = StateEncoder(self.game)
        self.state_number = self.encoder.state_number

        self.state_to_int, self.int_to_state = self.encoder.state_index_function()
        self.action_number = len(self.actions)
        self.qtable = zeros( (self.state_number,self.action_number),dtype = float)


    def reward(self, state, action) :
        """ 
            récompense liée à une action
            Si l'action ne fait pas changer d'état la récompense est -1
            Si l'action fait aboutir à un état final la récompense est 1
            Sinon la récompense est 0
            Après l'appel de cette fonction le jeu est dans le nouvel etat 
        """
      
        self.game.set_state(state)
        new_state = self.game.do_action(action)
        if new_state == state : return -1 ,new_state
        if game.state_is_won(new_state) : return 1 ,new_state
        return 0 ,new_state

    def  learn(self, nb_iter, mu = 0.9) :
        
        for _ in range(nb_iter) :
            state_index = randint(0,self.state_number-1)
            state = self.int_to_state(state_index)
            action = choice(self.actions)

            immediate_reward ,new_state= self.reward(state,action)
            new_state_index = self.state_to_int(new_state)
            delay_reward = mu * max( self.qtable[new_state_index,:])

            self.qtable[state_index] = immediate_reward + delay_reward


game = Game.load_from_json("games/game2x2.json")
learner = Qlearner(game)
learner.learn(100)









