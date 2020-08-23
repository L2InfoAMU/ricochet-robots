
""" Projet Maths Info pour le DU CCIE et la L3 Maths-Info
Chef de projet : CANALS Martin L3
Développeurs : AUBIN François DU CCIE, GIANI Théo L3

Fichier stateencoder.py
La classe StateEncoder 
- détermine le nombre d'états du jeu
- propose un encodage des états en un entier naturel
- propose le décodage correspondant

Le codage est basé sur le nombre de cases de la grille
size = height * width
Le codage d'un état est le suivant :
Les positions (x1,y1), (x2,y2), (x3,y3)... des robots 
sont converties en entiers naturels
n1 = x1 * width + y1 , n2 = x2 *width + y2 ...

L'index est calculé par

index = n1 * (size-1)! + 
"""


def arrangement(n,p) :
    a = 1
    for i in range(p):
        a = a*(n-i)
    return a

class StateEncoder :

    def __init__(self , game) :
        self.game = game
        size = self.game.board.width*self.game.board.height
        nr = len(self.game.robots)
        self.state_number = arrangement(size,nr)

    def position_encoder_functions(self) :
        width = self.game.board.width

        def position_to_int( position) :
            x ,y = position
            return x * width + y

        def int_to_position( index) :
            return (index // width, index%width)

        return position_to_int, int_to_position
          
    def state_index_function(self) :

        s = len(self.game.robots)
        size = self.game.board.height*self.game.board.width
        
        pos2int, int2pos = self.position_encoder_functions()
        arrangements = [ arrangement(size-i-1,s-i-1) for i in range(s)]
        def encoder(state) : 
            index = 0        
            integers = [pos2int( pos) for pos in state]
            for  i in range(s) :
                x_i = integers[i]
                minus = 0
                for j in range(i) :
                    if integers[j] < x_i : minus += 1
                x_i -= minus
                index += x_i * arrangements[i]
            
            return index
            
        def decoder(index) :
            
            indexes = []
            
            for i in range(s) :
                digits = [j for j in indexes]
                digits.sort()
                x_i, index  = index// arrangements[i] , index%arrangements[i]
               

                for j in range(i) :
                    if digits[j] <= x_i : x_i +=1
                
                indexes.append(x_i)
            
            positions = [int2pos(x_i) for x_i in indexes]
            return tuple(positions)

        return encoder, decoder


    