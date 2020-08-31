from stateencoder import StateEncoder
from game import Game
from numpy import array, zeros
from random import randint,choice, random
from math import inf

def indices_max(data) :
    """ renvoie la liste des indices des maximaix dans le tableau data
    exemples indices_max([0,0,2,1,2]) renvoie [2,4] 
    """
    max = -inf
    indices=[]

    for i in range(len(data)) :
        if data[i] > max :
            max = data[i]
            indices = [i]
        elif data[i] == max :
            indices.append(i)
    
    return indices

class Qlearner :

    def __init__(self, game) :
        """ construit un apprenant pour le jeu game 
        """

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

    def  learn(self, nb_iter, mu = 0.9, c = 1 ,explore = 1 ) :
        """ apprend la Qtable en simulant nb_iter épisodes de jeu
        mu est le facteur de récompense retardée
        c le facteur d'apprentissage qui peut varier entre 0 et 1
        c = 0 , l'agent n'apprend rien, 
        c = 1 , l'agent met à jour complétement la valeur de Q (voir rapport)

        explore est le facteur d'exploration qui peut varier entre 0 et 1 :
        explore = 0  : l'agent choisit l'action à partir de la meilleure récompense dans la table
        explore = 1 : l'agent explore en choisissant toutes ses actions au hasard
        """
        for _ in range(nb_iter) :
            state_index = randint(0,self.state_number-1)
            state = self.int_to_state(state_index)

            # choix de l'action
            # On fait de l'exploration avec une probabilité  égale à explore
            if random() < explore : 
                # choix aléatoire d'une action
                action_index = randint(0,len (self.actions)-1)

            else : # exploitation
                indices = indices_max( self.qtable[state_index,:])
                action_index = choice(indices)

                
            action = self.actions[action_index]

            immediate_reward ,new_state= self.reward(state,action)
            if immediate_reward == 1  :
                delay_reward = 0
            else :
                new_state_index = self.state_to_int(new_state)
                delay_reward = mu * max( self.qtable[new_state_index,:])

            self.qtable[state_index,action_index] = (1-c) *self.qtable[state_index,action_index] + c* (immediate_reward + delay_reward)



game = Game.load_from_json("games/game2x2.json")
learner = Qlearner(game)
learner.learn(1000)
print (learner.qtable)









