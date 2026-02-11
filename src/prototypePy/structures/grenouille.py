# LA GRENOUILLE DES TESTS
# python3 src/prototypePy/structures/grenouille.py
import pygame
from individu import Individu
import time


pygame.init()
# Setup écran
info = pygame.display.Info()
W, H = info.current_w, info.current_h
# Pour tester sans être en plein écran total bloquant :
screen = pygame.display.set_mode((W, H),pygame.RESIZABLE) 
pygame.display.set_caption("NomQuiClaque | La Simulation")

# Initialisation du framerate pour egaliser la vitesse de jeu sur toutes les machines
framerate = 60
clock = pygame.time.Clock()
dt = clock.tick(framerate)

Froggy = Individu(400, 300, 30)  # position + taille
Froggy.craft_individu()
grenouilles = [Individu(100, 100, 40), 
               Individu(200, 150, 30), 
               Individu(300, 250, 40), 
               Individu(400, 350, 35)]
for g in grenouilles:
        g.craft_individu()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((50, 50, 50))  # fond gris
    Froggy.draw(screen)        # on dessine la grenouille =)
    Froggy.deplacement()
    for g in grenouilles:
        g.draw(screen)
        g.deplacement()
    
    time.sleep(0.2)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
