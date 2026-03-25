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

        nb_alleles_etudiees += 1 if (type_allele == "int" or "list") else 0

        if type_allele == "int":
            somme = val1 + val2
            if somme != 0:
                # diff relative = |a - b| / moyenne(a, b)
                total_differences += abs((val1 - val2) / (somme / 2))
        
        elif type_allele == "list":
            diff = 0
            for i in range( len(val1) ):
                somme = val1[i] + val2[i]
                if somme != 0:
                    diff += abs((val1[i] - val2[i]) / (somme / 2))
            
            # diffR total = moyenne des differences relatives
            total_differences += diff / len(val1)
    

    return total_differences / nb_alleles_etudiees


def NouvelleEspecePointDInterrogation(popu):
    """!
    @brief Cherche si un individu a suffisamment muté pour fonder une nouvelle espèce.
    @param popu Liste contenant TOUS les individus d'une MÊME espèce.
    @return L'individu fondateur de la nouvelle espèce, ou None si pas de spéciation.
    """
    taille_pop = len(popu)
    if taille_pop < 5 : # pas besoin de réfléchir si y a pas assez d'indiv
        return None
    
    archetype = {} # création du profil archetype
    for agent in popu:
        for k in dico_alleles.keys():
            type_allele = dico_alleles[k][5]

            if type_allele == "int":
                if k not in archetype :
                    archetype[k] = agent.genome.get_val(k)  
                else:
                    archetype[k] += agent.genome.get_val(k)

            if type_allele == "list":
                if k not in archetype :
                    archetype[k] = agent.genome.get_val(k)  
                else:
                    for i in range(len(archetype[k])):
                        archetype[k][i] += agent.genome.get_val(k)[i]

            if type_allele == "str":
                archetype[k] = agent.genome.get_val(k)
    
    for a in archetype.values(): # division par le nombre d'invidivus
        if isinstance(a, int) :
            a /= taille_pop
        
        if isinstance(a, list) :
            for i in range( len(a) ):
                a[i] /= taille_pop

        print(a)
    ##

    agent_eloigne = None # On trouve l'agent le "plus mutant"
    m = 0
    for agent in popu:
        m2 = moyenne_des_differences(agent,archetype)
        if m<=m2:
            m = m2
            agent_eloigne = agent
    
    #On compte combien d'agents sont similaires et différents par rapport à l'agent le plus éloigné pour savoir si on crée un nouvelle espèce
    differents = 0
    similaires = 0
    for agent in popu:
        if agent != agent_eloigne:
            distance = moyenne_des_differences(agent_eloigne,agent)

            if distance <= 0.2:
                similaires += 1
            elif distance > 0.3:
                differents += 1

    # si sous-groupe (similaires) + éloigné de la masse (différents)
    if similaires >= taille_pop/4 and differents >= taille_pop / 2:
        return agent_eloigne

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
#   ID de l'espèce : [ID du parent, Année de naissance, Année de mort]
suivi_espece = {0 : [None, 0, None]}
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
                    for indiv in popu:
                        if moyenne_des_differences(agent,indiv) <= 0.2 and agent != indiv:
                            indiv.id_espece = liste_especes[-1].id_espece

                
                e.update()
            
            for e in liste_especes:
                if len(e.effectif)>1 and e.effectif[-1] == 0 and not e.morte:
                    e.morte = True
                    suivi_espece[e.id_espece][2] = age


        age_texte = font.render(f"Années : {round(age/60, 1)}", True, (255, 255, 255))
        screen.blit(age_texte, (W*0.01, H*0.035))

        nbIndiv = len(Population.populations)
        nbIndiv_texte = font.render(f"Population : {nbIndiv}", True, (255, 255, 255))
        screen.blit(nbIndiv_texte, (W*0.01, H*0.06))

        #time.sleep(0.2)
        pygame.display.flip()
        clock.tick(60)

pygame.quit()