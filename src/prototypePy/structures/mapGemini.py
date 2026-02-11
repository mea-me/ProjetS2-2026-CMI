import pygame
import random

# --- CONFIGURATION DES BIOMES ---
class Biome:
    def __init__(self, nom, temp, humidite, color):
        self.nom = nom
        self.temp = temp        # -10 à 40
        self.humidite = humidite # 0 à 100
        self.color = color      # (R, G, B)

# Dictionnaire de configuration (nos pots de peinture)
BIOMES_DATA = {
    "EAU":      Biome("Eau",      15, 100, (20, 40, 180)),   # Bleu
    "PLAINE":   Biome("Plaine",   20, 50,  (100, 200, 100)), # Vert clair
    "FORET":    Biome("Foret",    18, 80,  (34, 139, 34)),   # Vert sapin
    "DESERT":   Biome("Desert",   40, 10,  (237, 201, 175)), # Sable
    "NEIGE":    Biome("Neige",    -5, 40,  (240, 250, 255)), # Blanc
}

# --- CLASSE ZONE (Un coup de pinceau) ---
class Zone:
    def __init__(self, x, y, radius, biome_key):
        self.x = x
        self.y = y
        self.radius = radius
        self.biome_key = biome_key # Stocke juste le nom (ex: "FORET")
    
    @property
    def biome(self):
        return BIOMES_DATA[self.biome_key]

    def contains(self, px, py):
        """Vérifie si un point (px, py) est dans ce cercle (maths de base)"""
        return (px - self.x)**2 + (py - self.y)**2 <= self.radius**2

# --- MOTEUR DE CARTE ---
class WorldMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.zones = [] # Liste de tous les coups de pinceaux
        
        # On remplit le fond avec de l'eau par défaut (Zone infinie ou juste couleur de fond)
        self.background_biome = "EAU"

    def add_brush(self, x, y, radius, biome_name):
        """Ajoute une zone (un cercle) à la carte"""
        nouvelle_zone = Zone(x, y, radius, biome_name)
        self.zones.append(nouvelle_zone)

    def draw(self, surface):
        """Dessine tout le monde. L'ordre compte !"""
        # 1. Fond
        bg_color = BIOMES_DATA[self.background_biome].color
        surface.fill(bg_color)

        # 2. Zones (les dernières ajoutées sont au dessus)
        for zone in self.zones:
            color = zone.biome.color
            pygame.draw.circle(surface, color, (zone.x, zone.y), zone.radius)

    def get_climate_at(self, x, y):
        """
        Récupère Temp et Humidité à une position donnée.
        On parcourt la liste À L'ENVERS pour trouver la zone la plus 'haute' (la dernière dessinée).
        """
        # On cherche de la dernière zone ajoutée vers la première
        for zone in reversed(self.zones):
            if zone.contains(x, y):
                return zone.biome.temp, zone.biome.humidite
        
        # Si aucune zone trouvée, c'est le fond
        bg = BIOMES_DATA[self.background_biome]
        return bg.temp, bg.humidite

# --- MAIN ---
pygame.init()

# Setup écran
info = pygame.display.Info()
W, H = info.current_w, info.current_h
# Pour tester sans être en plein écran total bloquant :
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE) 
pygame.display.set_caption("EvoSim - Génération Procédurale")

# Initialisation de la carte
world = WorldMap(W, H)

# --- GÉNÉRATION ALÉATOIRE (Simulation de la brosse) ---
# On "peint" quelques gros continents
world.add_brush(W//2, H//2, 300, "PLAINE") 
world.add_brush(W//2 + 200, H//2 - 100, 250, "DESERT")

# On rajoute des détails (Forêts, Lacs...)
for _ in range(20): # 20 coups de pinceaux aléatoires
    bx = random.randint(0, W)
    by = random.randint(0, H)
    br = random.randint(50, 150) # Rayon aléatoire
    btype = random.choice(["FORET", "NEIGE", "PLAINE"])
    world.add_brush(bx, by, br, btype)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # TEST : Clic de souris pour voir le climat
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            temp, hum = world.get_climate_at(mx, my)
            print(f"Clic en ({mx}, {my}) -> Temp: {temp}°C, Humidité: {hum}%")
            # Ajout dynamique d'un lac au clic
            # world.add_brush(mx, my, 40, "EAU")

    # Rendu
    world.draw(screen)
    
    pygame.display.flip()
    clock.tick(60) # Limite à 60 FPS pour pas brûler le PC

pygame.quit()