import copy

class Individual:       # class qui va probablment beauuucoup changer
    def __init__(self, genome_parent):
        self.age = 0
        self.energie = 100 # Par défaut
        self.is_alive = True
        
        # On fait une COPIE pour qu'il ait ses propres gènes
        self.genome = copy.deepcopy(genome_parent)
        
        # calc des stats max basées sur l'ADN
        self.max_vitesse = self.genome.get_val("vitesse")
        self.max_size = self.genome.get_val("taille")              # c'est juste pour l'idée
        self.sense_radius = self.genome.get_val("perception")      # faut réfléchir a comment le faire

    def update(self):
        # c'est ça qu'on fera a chaque 'tick' de la clock pygame
        self.age += 1
        self.energie -= 0.1 * self.max_size # Plus on est gros, plus on consomme
        
        if self.energie <= 0:
            self.is_alive = False #bleurgh

    def __repr__(self):
        # formater le print
        return f"Indiv(T:{self.taille} | E:{self.energie} | V:{self.max_vitesse})"  # la aussi c'est une idée 