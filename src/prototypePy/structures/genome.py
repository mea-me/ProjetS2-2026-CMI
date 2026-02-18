from random import randint,choice
from .allele import Allele, dico_alleles
import copy

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
                
                if gene.valeur < 1: 
                    gene.valeur = 1 # borne anti négative (genre vitesse négative pas possible)

            elif isinstance(gene.valeur, list) and randint(1, 99) < gene.mutation_rate:
                for i in range(len(gene.valeur)):
                    gene.valeur[i] += randint(-gene.mutation_step, gene.mutation_step)
                
                    if gene.valeur[i] < 0: 
                        gene.valeur[i] += 255 # borne anti négative (genre vitesse négative pas possible)

                    elif gene.valeur[i] > 255: 
                        gene.valeur[i] -= 255 # borne anti positron (genre vitesse négative pas possible)

    def __repr__(self):
        # formater le print
        li = ""
        for a in self.alleles :
            li += f'{str(a)};\n '
        return f'Genome({li[:-2]})'
    
    def craft_alleles(self):
        for key,value in dico_alleles.items():
            if value[1]:
                if value[5] == "int":
                    self.add_allele(Allele(key,value[0],True,randint(value[2][0],value[2][1]),randint(0,100),randint(value[3][0],value[3][1]),value[5]))

                if value[5] == "str":
                    self.add_allele(Allele(key,value[0],True,choice(value[2]),randint(0,100),value[3],value[5]))
                    
                if key == "couleur":
                    self.add_allele(Allele("couleur","P",True,[randint(0,255),randint(0,255),randint(0,255)],randint(0,100),randint(value[3][0],value[3][1]),value[5]))

    def show_alleles(self):
        for i in self.alleles:
            for y in i:
                print(y)
                
    def clone(self):
        return copy.deepcopy(self)