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

# génération de la map procédurale
world.procedural_generation(80)

#Création de grenouille-----------------------------------------------------------------
Froggy = Individu(400, 300,0)  # position + taille
Froggy.craft_individu()
Froggy.give_rect(Froggy.genome.get_val("taille"))

Population.add_individu(Froggy)
grenouilles = [Individu(300, 100,0), 
               Individu(200, 100,0), 
               Individu(300, 100,0), 
               Individu(200, 100,0)]
for g in grenouilles:
        g.craft_individu()
        g.give_rect(g.genome.get_val("taille"))
        Population.add_individu(g)


grenouille = Espece(0,0)
#--------------------------------------------------------------------------------------- 

paused = False        
running = True

mask_surface = pygame.Surface((W, H), pygame.SRCALPHA) # -> SRCALPHA = transparent
mask_surface.fill((0, 0, 0, 0)) # no no zone

overlay = pygame.Surface((W, H), pygame.SRCALPHA)
overlay.fill((0, 0, 0, 255)) # ca c'est pour qu'on puisse voir le tour de l'ellipse

playable_rect = pygame.Rect(20, 20, W - 40, H - 40)
pygame.draw.ellipse(mask_surface, (255, 255, 255, 255), playable_rect)
pygame.draw.ellipse(overlay, (0, 0, 0, 0), playable_rect)

allowed_mask = pygame.mask.from_surface(mask_surface)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN: #mettre en pause appuyant sur entré
            if event.key == pygame.K_RETURN:
                paused = not(paused)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            temp, hum, nom = world.get_infos_at(mx, my)
            print(f"Zone: {nom.upper()} | Temp: {temp}°C | Hum: {hum}%")

    if paused:
        continue                
    else:
        # 2. Dessin
        world.paint(screen)
        
        # (Optionnel) Afficher le climat sous la souris en temps réel
        #mx, my = pygame.mouse.get_pos()
        #temp, hum, nom = world.get_infos_at(mx, my)
        #text_surf = font.render(f"{nom}: {temp}°C / {hum}%", True, (0, 0, 0))
        #screen.blit(text_surf, (mx + 10, my + 10))

        # on dessine la grenouille =)
        for g in Population.populations:
            g.draw(screen)
            g.deplacement(allowed_mask)

        screen.blit(overlay, (0, 0))
            
        Population.update(W,H,world)

        # infos
        fps = round(clock.get_fps(),2)
        fps_texte = font.render(f"FPS : {fps}", True, (0, 0, 0))
        screen.blit(fps_texte, (W*0.8, 10))

        age += 1
        if age %300 == 0:
            grenouille.update()
        age_texte = font.render(f"Années : {round(age/60, 1)}", True, (0, 0, 0))
        screen.blit(age_texte, (W*0.8, 40))

        nbIndiv = len(Population.populations)
        nbIndiv_texte = font.render(f"Population : {nbIndiv}", True, (0, 0, 0))
        screen.blit(nbIndiv_texte, (W*0.8, 80))

        #time.sleep(0.2)
        pygame.display.flip()
        clock.tick(20)

pygame.quit()