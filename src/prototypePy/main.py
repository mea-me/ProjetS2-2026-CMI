#Importation des librairies

import pygame,os,sys,time
from structures.genome import Genome
from random import choice
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
world.add_zone("montagne", 600, 250, 80, 80)    # Montagne DANS le désert

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
            g.deplacement()
            
        Population.update(W,H,world)

        # infos
        fps = round(clock.get_fps(),2)
        fps_texte = font.render(f"FPS : {fps}", True, (0, 0, 0))
        screen.blit(fps_texte, (W*0.8, 10))

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
                    suivi_espece[liste_especes[-1].id_espece] = [agent.id_espece,age]
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


        age_texte = font.render(f"Années : {round(age/60, 1)}", True, (0, 0, 0))
        screen.blit(age_texte, (W*0.8, 40))

        nbIndiv = len(Population.populations)
        nbIndiv_texte = font.render(f"Population : {nbIndiv}", True, (0, 0, 0))
        screen.blit(nbIndiv_texte, (W*0.8, 80))

        #time.sleep(0.2)
        pygame.display.flip()
        clock.tick(60)

pygame.quit()