from enum import Enum
class RColors(Enum) :
 
   # BLACK = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4

    def __str__(self) :
        """ renvoie une représentation sous forme de chaine de la couleur"""
        return color_names[self]

    @classmethod
    def from_str(cls , string) : 
        """ renvoie un objet RColors correspondant àstring 
        string doit être un élément de ["R","G","B","Y"]
        """
        assert string in color_by_name
        return color_by_name[string]

color_names = {
                    RColors.RED : 'R',
                    RColors.BLUE : 'B',
                    RColors.YELLOW :'Y',
                    RColors.GREEN : 'G'}
                    
color_by_name = {     'R' : RColors.RED,
                      'B' : RColors.BLUE,
                      'Y' : RColors.YELLOW,
                      'G' : RColors.GREEN}
