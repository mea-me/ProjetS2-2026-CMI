class Allele:
    def __init__(self, al_type:str, req:bool, nom:str, valeur,  mutation_rate:int, mutation_step:int):
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

    def __repr__(self):
        # formater le print
        return f"[{self.nom}: {self.valeur}]" 
    

######### Allèles de base

dico_alleles = {
    # "nom" : ["description", "type", is required True/False],
    "vitesse" : ["La vitesse de déplacement de l'individu (0-100)", "int", True],
    "masse" : ["La masse de l'individu (0-100)", "int", True],
    "taille" : ["La taille de l'individu (0-100)", "int", True],
    "régime" : ["Le régime alimentaire de l'individu (carnivore, omnivore, herbivore)", "str", True],
    "couleur" : ["La couleur de l'individu (RGB)", "list", True]
}

