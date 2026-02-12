import pygame
from genome import Genome
from random import choice
from allele import Allele
from individu import Individu



class Livings:
    def __init__(self):
        self.populations = []

    def add_individu(self,individu):
        self.populations.append(individu)
    
    def reproduction(self, individu1, individu2):
        new_genome = Genome()

        for allele1, allele2 in zip(individu1.genome.alleles, individu2.genome.alleles):
            parent_allele = choice([allele1, allele2]) # choisir l'allèle du parent 1 ou 2

            new_allele = Allele(parent_allele.nom, 
                                parent_allele.al_type, 
                                parent_allele.req, 
                                parent_allele.valeur, 
                                parent_allele.mutation_rate, 
                                parent_allele.mutation_step )
            new_genome.add_allele(new_allele)

        # Position du bébé entre les parents ça marche pas trop
        x = (individu1.rect.x + individu2.rect.x) // 2
        y = (individu1.rect.y + individu2.rect.y) // 2

        bébé = Individu(x, y, new_genome) # Création du nouvel individu
        self.populations.append(bébé) # Ajout à la population
        return bébé