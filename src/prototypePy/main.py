#Importation des librairies

import math
import pygame,os,sys,time, json
from random import randint
from structures.genome import Genome
from structures.allele import Allele, dico_alleles
from structures.individu import Individu
from structures.environnement import Biome, WorldMap
from structures.livings import Livings, Espece, Population
from nourriture.plantes import Plante,Liste_plantes
from structures.menu import Menu
from info_panel import InfoPanel
from especes.requin import Requin
from especes.blob import Blob
from especes.dragon import Dragon
from especes.licorne import Licorne
from graph import *


def draw_dna(surface, center, time, scale=1.5):
    cx, cy = center
    points = 27  # plus de détails
    height = 250 * scale   # hauteur ADN
    width = 100 * scale    # largeur ADN

    for i in range(points):
        y = -height // 2 + (i / points) * height
        angle = time * 0.002 + i * 0.35

        x1 = math.cos(angle) * width
        x2 = math.cos(angle + math.pi) * width

        pygame.draw.circle(
            surface, (0, 220, 255),
            (int(cx + x1), int(cy + y)), 7
        )
        pygame.draw.circle(
            surface, (0, 140, 220),
            (int(cx + x2), int(cy + y)), 7
        )

        pygame.draw.line(
            surface, (60, 100, 160),
            (cx + x1, cy + y),
            (cx + x2, cy + y), 2
        )

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

        if distance <= 0.2:
            similaires += 1
        elif distance > 0.25:
            differents += 1

    # si sous-groupe (20.5% mini) + éloigné de la masse (35% mini)
    if similaires >= taille_pop *0.205 and  differents >= taille_pop *0.35:
        return agent_eloigne

    if moyenne_des_differences(archetype,suivi_espece[popu[0].id_espece][3]) >= 0.2:
        print("floup")
        distance = 1
        agent_proche = None
        for agent in popu:
            m = moyenne_des_differences(agent,archetype)
            if m < distance:
                agent_proche = agent
                distance = m
        return agent_proche
    
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

def starting_game():
    import random

    clock = pygame.time.Clock()
    run = True
    time = 0

    blink = True
    blink_timer = 0

    # Polices
    font_title = pygame.font.Font(None, 110)
    font_text = pygame.font.Font(None, 48)
    font_signature = pygame.font.Font(None, 24)

    signature_text = font_signature.render(
        "Made by ToZiLéNon", True, (255, 255, 255)
    )

    signature_shadow = font_signature.render(
        "Made by ToZiLéNon", True, (0, 0, 0)
    )

    # Textes
    title_text = font_title.render("NeoRiza", True, (255, 255, 255))
    start_text = font_text.render(
        "Appuyez sur n'importe quelle touche pour commencer",
        True,
        (200, 200, 200)
    )

    title_rect = title_text.get_rect(center=(W // 2, H * 0.15))
    start_rect = start_text.get_rect(center=(W // 2, H * 0.8))

    # Surface de bruit (créée une seule fois)
    noise_surface = pygame.Surface((W, H))
    noise_surface.set_alpha(12)

    while run:
        dt = clock.tick(60)
        time += dt
        blink_timer += dt

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:
                return True

        if blink_timer > 600:
            blink = not blink
            blink_timer = 0

        
        # ---------- FOND BLEU SUBTIL (GRADIENT) ----------
        for y in range(H):
            blue = int(20 + (y / H) * 40)
            pygame.draw.line(
                screen,
                (10, 20, blue),
                (0, y),
                (W, y)
            )

        # ---------- BRUIT BLEUTÉ LÉGER ----------
        noise_surface.fill((
            random.randint(0, 4),
            random.randint(0, 6),
            random.randint(8, 14)
        ))
        screen.blit(noise_surface, (0, 0))

        # ---------- ADN ----------
        draw_dna(screen, (W // 2, H // 2), time, scale=1.6)

        # ---------- TEXTES ----------
        screen.blit(title_text, title_rect)

         # Rotation du texte (penché)
        signature_text_rot = pygame.transform.rotate(signature_text, +15)
        signature_shadow_rot = pygame.transform.rotate(signature_shadow, +15)


        # Texte penché style Minecraft (ombre + texte)
        screen.blit(signature_shadow_rot, (14, 14))
        screen.blit(signature_text_rot, (12, 12))

        if blink:
            screen.blit(start_text, start_rect)

        pygame.display.flip()
starting_game()

def menu_start():
    import random
    import math

    clock = pygame.time.Clock()
    time = 0

    options = ["Jouer", "Options", "Quitter"]
    selected = 0

    # -------- FONTS --------
    font_title = pygame.font.Font(None, 110)
    font_menu = pygame.font.Font(None, 52)
    font_signature = pygame.font.Font(None, 24)

    title_text = font_title.render("NeoRiza", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(W // 2, H * 0.15))

    # Signature penchée (style Minecraft)
    signature = font_signature.render("Made by ToZiLéNon", True, (200, 220, 255))
    signature_shadow = font_signature.render("Made by ToZiLéNon", True, (0, 0, 0))
    signature_rot = pygame.transform.rotate(signature, +15)
    signature_shadow_rot = pygame.transform.rotate(signature_shadow, +15)

    # Bruit
    noise = pygame.Surface((W, H))
    noise.set_alpha(14)

    while True:
        dt = clock.tick(60)
        time += dt

        # -------- EVENTS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)

                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)

                if event.key == pygame.K_RETURN:
                    return options[selected]

        # -------- FOND BLEU SUBTIL --------
        for y in range(H):
            blue = int(35 + (y / H) * 55)
            pygame.draw.line(screen, (10, 20, blue), (0, y), (W, y))

        # -------- BRUIT --------
        noise.fill((
            random.randint(0, 3),
            random.randint(0, 5),
            random.randint(8, 14)
        ))
        screen.blit(noise, (0, 0))
        
        # -------- TITRE --------
        screen.blit(title_text, title_rect)

        # -------- MENU --------
        for i, option in enumerate(options):
            if i == selected:
                color = (150, 200, 255)
            else:
                color = (200, 200, 200)

            text = font_menu.render(option, True, color)
            rect = text.get_rect(center=(W // 2, H * 0.45 + i * 70))
            screen.blit(text, rect)

            # Petit indicateur discret
            if i == selected:
                pygame.draw.circle(screen, (150, 200, 255),
                                   (rect.left - 20, rect.centery), 5)

        # -------- SIGNATURE --------
        screen.blit(signature_shadow_rot, (14, 14))
        screen.blit(signature_rot, (12, 12))

        pygame.display.flip()

choix = menu_start()

if choix == "Jouer":
    pass

elif choix == "Options":
    print("igigi")

elif choix == "Quitter":
    pygame.quit()


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

liste_especes = [Espece("requin",0),Espece("licorne",0),Espece("blob",0),Espece("dragon",0),grenouille,grenouille_bis]
#   ID de l'espèce : [ID du parent, Année de naissance, Année de mort, agent archétype à la création]
suivi_espece = {"requin" : [None,0,None],"licorne" : [None, 0, None],"blob" : [None, 0, None],"dragon" : [None, 0, None],0 : [None, 0, None], 1 : [None,0,None]}

popu1, popu2 = [], []
for p in Population.populations:
    if p.id_espece == 0:
        popu1.append(p)
    else:
        popu2.append(p)

suivi_espece["requin"].append(Requin(0,0))
suivi_espece["licorne"].append(Licorne(0,0))
suivi_espece["blob"].append(Blob(0,0))
suivi_espece["dragon"].append(Dragon(0,0))
suivi_espece[0].append(agentArchetype(popu1)) 
suivi_espece[1].append(agentArchetype(popu2))

for i in range(50):
    valide = False
    
    while not valide:
        x, y = randint(0, W-1), randint(0, H-1)
        if allowed_mask.get_at((x, y)):
            valide = True
            
    Liste_plantes.append(Plante(x, y, 200, 0))
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
# création du menu et du panel
menu = Menu(screen, game_state)
info_panel = InfoPanel(screen)

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

            if event.key == pygame.K_g: # afficher les graphes
                game_state["paused"] = not game_state["paused"]
                save_json(liste_especes, suivi_espece)
                generer_graphique_population()
                generer_arbre_genealogique()  

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
        game_state["paused"] = True
        # Réinitialiser le monde
        world = WorldMap(W, H)
        world.procedural_generation()

        # Réinitialiser la population
        Population.populations = []
        #Création de grenouille---------------------------------------------
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

        # Réinitialiser les espèces
        grenouille = Espece(0, 0)
        grenouille_bis = Espece(1,0)
        liste_especes = [Espece("requin",0),Espece("licorne",0),Espece("blob",0),Espece("dragon",0),grenouille,grenouille_bis]
        #   ID de l'espèce : [ID du parent, Année de naissance, Année de mort, agent archétype à la création]
        suivi_espece = {"requin" : ["TOBLADZ",0,None],"licorne" : ["TOBLADZ", 0, None],"blob" : ["TOBLADZ", 0, None],"dragon" : ["TOBLADZ", 0, None],0 : ["TOBLADZ", 0, None], 1 : ["TOBLADZ",0,None]}
        suivi_espece["requin"].append(Requin(0,0))
        suivi_espece["licorne"].append(Licorne(0,0))
        suivi_espece["blob"].append(Blob(0,0))
        suivi_espece["dragon"].append(Dragon(0,0))
        suivi_espece[0].append(agentArchetype(popu1)) 
        suivi_espece[1].append(agentArchetype(popu2))


        # Réinitialiser le temps
        age = 0

        # Fin du reset
        game_state["reset"] = False

    if game_state["paused"]:
        world.paint(screen)
        screen.blit(overlay, (0, 0))

        # --- DESSINER LES INDIVIDUS MÊME EN PAUSE ---
        for g in Population.populations:
            g.draw(screen)

        for plante in Liste_plantes:
            plante.draw(screen)

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

    deletion = []
    for plante in Liste_plantes:
        plante.draw(screen)
        plante.age += 1
        for P in Population.populations:
            if P.collide_with(plante) and P.genome.get_val("régime") != "carnivore":
                P.energie += plante.manger()
                deletion.append(plante)
        
    for plante in deletion:
        if plante in Liste_plantes:
            Liste_plantes.remove(plante)
        del(plante)
    screen.blit(overlay, (0, 0)) # ellipse

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

    # Gestion des espèces 
    if age%60 == 0:
        for e in liste_especes:
            print(e.effectif)
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
                    if moyenne_des_differences(agent,indiv) <= 0.2 and agent != indiv:
                        indiv.id_espece = liste_especes[-1].id_espece
                        popu_bis.append(indiv)
                suivi_espece[liste_especes[-1].id_espece].append(agentArchetype(popu_bis))
                
                popu_bis_bis = []
                for indiv in popu:
                    if indiv.id_espece == suivi_espece[liste_especes[-1].id_espece][0]:
                        popu_bis_bis.append(indiv)
                suivi_espece[suivi_espece[liste_especes[-1].id_espece][0]][3] = dict(agentArchetype(popu_bis_bis))

                print("Changement : ")
                for i in suivi_espece.keys():
                    print(i," : ", end = "")
                    for I in range(3):
                        print(suivi_espece[i][I],end=" ")
                    print("")
                for i in range(len(liste_especes)):
                    print(i ,":", liste_especes[i].effectif)

                
            e.update()

        for e in liste_especes:
            if len(e.effectif) > 1 and e.effectif[-1] == 0 and not e.morte:
                e.morte = True
                suivi_espece[e.id_espece][2] = age
                # print("Changement : ")
                # for i in range(len(suivi_espece.keys())):
                #     print(i," : ", end = "")
                #     for I in range(3):
                #         print(suivi_espece[i][I],end=" ")
                #     print("")
                # for i in range(len(liste_especes)):
                #     print(i ,":", liste_especes[i].effectif)

        print(suivi_espece)

        for i in range(50-len(Liste_plantes)):
                valide = False
                
                while not valide:
                    x, y = randint(0, W-1), randint(0, H-1)
                    if allowed_mask.get_at((x, y)):
                        valide = True
                        
                Liste_plantes.append(Plante(x, y, 200, 0))
        
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
