#Importation des librairies

import pygame,os,sys,time
from structures.genome import Genome
from random import choice
from structures.allele import Allele
from structures.individu import Individu
from structures.environnement import Biome, WorldMap
from structures.livings import Livings

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

font = pygame.font.SysFont("Arial", 18)
world = WorldMap(W, H)

# On "Peint" le monde avec des rectangles (Tes zones)
# args : nom, x, y, largeur, hauteur
world.add_zone("plaine", 50, 50, 400, 300)      # Gros continent
world.add_zone("foret",  100, 100, 150, 150)    # Forêt DANS la plaine
world.add_zone("desert", 500, 200, 200, 300)    # Désert à droite
world.add_zone("montagne", 600, 250, 80, 80)    # Montagne DANS le désert

#Création de grenouille
Population = Livings()
Froggy = Individu(400, 300, 30)  # position + taille
Froggy.craft_individu()
Population.add_individu(Froggy)
grenouilles = [Individu(100, 100, 40), 
               Individu(200, 150, 30), 
               Individu(300, 250, 40), 
               Individu(400, 350, 35)]
for g in grenouilles:
        g.craft_individu()
        Population.add_individu(g)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            temp, hum, nom = world.get_infos_at(mx, my)
            print(f"Zone: {nom.upper()} | Temp: {temp}°C | Hum: {hum}%")

    # 2. Dessin
    world.paint(screen)
    
    # (Optionnel) Afficher le climat sous la souris en temps réel
    mx, my = pygame.mouse.get_pos()
    temp, hum, nom = world.get_infos_at(mx, my)
    text_surf = font.render(f"{nom}: {temp}°C / {hum}%", True, (0, 0, 0))
    screen.blit(text_surf, (mx + 10, my + 10))
    
    # on dessine la grenouille =)
    for g in Population.populations:
        g.draw(screen)
        g.deplacement()
        
    Population.update(W,H)

    time.sleep(0.2)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()