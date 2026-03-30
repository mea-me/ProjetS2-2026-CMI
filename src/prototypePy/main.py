#Importation des librairies

import pygame,os,sys,time
from random import randint
from structures.genome import Genome
from structures.allele import Allele, dico_alleles
from structures.individu import Individu
from structures.environnement import Biome, WorldMap
from structures.livings import Livings, Espece, Population


def moyenne_des_differences(individu1, individu2):
    """!
    @brief Calcule la distance génétique moyenne entre deux individus.
    @param individu1 Premier individu à comparer.
    @param individu2 Second individu à comparer.
    @return Un float représentant le pourcentage moyen de différence (ex: 0.2 = 20%).
    """
    nb_alleles_etudiees = 0
    total_differences = 0

    for k in dico_alleles.keys():
        type_allele = dico_alleles[k][5]
        val1 = individu1[k] if (isinstance(individu1, dict)) else individu1.genome.get_val(k)
        val2 = individu2[k] if (isinstance(individu2, dict)) else individu2.genome.get_val(k)

        if type_allele == "int":
            somme = val1 + val2
            if somme != 0:
                    # diff relative = |a - b| / moyenne(a, b)
                total_differences += abs((val1 - val2) / (somme / 2))
                nb_alleles_etudiees += 1
        
        elif type_allele == "list":
            diff, elements_valides = 0, 0
            for i in range( len(val1) ):
                somme = val1[i] + val2[i]
                if somme != 0:
                    diff += abs((val1[i] - val2[i]) / (somme / 2))
                    elements_valides += 1
            
            if elements_valides > 0:
                total_differences += diff / elements_valides
                nb_alleles_etudiees += 1
    
    if nb_alleles_etudiees == 0:
        return 0

    return total_differences / nb_alleles_etudiees


def agentArchetype(popu):
    taille_pop = len(popu)
    archetype = {} 
    for agent in popu:
        for k in dico_alleles.keys():
            type_allele = dico_alleles[k][5]
            val = agent.genome.get_val(k)

            if type_allele == "int":
                if k not in archetype:
                    archetype[k] = val
                else:
                    archetype[k] += val

            elif type_allele == "list":
                if k not in archetype:
                    archetype[k] = list(val) 
                else:
                    for i in range(len(archetype[k])):
                        archetype[k][i] += val[i]

            if type_allele == "str":
                archetype[k] = val
    
    for k in archetype.keys(): # division par le nombre d'invidivus
        type_allele = dico_alleles[k][5]

        if type_allele == "int":
            archetype[k] /= taille_pop

        elif type_allele == "list":
            for i in range(len(archetype[k])):
                archetype[k][i] /= taille_pop
    
    return archetype

def NouvelleEspecePointDInterrogation(popu):
    """!
    @brief Cherche si un individu a suffisamment muté pour fonder une nouvelle espèce.
    @param popu Liste contenant TOUS les individus d'une MÊME espèce.
    @return L'individu fondateur de la nouvelle espèce, ou None si pas de spéciation.
    """
    taille_pop = len(popu)
    if taille_pop < 5 : # pas besoin de réfléchir si y a pas assez d'indiv
        return None
    
    #   PROFIL ARCHÉTYPE
    archetype = dict(agentArchetype(popu))

    ##

    agent_eloigne = None 
    max_distance = -1 
    
    for agent in popu:
        m2 = moyenne_des_differences(agent, archetype)
        if m2 > max_distance:
            max_distance = m2
            agent_eloigne = agent
    
    # si le + grand mutant est quasi la moyenne -> on annule
    if max_distance < 0.15:
        return None

    differents = 0
    similaires = 0
    for agent in popu:
        # l'agent compte dans sa famille maintenant
        distance = moyenne_des_differences(agent_eloigne, agent)

        if distance <= 0.15:
            similaires += 1
        elif distance > 0.25:
            differents += 1

    # si sous-groupe (10% mini) + éloigné de la masse (30% mini)
    if similaires >= taille_pop *0.205 and  differents >= taille_pop *0.35:
        return agent_eloigne

    if moyenne_des_differences(archetype,suivi_espece[popu[0].id_espece][3]) >= 0.1:
        distance = 1
        agent_proche = None
        for agent in popu:
            m = moyenne_des_differences(agent,archetype)
            if m < distance:
                agent_proche = agent
                distance = m
        return agent_proche
    
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
grenouilles_bis = []

for i in range(10):
    valide = False
    
    while not valide:
        x, y = randint(0, W), randint(0, H)
        if allowed_mask.get_at((x, y)):
            valide = True
    
    if i > 5:       
        grenouilles.append(Individu(x, y, 0))
    else:
        grenouilles_bis.append(Individu(x,y,1))

for g in grenouilles:
        g.craft_individu()
        g.give_rect(g.genome.get_val("taille"))
        Population.add_individu(g)
for g in grenouilles_bis:
        g.craft_individu()
        g.give_rect(g.genome.get_val("taille"))
        Population.add_individu(g)


grenouille = Espece(0,0)
grenouille_bis = Espece(1,0)

liste_especes = [grenouille,grenouille_bis]
#   ID de l'espèce : [ID du parent, Année de naissance, Année de mort, agent archétype à la création]
suivi_espece = {0 : [None, 0, None], 1 : [None,0,None]}
#---------------------------------------------------------------------------------------
popu1, popu2 = [], []
for p in Population.populations:
    if p.id_espece == 0:
        popu1.append(p)
    else:
        popu2.append(p)
suivi_espece[0].append(agentArchetype(popu1)) 
suivi_espece[1].append(agentArchetype(popu2))

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
            if event.key == pygame.K_e: # afficher les graphes
                print(f"- - - - -\n{suivi_espece}\n- - - - -")

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
        if age%60 == 0:
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
                    popu_bis = []
                    for indiv in popu:
                        if moyenne_des_differences(agent,indiv) <= 0.15 and agent != indiv:
                            indiv.id_espece = liste_especes[-1].id_espece
                            popu_bis.append(indiv)
                    suivi_espece[liste_especes[-1].id_espece].append(agentArchetype(popu_bis))
                    
                    popu_bis_bis = []
                    for indiv in popu:
                        if indiv.id_espece == suivi_espece[liste_especes[-1].id_espece][0]:
                            popu_bis_bis.append(indiv)
                    suivi_espece[suivi_espece[liste_especes[-1].id_espece][0]][3] = dict(agentArchetype(popu_bis_bis))

                    print("Changement : ")
                    for i in range(len(suivi_espece.keys())):
                        print(i," : ", end = "")
                        for I in range(3):
                            print(suivi_espece[i][I],end=" ")
                        print("")

                
                e.update()
            
            for e in liste_especes:
                if len(e.effectif)>1 and e.effectif[-1] == 0 and not e.morte:
                    e.morte = True
                    suivi_espece[e.id_espece][2] = age
                    print(f"Changement : {suivi_espece}")


        age_texte = font.render(f"Années : {round(age/60, 1)}", True, (255, 255, 255))
        screen.blit(age_texte, (W*0.01, H*0.035))

        nbIndiv = len(Population.populations)
        nbIndiv_texte = font.render(f"Population : {nbIndiv}", True, (255, 255, 255))
        screen.blit(nbIndiv_texte, (W*0.01, H*0.06))

        #time.sleep(0.2)
        pygame.display.flip()
        clock.tick(60)

pygame.quit()