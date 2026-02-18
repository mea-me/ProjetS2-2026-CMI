class Allele:
    def __init__(self, nom:str, al_type:str, req:bool,  valeur,  mutation_rate:int, mutation_step:int,tipe:str,):
        """
        :param al_type: Le type du gène comportement ou physique (ex: C / P)
        :param req: Si l'allèle est obligatoire (basique) ou pas (ex : vitesse)
        :param nom: Le nom du gène (ex: "vitesse")
        :param valeur_base: La valeur numérique (ex: 50) ou booléenne 
        :param mutation_rate: Chance de muter à chaque génération (en %)
        :param mutation_step: De combien ça change si ça mute (ex: +/- 2)
        """
        self.al_type = al_type
        self.req = req
        self.nom = nom
        self.valeur = valeur
        self.mutation_rate = mutation_rate
        self.mutation_step = mutation_step
        self.type = tipe

    def __repr__(self):
        # formater le print
        return f"[{self.nom}: {self.valeur}]" 
    

######### Allèles de base

dico_alleles = {
    #           0        1     2                3          4        5
    # "nom" : [al_type, req, valeur (écart), mutStep, description, type]
    "vitesse" : ["P",True,(5,50), (1, 5), "La vitesse de déplacement de l'individu (0-100)", "int"],
    "masse" : ["P",True,(3,75), (1, 5), "La masse de l'individu (0-100)", "int"],
    "taille" : ["P",True,(20,75), (1, 5), "La taille de l'individu (0-100)", "int"],
    "régime" : ["P", True, ["carnivore", "herbivore", "omnivore"], None, "Le régime alimentaire de l'individu (carnivore ou omnivore ou herbivore)", "str"],
    "couleur" : ["P",True,"couleur pas accéder", (1, 25), "La couleur de l'individu (RGB)", "list"],
    "agilité" : ["P",True,(0,100), (1, 5), "L'agilité de l'individu (résistance au terrain escarpé)", "int"],

    # climatoseptikPoP
    "température" : ["P",True,(-20,40), (1, 3), "La vitesse de déplacement de l'individu (0-100)", "int"],
    "humidité" : ["P",True,(0,100), (1, 5), "La vitesse de déplacement de l'individu (0-100)", "int"],
 
    "aggréssivité" : ["C",True,(0,75), (1, 5), "Le taux d'aggresivité de l'individu (0-100)", "int", True],
    "fertilité" : ["C",True,(0,75), (1, 5), "Le taux de fertilité de l'individu (0-100)", "int", True],
    "adaptabilité" : ["C",True,(0,75), (1, 5), "Le taux d'adaptabilité de l'individu (0-100)", "int", True],
    "perception" : ["C",True,(0,75), (1, 5), "La distance à laquelle il peut voir", "int", True]
}

