#Importation des librairies

import pygame,os,sys,time
from random import randint
from structures.genome import Genome
from structures.allele import Allele, dico_alleles
from structures.individu import Individu
from structures.environnement import Biome, WorldMap
from structures.livings import Livings, Espece, Population
from structures.menu import Menu
from info_panel import InfoPanel
from especes.requin import Requin
from especes.blob import Blob
from especes.dragon import Dragon
from especes.licorne import Licorne


#Fonctions utilisées plus tard =)
def explosion(screen, x, y, max_radius, entities):
    """Explosion animée qui tue toutes les entités dans un rayon."""
    radius = 0
    growth = 12  # vitesse du cercle

    # animation
    while radius < max_radius:
        pygame.time.delay(10)

        # dessiner l'explosion
        pygame.draw.circle(screen, (255, 150, 0), (x, y), radius)
        pygame.draw.circle(screen, (255, 80, 0), (x, y), radius // 2)
        pygame.draw.circle(screen, (255, 200, 0), (x, y), radius, 3)

        pygame.display.update()

        radius += growth

    # tuer les entités touchées
    killed = []
    for e in entities:
        ex, ey = e.rect.center
        if (ex - x)**2 + (ey - y)**2 <= max_radius**2:
            killed.append(e)

    for e in killed:
        entities.remove(e)

    return killed


def moyenne_des_differences(individu1, individu2):
    nb_alleles_etudiees = 0
    t = 0
    for k in dico_alleles.keys():
        if dico_alleles[k][5] == "int":
            nb_alleles_etudiees += 1
        
        if k == "couleur":
            nb_alleles_etudiees += 1

    
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


radial_options = [
    {"name": "Random", "color": (120, 180, 255)},
    {"name": "Requin", "color": (255, 80, 80)},
    {"name": "Licorne", "color": (255, 150, 255)},
    {"name": "Blob", "color": (180, 0, 255)},
    {"name": "Dragon", "color": (255, 60, 60)}
]

def draw_radial_menu(screen, pos, options):
    x, y = pos
    radius = 70
    button_positions = []

    pygame.draw.circle(screen, (50, 50, 50), (x, y), radius)
    pygame.draw.circle(screen, (200, 200, 200), (x, y), radius, 3)

    angle_step = 360 / len(options)

    for i, opt in enumerate(options):
        angle = i * angle_step
        vec = pygame.math.Vector2(1, 0).rotate(angle)
        ox = x + int(vec.x * radius * 0.6)
        oy = y + int(vec.y * radius * 0.6)

        pygame.draw.circle(screen, opt["color"], (ox, oy), 22)

        font = pygame.font.SysFont(None, 20)
        txt = font.render(opt["name"], True, (0, 0, 0))
        screen.blit(txt, (ox - txt.get_width()//2, oy - txt.get_height()//2))

        button_positions.append((ox, oy, 22, opt["name"]))

    return button_positions




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

# --- AJOUT : état global du jeu ---
game_state = {
    "paused": True,
    "running": True,
    "reset": False,
    "selected": None,
    "placing_mode" : False,
    "radial_open" : False,
    "radial_pos" : (0, 0),
    "speed": 1,
    "skip": 0
}

menu = Menu(screen, game_state)
info_panel = InfoPanel(screen)



shark = Requin(500, 500)
Population.add_individu(shark)


while game_state["running"]:

    # --- Gestion des événements ---
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_state["running"] = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state["running"] = False

            if event.key == pygame.K_RETURN:
                game_state["paused"] = not game_state["paused"]

            if event.key == pygame.K_1:
                x, y = pygame.mouse.get_pos()
                explosion(screen, x, y, 300, Population.populations)

            if event.key == pygame.K_p:  # touche P
                game_state["placing_mode"] = not game_state["placing_mode"]
                game_state["radial_open"] = False
                print("Mode pose :", game_state["placing_mode"])

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # Vérifier si on clique un individu
            clicked = None
            for indi in Population.populations:
                if indi.rect.collidepoint(mx, my):
                    clicked = indi
                    break

            if clicked:
                game_state["selected"] = clicked
            else:
                # Sinon, afficher les infos du biome comme avant
                game_state["selected"] = None
                temp, hum, nom = world.get_infos_at(mx, my)
                print(f"Zone: {nom.upper()} | Temp: {temp}°C | Hum: {hum}%")
            
        # --- Clic droit : ouvrir le menu radial ---
        if game_state["placing_mode"] and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # clic droit
                game_state["radial_open"] = True
                game_state["radial_pos"] = pygame.mouse.get_pos()
        
        # --- Clic gauche : sélectionner une option du menu ---
        if game_state["placing_mode"] and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and game_state["radial_open"]:
                mx, my = pygame.mouse.get_pos()

                for ox, oy, r, name in game_state["radial_buttons"]:
                    if (mx - ox)**2 + (my - oy)**2 <= r*r:

                        if name == "Random":
                            new = Individu(mx, my, espece=0)
                            new.craft_individu()
                            new.give_rect(new.genome.get_val("taille"))
                            Population.add_individu(new)

                        elif name == "Requin":
                            shark = Requin(mx, my)
                            Population.add_individu(shark)

                        elif name == "Licorne":
                            licorne = Licorne(mx, my)
                            Population.add_individu(licorne)

                        elif name == "Blob":
                            blob = Blob(mx, my)
                            Population.add_individu(blob)

                        elif name == "Dragon":
                            dragon = Dragon(mx, my)
                            Population.add_individu(dragon)

                        print(f"{name} ajouté en", mx, my)

                game_state["radial_open"] = False




        # Boutons du menu
        menu.handle_event(event)


    # --- SAUT DANS LE TEMPS PROGRESSIF ---
    if game_state["skip"] > 0:
        step = min(10, game_state["skip"])  # 10 frames simulées par tick

        for _ in range(step):

            # Simuler la vie normalement (sans affichage)
            for g in Population.populations:
                g.deplacement_random()

            Population.update(W, H, world)
            age += 1

        game_state["skip"] -= step

    # --- RESET ---
    if game_state["reset"]:
        # Réinitialiser le monde
        world = WorldMap(W, H)
        world.procedural_generation()

        # Réinitialiser la population
        Population.populations = []
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

        # Réinitialiser les espèces
        grenouille = Espece(0, 0)
        liste_especes = [grenouille]
        suivi_espece = {0: [None, 0, None]}

        # Réinitialiser le temps
        age = 0

        # Fin du reset
        game_state["reset"] = False


    if game_state["paused"]:
        world.paint(screen)
        screen.blit(overlay, (0, 0))

        # --- DESSINER LES INDIVIDUS MÊME EN PAUSE ---
        for g in Population.populations:
            g.draw(screen)   # pas de déplacement ici

        # --- AFFICHER LES INFOS MÊME EN PAUSE ---
        fps = round(clock.get_fps(), 2)
        fps_texte = font.render(f"FPS : {fps}", True, (255, 255, 255))
        screen.blit(fps_texte, (W*0.01, H*0.01))

        age_texte = font.render(f"Années : {round(age/60, 1)}", True, (255, 255, 255))
        screen.blit(age_texte, (W*0.01, H*0.035))

        nbIndiv = len(Population.populations)
        nbIndiv_texte = font.render(f"Population : {nbIndiv}", True, (255, 255, 255))
        screen.blit(nbIndiv_texte, (W*0.01, H*0.06))

        # --- AFFICHER LE MENU ---
        menu.draw()

        # --- AFFICHER LE PANNEAU D’INFO SI UN INDIVIDU EST SÉLECTIONNÉ ---
        if game_state["selected"] is not None:
            info_panel.draw(game_state["selected"], world)

        # --- AFFICHAGE DU MENU RADIAL ---
        if game_state["placing_mode"] and game_state["radial_open"]:
            game_state["radial_buttons"] = draw_radial_menu(
                screen,
                game_state["radial_pos"],
                radial_options
            )


        pygame.display.flip()
        clock.tick(60)
        continue



    # --- MODE NORMAL ---
    world.paint(screen)

    for g in Population.populations:
        g.draw(screen)
        g.deplacement_random()

    screen.blit(overlay, (0, 0))

    Population.update(W, H, world)  

    # FPS
    fps = round(clock.get_fps(), 2)
    fps_texte = font.render(f"FPS : {fps}", True, (255, 255, 255))
    screen.blit(fps_texte, (W*0.01, H*0.01))

    # Accélération du temps
    age += game_state["speed"]

    # Gestion des espèces (inchangé)
    if age % 180 == 0:
        liste_especes_bis = liste_especes[:]
        for e in liste_especes_bis:
            popu = [indi for indi in Population.populations if indi.id_espece == e.id_espece]
            agent = NouvelleEspecePointDInterrogation(popu)

            if agent is not None:
                a = Espece(liste_especes[-1].id_espece + 1, age)
                liste_especes.append(a)
                suivi_espece[a.id_espece] = [agent.id_espece, age, None]
                agent.id_espece = a.id_espece

                for indiv in popu:
                    if moyenne_des_differences(agent, indiv) <= 0.2 and agent != indiv:
                        indiv.id_espece = a.id_espece

            e.update()

        for e in liste_especes:
            if len(e.effectif) > 1 and e.effectif[-1] == 0 and not e.morte:
                e.morte = True
                suivi_espece[e.id_espece][2] = age

        print(suivi_espece)

    # Infos
    age_texte = font.render(f"Années : {round(age/60, 1)}", True, (255, 255, 255))
    screen.blit(age_texte, (W*0.01, H*0.035))

    nbIndiv = len(Population.populations)
    nbIndiv_texte = font.render(f"Population : {nbIndiv}", True, (255, 255, 255))
    screen.blit(nbIndiv_texte, (W*0.01, H*0.06))

    # --- AFFICHAGE DU MENU EN PERMANENCE ---
    menu.draw()

    # Affichage du panneau si un individu est sélectionné
    if game_state["selected"] is not None:
        info_panel.draw(game_state["selected"], world)

    # --- AFFICHAGE DU MENU RADIAL ---
    if game_state["placing_mode"] and game_state["radial_open"]:
        game_state["radial_buttons"] = draw_radial_menu(
            screen,
            game_state["radial_pos"],
            radial_options
        )
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
