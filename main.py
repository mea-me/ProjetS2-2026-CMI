#Importation des librairies et fichiers

import math, pygame, random
from random import randint

import src.core.son as son

from src.simulation.genetique.genome import Genome
from src.simulation.genetique.allele import Allele, dico_alleles

from src.simulation.entites.individu import Individu
from src.simulation.entites.livings import Livings, Espece, Population
from src.simulation.entites.especes_predef import *

from src.simulation.environnement.map_generation import Biome, WorldMap
from src.simulation.environnement.plantes import Plante,Liste_plantes

from src.ui.menu import Menu
from src.ui.info_panel import InfoPanel

from src.tools.graph import *



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

    son.explosion()
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
        #print("floup")
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

# Musique pour le menu
pygame.mixer.init()  # Initialize le module mixer.
pygame.mixer.music.load("assets/sounds/background_music_start.mp3")
pygame.mixer.music.play(15)  # Joue la musique de fond.

def starting_game():
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
                son.selection_2()
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

def menu_start():
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

def menu_options():
    clock = pygame.time.Clock()
    time = 0

    menu_items = ["Map", "Espece", "Retour"]
    selected = 0

    # -------- FONTS --------
    font_title = pygame.font.Font(None, 110)
    font_menu = pygame.font.Font(None, 52)

    title_text = font_title.render("NeoRiza", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(W // 2, H * 0.15))

    # Bruit
    noise = pygame.Surface((W, H))
    noise.set_alpha(14)

    while True:
        dt = clock.tick(60)
        time += dt

        # ----- EVENTS -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_items)

                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_items)

                elif event.key == pygame.K_RETURN:
                    return menu_items[selected]

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

        # ----- MENU -----
        for i, item in enumerate(menu_items):
            color = (150, 200, 255) if i == selected else (200, 200, 200)

            text = item

            render = font_menu.render(text, True, color)
            rect = render.get_rect(center=(W // 2, H * 0.4 + i * 60))
            screen.blit(render, rect)

            if i == selected:
                pygame.draw.circle(screen, (150, 200, 255),
                                   (rect.left - 20, rect.centery), 5)

        pygame.display.flip()

def Map_options():
    clock = pygame.time.Clock()

    def reset_settings():
        return {"Taille": 1, "Compléxité": 2, "Fond": 0}, {"Forêt": 0.5, "Désert": 0.5, "Neige": 0.5, "Montagne": 0.5}


    # ----- OPTIONS CLASSIQUES -----
    settings = {
        "Taille": ["S", "M", "L", "XL"],
        "Compléxité": ["1", "2", "3", "4", "5"],
        "Fond": ["ocean", "lagon", "desert", "neige", "plaine"]
    }

    values_index, biomes_sliders = reset_settings()
    active_slider = None

    menu_items = [
        "Taille", "Compléxité", "Fond", 
        "Forêt", "Désert", "Neige", "Montagne", 
        "Réinitialiser", "Retour"
    ]
    selected = 0

    # -------- FONTS --------
    font_title = pygame.font.Font(None, 110)
    font_menu = pygame.font.Font(None, 50)

    title_text = font_title.render("NeoRiza", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(W // 2, H * 0.15))

    # Bruit
    noise = pygame.Surface((W, H))
    noise.set_alpha(14)

    slider_width = 320
    start_y = H * 0.25 # début + haut pour + d'options
    step_y = 60   # espacement ligne

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            # -------- CLAVIER --------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_items)

                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_items)

                elif event.key == pygame.K_LEFT:
                    item = menu_items[selected]
                    if item in settings:
                        values_index[item] = (values_index[item] - 1) % len(settings[item])

                elif event.key == pygame.K_RIGHT:
                    item = menu_items[selected]
                    if item in settings:
                        values_index[item] = (values_index[item] + 1) % len(settings[item])

                elif event.key == pygame.K_RETURN:
                    item = menu_items[selected]
                    
                    if item == "Réinitialiser":
                        values_index, biomes_sliders = reset_settings()
                        
                    elif item == "Retour":
                        # formaté pour WorldMap
                        return {
                            "Taille": settings["Taille"][values_index["Taille"]],
                            "Compléxité": int(settings["Compléxité"][values_index["Compléxité"]]),
                            "Fond": settings["Fond"][values_index["Fond"]],
                            "Composition": {
                                "foret": int(biomes_sliders["Forêt"] * 10),
                                "desert": int(biomes_sliders["Désert"] * 10),
                                "neige": int(biomes_sliders["Neige"] * 10),
                                "montagne": int(biomes_sliders["Montagne"] * 10)
                            }
                        }

            # -------- SOURIS (SLIDERS) --------
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                slider_x = W // 2 - slider_width // 2

                y_temp = int(H * 0.4 + 2 * 65 + 30)
                y_hum = int(H * 0.4 + 3 * 65 + 30)

                if slider_x <= mx <= slider_x + slider_width:   
                    for i, item in enumerate(menu_items): 
                        if item in biomes_sliders: # chercher le slider en question
                            y_pos = int(start_y + i * step_y) +30
                            if abs(my - y_pos) < 15: 
                                active_slider = item

            elif event.type == pygame.MOUSEBUTTONUP:
                active_slider = None

            elif event.type == pygame.MOUSEMOTION and active_slider:
                mx, _ = event.pos
                slider_x = W // 2 - slider_width // 2
                value = (mx - slider_x) / slider_width
                value = max(0.0, min(1.0, value))
                biomes_sliders[active_slider] = value

        # -------- FOND --------
        for y in range(H):
            blue = int(35 + (y / H) * 55)
            pygame.draw.line(screen, (10, 20, blue), (0, y), (W, y))

        noise.fill((random.randint(0, 3), random.randint(0, 5), random.randint(8, 14)))
        screen.blit(noise, (0, 0))

        screen.blit(title_text, title_rect)

        # -------- MENU --------
        for i, item in enumerate(menu_items):
            y_pos = int(start_y + i * step_y)
            color = (150, 200, 255) if i == selected else (200, 200, 200)

            # Si c'est une option déroulante 
            if item in settings:
                value = settings[item][values_index[item]]
                txt = f"{item} : {value}"
                r = font_menu.render(txt, True, color)
                screen.blit(r, r.get_rect(center=(W // 2, y_pos)))

            # Si c'est un slider 
            elif item in biomes_sliders:
                v = int(biomes_sliders[item] * 10)
                r = font_menu.render(f"{item} : {v}/10", True, color)
                screen.blit(r, r.get_rect(center=(W // 2, y_pos)))

                # Dessin de la barre du slider
                sx = W // 2 - slider_width // 2
                pygame.draw.rect(screen, (90, 90, 120), (sx, y_pos + 30, slider_width, 4))
                pygame.draw.circle(screen, (150, 200, 255),
                                   (int(sx + biomes_sliders[item] * slider_width), y_pos + 32), 8)

            # Si c'est un bouton
            else:
                r = font_menu.render(item, True, color)
                screen.blit(r, r.get_rect(center=(W // 2, y_pos)))

            # Petit point de sélection à gauche
            if i == selected:
                pygame.draw.circle(screen, (150, 200, 255), (W // 2 - 230, y_pos), 6)

        pygame.display.flip()
            
def Espece_options():
    clock = pygame.time.Clock()

    # ----- OPTIONS -----
    settings = {
        "Nb Espèces": ["1", "2", "3", "4"],
        "Pop Espèce 1": ["5", "10", "15", "20", "30", "50"],
        "Pop Espèce 2": ["5", "10", "15", "20", "30", "50"],
        "Pop Espèce 3": ["5", "10", "15", "20", "30", "50"],
        "Pop Espèce 4": ["5", "10", "15", "20", "30", "50"]
    }

    values_index = {   # Valeurs par défaut : 2 espèces, de 10 individus
        "Nb Espèces": 1, 
        "Pop Espèce 1": 1, "Pop Espèce 2": 1, "Pop Espèce 3": 1, "Pop Espèce 4": 1
    }

    selected = 0

    # -------- FONTS --------
    font_title = pygame.font.Font(None, 110)
    font_menu = pygame.font.Font(None, 52)
    title_text = font_title.render("NeoRiza", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(W // 2, H * 0.15))

    noise = pygame.Surface((W, H))
    noise.set_alpha(14)

    while True:
        clock.tick(60)
        
        # On construit la liste des menus dynamiquement selon le nombre d'espèces
        nb_esp = int(settings["Nb Espèces"][values_index["Nb Espèces"]])
        menu_items = ["Nb Espèces"]
        for i in range(1, nb_esp + 1):
            menu_items.append(f"Pop Espèce {i}")
        menu_items.append("Retour")

        # ptite sécurité si le select dépasse la taille (quand on REDUIT le nb d'espèces)
        if selected >= len(menu_items): # comme ça on peut pas toucher a l'effectif de lespece 3 si y a 2 especes
            selected = len(menu_items) - 1

        # ----- EVENTS -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_items)

                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_items)

                elif event.key == pygame.K_LEFT:
                    item = menu_items[selected]
                    if item in settings:
                        values_index[item] = (values_index[item] - 1) % len(settings[item])

                elif event.key == pygame.K_RIGHT:
                    item = menu_items[selected]
                    if item in settings:
                        values_index[item] = (values_index[item] + 1) % len(settings[item])

                elif event.key == pygame.K_RETURN:
                    if menu_items[selected] == "Retour":
                        son.selection_3()
                        # On renvoie les paramètres formatés au main
                        return {
                            "Nb Espèces": int(settings["Nb Espèces"][values_index["Nb Espèces"]]),
                            "Pop Espèce 1": int(settings["Pop Espèce 1"][values_index["Pop Espèce 1"]]),
                            "Pop Espèce 2": int(settings["Pop Espèce 2"][values_index["Pop Espèce 2"]]),
                            "Pop Espèce 3": int(settings["Pop Espèce 3"][values_index["Pop Espèce 3"]]),
                            "Pop Espèce 4": int(settings["Pop Espèce 4"][values_index["Pop Espèce 4"]])
                        }

        # -------- FOND --------
        for y in range(H):
            blue = int(35 + (y / H) * 55)
            pygame.draw.line(screen, (10, 20, blue), (0, y), (W, y))

        noise.fill((random.randint(0, 3), random.randint(0, 5), random.randint(8, 14)))
        screen.blit(noise, (0, 0))
        screen.blit(title_text, title_rect)

        # ----- AFFICHAGE DU MENU -----
        for i, item in enumerate(menu_items):
            color = (150, 200, 255) if i == selected else (200, 200, 200)

            if item in settings:
                value = settings[item][values_index[item]]
                text = f"{item} : {value}"
            else:
                text = item

            render = font_menu.render(text, True, color)
            rect = render.get_rect(center=(W // 2, H * 0.35 + i * 60))
            screen.blit(render, rect)

            if i == selected: #point de séléction
                pygame.draw.circle(screen, (150, 200, 255), (rect.left - 20, rect.centery), 5)

        pygame.display.flip()

def menu_graphes():
    clock = pygame.time.Clock()

    options = [
        "Population",
        "Arbre généalogique",
        "Allèles (choisir)",
        "Vue globale (4 graphes)",
        "Retour"
    ]
    selected = 0

    font_title = pygame.font.Font(None, 110)
    font_menu = pygame.font.Font(None, 50)

    title = font_title.render("Graphes", True, (255, 255, 255))
    title_rect = title.get_rect(center=(W // 2, H * 0.2))

    noise = pygame.Surface((W, H))
    noise.set_alpha(14)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Retour"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)

                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)

                elif event.key == pygame.K_RETURN:
                    return options[selected]

        # -------- FOND --------
        for y in range(H):
            blue = int(35 + (y / H) * 55)
            pygame.draw.line(screen, (10, 20, blue), (0, y), (W, y))

        noise.fill((random.randint(0, 3), random.randint(0, 5), random.randint(8, 14)))
        screen.blit(noise, (0, 0))

        screen.blit(title, title_rect)

        for i, opt in enumerate(options):
            color = (150, 200, 255) if i == selected else (200, 200, 200)
            txt = font_menu.render(opt, True, color)
            rect = txt.get_rect(center=(W // 2, H * 0.4 + i * 55))
            screen.blit(txt, rect)

        pygame.display.flip()

def menu_choix_allele(dico_alleles):
    clock = pygame.time.Clock()

    # On garde uniquement les allèles numériques
    alleles = [
        a for a in dico_alleles.keys()
        if dico_alleles[a][5] == "int"
    ]

    index = 0

    font_title = pygame.font.Font(None, 70)
    font_text = pygame.font.Font(None, 48)

    title = font_title.render("Choisir un allèle", True, (255, 255, 255))
    title_rect = title.get_rect(center=(W // 2, H * 0.25))

    noise = pygame.Surface((W, H))
    noise.set_alpha(14)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    index = (index - 1) % len(alleles)

                elif event.key == pygame.K_RIGHT:
                    index = (index + 1) % len(alleles)

                elif event.key == pygame.K_RETURN:
                    return alleles[index]

                elif event.key == pygame.K_ESCAPE:
                    return None

        # -------- FOND --------
        for y in range(H):
            blue = int(35 + (y / H) * 55)
            pygame.draw.line(screen, (10, 20, blue), (0, y), (W, y))

        noise.fill((random.randint(0, 3), random.randint(0, 5), random.randint(8, 14)))
        screen.blit(noise, (0, 0))
        screen.blit(title, title_rect)

        txt = font_text.render(
            f"<  {alleles[index]}  >",
            True,
            (150, 200, 255)
        )
        screen.blit(txt, txt.get_rect(center=(W // 2, H * 0.5)))

        pygame.display.flip()


# valeurs par défaut de la map et des Espèces
Map_taille, Map_composition, Map_fond, Map_complexite = None, None, "ocean", 3
Espece_config = { "Nb Espèces": 2, "Pop Espèce 1": 10, "Pop Espèce 2": 10, "Pop Espèce 3": 10, "Pop Espèce 4": 10 }

running = True
starting_game()

while running:
    choix = menu_start()

    if choix == "Jouer":
        son.selection_1()
        running = False

    elif choix == "Options":
        son.selection_1()
        while True:
            option = menu_options()

            if option == "Map":
                son.selection_1()
                while True:
                    result = Map_options()
                    if result:
                        taille_map_conversion = {"S": 15, "M": 60, "L": 140, "XL": 250}

                        Map_taille = taille_map_conversion[result["Taille"]]
                        Map_complexite = result["Compléxité"]
                        Map_fond = result["Fond"]
                        Map_composition = result["Composition"]
                    break

            elif option == "Espece":
                son.selection_1()
                while True:
                    result = Espece_options()
                    if result: # Si l'utilisateur clique sur Retour
                        Espece_config = result
                        break

            elif option == "Retour":
                son.selection_3()
                break

    elif choix == "Quitter":
        son.selection_3()
        for a in range(20000):
            print(a)
        pygame.quit()
        running = False

pygame.mixer.music.pause()

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

# Initialisation du son
pygame.mixer.init()  # Initialize le module mixer.
pygame.mixer.music.load("assets/sounds/background_musique.mp3")
pygame.mixer.music.play(15)  # Joue la musique de fond.

# génération de la map procédurale
if Map_taille!=None:
    world.procedural_generation(Map_taille, Map_complexite, Map_composition, Map_fond)
else:
    world.procedural_generation()

# no more grenouille, c'est controlé mainteannt -------------------------------------------------------
def trouver_spawn_point():
    # trouver un point d'apparition dans l'ellispe
    valide = False
    while not valide:
        x, y = randint(0, W-1), randint(0, H-1)
        if allowed_mask.get_at((x, y)):
            valide = True
    return x, y

def genese(liste_especes=[], suivi_espece={}):
    # nom hyper fancy pour generer la population de départ
    # foncttion car on la réutilise dans le reset

    liste_especes.clear()
    suivi_espece.clear()
    Population.populations.clear()
    Liste_plantes.clear()

    # init des especes predef (SILENCIEUX, pour que le menu_radial marche)
    e_predef = ["requin", "licorne", "blob", "dragon"]
    for name in e_predef:
        liste_especes.append(Espece(name, 0))
        # pas sur la map mais existe quand meme
        suivi_espece[name] = [None, 0, None] 

    # faux archétypes pour boucher les trous des listes
    suivi_espece["requin"].append(agentArchetype([Requin(0,0)]))
    suivi_espece["licorne"].append(agentArchetype([Licorne(0,0)]))
    suivi_espece["blob"].append(agentArchetype([Blob(0,0)]))
    suivi_espece["dragon"].append(agentArchetype([Dragon(0,0)]))

    # spawn des especes que le joueur a ask for
    nb_esp_depart = Espece_config["Nb Espèces"]

    for i in range(nb_esp_depart):
        nouvelle_espece = Espece(i, 0) # ID ; Apparition = Année 0
        liste_especes.append(nouvelle_espece)
        suivi_espece[i] = [None, 0, None]
        
        popu_temporaire = []
        pop_count = Espece_config[f"Pop Espèce {i+1}"]
        
        for _ in range(pop_count):
            x, y = trouver_spawn_point()
            ind = Individu(x, y, i) # i est son ID d'espèce
            ind.craft_individu()
            ind.give_rect(ind.genome.get_val("taille"))
            Population.add_individu(ind)
            popu_temporaire.append(ind)
            
        # Validation de l'archétype pour le suivi
        if popu_temporaire:
            suivi_espece[i].append(agentArchetype(popu_temporaire))
        
        # et les plantes
        for i in range( 50 ): 
            x,y = trouver_spawn_point()
            Liste_plantes.append(Plante(x, y, 200, 0))
    
    return liste_especes, suivi_espece, Liste_plantes

liste_especes, suivi_espece, Liste_plantes = genese()
# ---------------------------------------------------------------------------------------

# --- état global du jeu ---
game_state = {
    "paused": True,
    "running": True,
    "reset": False,
    "selected": None,
    "placing_mode" : True,
    "radial_open" : False,
    "radial_pos" : (0, 0),
    "speed": 1
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

            if event.key == pygame.K_g:
                game_state["paused"] = True
                save_json(liste_especes, suivi_espece)
            
                choix = menu_graphes()
            
                if choix == "Population":
                    generer_graphique_population()
            
                elif choix == "Arbre généalogique":
                    generer_arbre_genealogique()
            
                elif choix == "Allèles (choisir)":
                    allele = menu_choix_allele(dico_alleles)
                    if allele is not None:
                        generer_graphique_allele(allele, age)
            
                elif choix == "Vue globale (4 graphes)":
                    generer_dashboard_graphes(age)
            
                game_state["paused"] = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # Vérifier si on clique un individu
            clicked = None
            for indi in Population.populations:
                if indi.rect.collidepoint(mx, my):
                    clicked = indi
                    son.selection_2()
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
                son.selection_3()
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
                            son.requin()
                            shark = Requin(mx, my)
                            Population.add_individu(shark)

                        elif name == "Licorne":
                            son.licorne()
                            licorne = Licorne(mx, my)
                            Population.add_individu(licorne)

                        elif name == "Blob":
                            son.blob()
                            blob = Blob(mx, my)
                            Population.add_individu(blob)

                        elif name == "Dragon":
                            son.dragon()
                            dragon = Dragon(mx, my)
                            Population.add_individu(dragon)

                        print(f"{name} ajouté en", mx, my)

                game_state["radial_open"] = False

        # Boutons du menu
        menu.handle_event(event)

    # --- RESET ---
    if game_state["reset"]:
        game_state["paused"] = True
        # Réinitialiser le monde
        world = WorldMap(W, H)
        if Map_taille != None:
            world.procedural_generation(Map_taille, Map_complexite, Map_composition, Map_fond)
        else:
            world.procedural_generation()

        # Réinitialiser la population
        liste_especes, suivi_espece, Liste_plantes = genese(liste_especes, suivi_espece)

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

                
            e.update()

            for e in liste_especes:
                # si espece prdef (texte) et qu'elle n'a JAMAIS vécu
                if isinstance(e.id_espece, str) and max(e.effectif) == 0:
                    e.effectif = [0] # pas besoin de plein de 0 
                    suivi_espece[e.id_espece][1] = age # on repousse sa date de naissance à "maintenant"
                    continue # next: on peut pas mourir si on est pas né jamie

                #Vérification de la  mort 
                if len(e.effectif) > 1 and e.effectif[-1] == 0 and not e.morte:
                    e.morte = True
                    suivi_espece[e.id_espece][2] = age
                    # print(f"L'espèce {e.id_espece} s'est éteinte !")

        for i in range(50-len(Liste_plantes)):                
                x,y = trouver_spawn_point()                        
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
