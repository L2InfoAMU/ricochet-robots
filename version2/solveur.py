""" Projet Maths Info pour le DU CCIE et la L3 Maths-Info
Chef de projet : CANALS Martin L3
Développeurs : AUBIN François DU CCIE, GIANI Théo L3

Module pour la recherche d'une solution par exploration du graphe en largeur

"""
from collections import deque 


class solveur :

    def __init__(self, game) :
        self.game = game

    @staticmethod
    def action_sequence_from_pred(pred, final_state) :
        action_sequence = deque()

        state = final_state
        while state is not None :
            state , action = pred[state]
            action_sequence.appendleft(action)
        return list(action_sequence)

    def find_solution(self) :


        actions = self.game.actions_list()
        queue = deque()
        empty_queue = deque()
        graph = set()
        pred = dict()

        initial_state = self.game.get_state()
        graph.add(initial_state)
        queue.append(initial_state)
        pred[initial_state]= (None , None)
        while queue != empty_queue :
            state = queue.popleft()
            for action in actions :
                self.game.set_state(state)
                result_state = self.game.do_action(action)
                if result_state not in graph :
                    graph.add(result_state) 
                    pred[result_state] =(state,action)
                    if self.game.state_is_won(result_state) :
                        return solveur.action_sequence_from_pred(pred,result_state)
                    queue.append(result_state)
        


    