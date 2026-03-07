#Importation des librairies

import pygame,os,sys,time
from structures.genome import Genome
from random import choice
from structures.allele import Allele
from structures.individu import Individu
from structures.environnement import Biome, WorldMap
from structures.livings import Livings, Espece, Population

#Initialisation de Pygame
pygame.init()


# Setup écran
info = pygame.display.Info()
W, H = info.current_w, info.current_h
# Pour tester sans être en plein écran total bloquant :
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE) 
pygame.display.set_caption("NeoRiza | Simulateur d’Évolution Biologique")

# Initialisation du framerate pour egaliser la vitesse de jeu sur toutes les machines
framerate = 60
clock = pygame.time.Clock()
dt = clock.tick(framerate)
age = 0

font = pygame.font.SysFont("Arial", 18)
world = WorldMap(W, H)

# On "Peint" le monde avec des rectangles (Tes zones)
# args : nom, x, y, largeur, hauteur
world.add_zone("plaine", 50, 50, 400, 300)      # Gros continent
world.add_zone("foret",  100, 100, 150, 150)    # Forêt DANS la plaine
world.add_zone("desert", 500, 200, 200, 300)    # Désert à droite
world.add_zone("montagne", 600, 250, 80, 80)   