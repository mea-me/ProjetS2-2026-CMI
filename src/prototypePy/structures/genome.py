from random import randint
from allele import Allele

class Genome:
    def __init__(self):
        self.alleles = [] # liste d'objets Allele

    def add_allele(self, allele):
        self.alleles.append(allele)

    def get_val(self, nom_allele):
        #  récupérer une valeur par son nom d'allele
        for a in self.alleles:
            if a.nom == nom_allele:
                return a.valeur
        return 1 # code d'erreur si echec

    def muter(self):
        """Applique potentiellement une mutation (sur chaque allèle)"""
        for gene in self.alleles:
            if isinstance(gene.valeur, int) and randint(1, 99) < gene.mutation_rate:  # si mutation

                gene.valeur += randint(-gene.mutation_step, gene.mutation_step)
                
                if gene.valeur < 0: 
                    gene.valeur = 0 # borne anti négative (genre vitesse négative pas possible)

    def __repr__(self):
        # formater le print
        li = ""
        for a in self.alleles :
            li += f'{str(a)}; '
        return f'Genome({li[:-2]})'

# ali = Genome()
# a1, a2, a3  = Allele('C', True, 'Abby', 1, 22, 343), Allele('P', True, 'Bobby', 31, 98, 1), Allele('C', True, 'Coby', 321, 3, 32)
# ali.add_allele(a1)
# ali.add_allele(a2)
# ali.add_allele(a3)
# 
# print(ali)
# ali.muter()
# print(ali)