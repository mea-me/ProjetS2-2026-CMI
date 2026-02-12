import pygame
from genome import Genome
from random import choice
from allele import Allele
from individu import Individu

pygame.init()

screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height))

surface = pygame.PixelArray(screen)

del surface # -> pas possible de mettre à jour 
          # le display si surface active

pygame.display.flip()

red = pygame.Color.r

def add_zone(h, w):
    pygame.draw.rect(surface, red, h, w)


class Biome:
    def __init__(self, nom, temperature, humidite, x, y):
        # width et height sont la taille de l'objet
        self.nom = nom
        self.temperature = temperature
        self.humidite = humidite
        self.x = x
        self.y = y

    def draw_biome(self, screen, color, taille): #color qui peut devenir image
        pygame.draw.rect(screen, color, (self.x, self.y), taille) #taille = rayon

    def contains(self, individu): # test si il a un individu dedans 
        return self.rect.collidepoint(individu.x, individu.y)
    
    def __repr__(self): 
        return f"{self.nom} (T={self.temperature}, H={self.humidite})"


dico_biomes = {
    # nom : [temperature, humidite]
    "foret" :   [25, 80],
    "plaine" :  [15, 30],
    "ocean" :   [10, 100],
    "desert" :  [40, 0],
    "montagne": [-5,20],
    "neige" :   [-20,60]
}


class WorldMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.individus = [] #liste des individus
        self.biomes = [] # liste d'objets Biome
        self.background_biome = "plaine"

    def get_biome_at(self, x, y):
        for b in reversed(self.biomes):
            if b.contains(x,y):
                return b.nom

    def get_climate_at(self, x, y):
        # On cherche de la dernière zone ajoutée vers la première
        for b in reversed(self.biomes):
            if b.contains(x, y):
                return b.temperature, b.humidite
        
        # Si aucun biome trouvé, c'est le fond
        bg = dico_biomes[self.background_biome]
        return bg.temperature, bg.humidite
    
    def paint(self, surface):
        # Fond
        bg_color = dico_biomes[self.background_biome]
        surface.fill(bg_color)

        # Zones (les dernières ajoutées sont au dessus)
        for b in self.biomes:
            color = b.biome.color
            pygame.draw.rect(surface, color, (b.x, b.y))

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
        self.individus.append(bébé) # Ajout à la population
        return bébé
