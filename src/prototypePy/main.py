#Importation des librairies

import pygame,os,sys,time
from random import randint
from structures.genome import Genome
from structures.allele import Allele, dico_alleles
from structures.individu import Individu
from structures.environnement import Biome, WorldMap
from structures.livings import Livings, Espece, Population


#Fonctions utilisées plus tard =)

def moyenne_des_differences(individu1, individu2):
    nb_alleles_etudiees = 0
    for k in dico_alleles.keys():
        if dico_alleles[k][5] == "int":
            nb_alleles_etudiees += 1
        
        if k == "couleur":
            nb_alleles_etudiees += 1

    
    t = 0
    for k in dico_alleles.keys():
        a = individu1.genome.get_val(k)
        b = individu2.genome.get_val(k)
        if dico_alleles[k][5] == "int":
            if not a+b == 0:
                t += abs((a-b)/((a+b)/2))
        
        if k == "couleur":
            t_bis = 0
            for i in range(3):
                if not a[i] + b[i] == 0:
                    t_bis += abs((a[i]-b[i])/((a[i]+b[i])/2))
            
            t += t_bis/3
    

    return t/nb_alleles_etudiees


def NouvelleEspecePointDInterrogation(popu):
    '''renvoie un agent si les conditions requises pour une nouvelle espece sont atteintes, None sinon
    arg : popu est la liste population mais ne contenant que des individus d'une meme espece'''
    for agent in popu:
        similaires = 0
        for agent_bis in popu:
            if agent != agent_bis and moyenne_des_differences(agent,agent_bis)<=0.2:
                similaires += 1
        differents = 0
        for agent_bis in popu:
            if agent != agent_bis and moyenne_des_differences(agent,agent_bis)>0.3:
                differents += 1

        if len(popu)>4 and similaires >= len(popu)/4 and differents >= len(popu)/2:
            return agent

    return None



#Initialisation de Pygame
pygame.init()


# Setup écran
info = pygame.display.Info()
W, H = info.current_w, info.current_h
# Pour tester sans être en plein écran total bloquant :
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN) 
pygame.display.set_caption("NeoRiza | Simulateur d’Évolution Biologique")

# Initialisation du framerate pour egaliser la vitesse de jeu sur toutes les machines
framerate = 60
clock = pygame.time.Clock()
dt = clock.tick(framerate)
age = 0

#ellipse
mask_surface = pygame.Surface((W, H), pygame.SRCALPHA) # -> SRCALPHA = transparent
mask_surface.fill((0, 0, 0, 0)) # no no zone

overlay = pygame.Surface((W, H)) 
overlay.fill((10, 10, 10)) # Couleur de l'extérieur du globe (gris très foncé/noir)

playable_rect = pygame.Rect(20, 20, W - 40, H - 40) # ellipse magenta qui servira de trou
pygame.draw.ellipse(overlay, (255, 0, 255), playable_rect) 
overlay.set_colorkey((255, 0, 255)) # le magenta = 100% transparent

# Masque de collision (rétréci de 40px de chaque côté)
movement_rect = playable_rect.inflate(-80, -80) 

mask_surface = pygame.Surface((W, H), pygame.SRCALPHA)
# ellipse de déplacement autorisée 
pygame.draw.ellipse(mask_surface, (255, 255, 255, 255), movement_rect)

allowed_mask = pygame.mask.from_surface(mask_surface)

grenouille = Espece(0,0)
font = pygame.font.SysFont("Arial", 18)
world = WorldMap(W, H)

# génération de la map procédurale
world.procedural_generation()

#Création de grenouille-----------------------------------------------------------------
grenouilles = []

for i in range(5):
    valide = False
    
    while not valide:
        x, y = randint(0, W), randint(0, H)
        if allowed_mask.get_at((x, y)):
            valide = True
            
    grenouilles.append(Individu(x, y, 0))

for g in grenouilles:
        g.craft_individu()
        g.give_rect(g.genome.get_val("taille"))
        Population.add_individu(g)


grenouille = Espece(0,0)

liste_especes = [grenouille]
#     clé : espece;0 : parent ; 1 : date d'apparition ; 2 : date de mort
suivi_espece = {0 : [None,0,None]}
#--------------------------------------------------------------------------------------- 

paused = False        
running = True



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: # PAUSE SUR ENTREE
                paused = not(paused)
            if event.key == pygame.K_ESCAPE: # Sécurité Plein Écran
                running = False

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

        # on dessine la population =)
        for g in Population.populations:
            g.draw(screen)
            g.deplacement_random()
            #deplacement en soustrayant le x des dux individu besoin de trouver le pplus proche voisin avant

        screen.blit(overlay, (0, 0)) # ellipse
            
        Population.update(W,H,world)

        # infos
        fps = round(clock.get_fps(),2)
        fps_texte = font.render(f"FPS : {fps}", True, (255, 255, 255))
        screen.blit(fps_texte, (W*0.01, H*0.01))

        age += 1
        if age %180 == 0:
            liste_especes_bis = liste_especes[:]
            for e in liste_especes_bis:
                popu = []
                for indi in Population.populations:
                    if indi.id_espece == e.id_espece:
                        popu.append(indi)
                agent = NouvelleEspecePointDInterrogation(popu)
                if agent is not None:
                    a = Espece(liste_especes[-1].id_espece + 1,age)
                    liste_especes.append(a)
                    suivi_espece[liste_especes[-1].id_espece] = [agent.id_espece, age, None]
                    agent.id_espece = liste_especes[-1].id_espece
                    for indiv in popu:
                        if moyenne_des_differences(agent,indiv) <= 0.2 and agent != indiv:
                            indiv.id_espece = liste_especes[-1].id_espece

                
                e.update()
            
            for e in liste_especes:
                if len(e.effectif)>1 and e.effectif[-1] == 0 and not e.morte:
                    e.morte = True
                    suivi_espece[e.id_espece][2] = age
                    
            print(suivi_espece)


        age_texte = font.render(f"Années : {round(age/60, 1)}", True, (255, 255, 255))
        screen.blit(age_texte, (W*0.01, H*0.035))

        nbIndiv = len(Population.populations)
        nbIndiv_texte = font.render(f"Population : {nbIndiv}", True, (255, 255, 255))
        screen.blit(nbIndiv_texte, (W*0.01, H*0.06))

        #time.sleep(0.2)
        pygame.display.flip()
        clock.tick(60)

pygame.quit()