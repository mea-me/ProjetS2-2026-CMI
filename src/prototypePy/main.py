#Importation des librairies

import pygame

#Initialisation de Pygame
pygame.init()

#Définition de la taille de la fenêtre du jeu
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
playHeight = screen_height -  (1/5 * screen_height)
screen = pygame.display.set_mode((screen_width, screen_height))

# Initialisation du framerate pour egaliser la vitesse de jeu sur toutes les machines
framerate = 60
clock = pygame.time.Clock()
dt = clock.tick(framerate)


pygame.quit()