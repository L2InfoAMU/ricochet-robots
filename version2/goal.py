"""
la classe Goal permet de créer des objets pour l'objectif du jeu.
Un objectif est la donnée d'une couleur et d'une position
    goal = Goal(RColors.GREEN, (0,4))

    On accède aux champs par :
    goal.color
    goal.position
"""
class Goal :
    def __init__(self, color, position) :
        """ initialisation d'un objet Goal """
        self.color = color
        self.position = position

    def __str__(self) :
        """ renvoie une chaîne de caractère décrivant l'objectif du jeu 
        La chaîne est de la forme :
        '"goal" : { "color" : "R",
            "position" : [x,y]
            }
        """
        string = '"goal" : { "color" : "' + str(self.color)+'"'
        string +=  ',\n\t"position" :' + str(list(self.position))
        string += '\n\t}'
        return string