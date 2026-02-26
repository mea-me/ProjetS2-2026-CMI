import pygame
import random 

class Biome:
    def __init__(self, nom, x, y, width, height):
        self.nom = nom
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        infos = dico_biomes[nom]
        self.temperature = infos["temperature"]
        self.humidite = infos["humidite"]
        self.color = infos["color"]

        self.rect = pygame.Rect(x, y, width, height)

    def draw_biome(self, surface): 
        pygame.draw.rect(surface, self.color, self.rect) 
   
    def contains(self, x, y): # position d'un clic de souris 
        # ou un individu (si on passe ses coords : Individu.get_position)
        return self.rect.collidepoint(x, y) 
    
    def get_pos(self):
        return (self.x,self.y)
    
    def __repr__(self): 
        return f"{self.nom} [Pos: {self.x},{self.y}] (T={self.temperature}, H={self.humidite})"


# Format : "nom": {"temperature": T, "humidite": H, "color": (R, G, B), "affinites" : dictionnaire des affinités entre biomes}
dico_biomes = {
    "ocean":    {"temperature": 10,  "humidite": 100, "color": (30, 144, 255),  "affinites": {"ocean": 100, "plaine": 50, "desert": 5}},
    "plaine":   {"temperature": 15,  "humidite": 30,  "color": (144, 238, 144), "affinites": {"ocean": 60, "plaine": 100, "foret": 80, "desert": 20, "montagne": 40}},
    "foret":    {"temperature": 25,  "humidite": 80,  "color": (34, 139, 34),   "affinites": {"plaine": 100, "foret": 100, "montagne": 30}},
    "desert":   {"temperature": 40,  "humidite": 0,   "color": (237, 201, 175), "affinites": {"plaine": 30, "desert": 100, "ocean": 5}},
    "montagne": {"temperature": -5,  "humidite": 20,  "color": (128, 128, 128), "affinites": {"plaine": 50, "foret": 40, "montagne": 100, "neige": 90}},
    "neige":    {"temperature": -20, "humidite": 60,  "color": (255, 250, 250), "affinites": {"montagne": 100, "neige": 100, "plaine": 10}}
}



class WorldMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.biomes = [] # liste d'objets Biome
        self.background_biome = "ocean"

    def add_zone(self, nom, x, y, width, height): # add a la liste de biomes
        self.biomes.append(Biome(nom, x, y, width, height))

    def procedural_generation(self, nb_zones=50):
        # gros continent de base (Plaine) au centre
        w_base, h_base = int(self.width * 0.8), int(self.height * 0.8)
        x_base, y_base = (self.width - w_base) // 2, (self.height - h_base) // 2
        self.add_zone("plaine", x_base, y_base, w_base, h_base)

        biomes_a_placer = ["foret", "desert", "montagne", "neige"]

        tentatives_max = nb_zones * 4 # sécu
        zones_placees = 0

        while zones_placees < nb_zones and tentatives_max > 0:
            tentatives_max -= 1
            
            biome_candidat = random.choice(biomes_a_placer)
            
            # random coordonnée sur la map
            temp_x, temp_y  = random.randint(0, self.width), random.randint(0, self.height)

            _, _, biome_actuel = self.get_infos_at(temp_x, temp_y)
            
            # LOGIQUE DE POIDS (Affinité)
            affinite = dico_biomes[biome_candidat]["affinites"].get(biome_actuel, 0)
                                                          # si pas d'affinité définie --> 0
            
            if random.randint(0, 100) <= affinite:
                if biome_candidat == "montagne" or biome_candidat == "neige":
                    bw = random.randint(40, 150)
                else:
                    bw = random.randint(100, 300)
                
                bh = int(bw * random.uniform(0.6, 1.4)) # variation rectangulaire (pas carré)
                
                # On centre le rectangle sur le point temporaire
                final_x, final_y = temp_x - (bw // 2), temp_y - (bh // 2)
                
                self.add_zone(biome_candidat, final_x, final_y, bw, bh)
                zones_placees += 1

    def get_infos_at(self, x, y):
        # On cherche de la dernière zone ajoutée vers la première (logique de calques)
        for b in reversed(self.biomes):
            if b.contains(x, y):
                return b.temperature, b.humidite, b.nom
        
        # Si aucun biome trouvé, c'est le fond
        bg = dico_biomes[self.background_biome]
        return bg["temperature"], bg["humidite"], self.background_biome
    
    def paint(self, surface):
        bg_color = dico_biomes[self.background_biome]["color"]
        surface.fill(bg_color)

        for b in self.biomes:
            b.draw_biome(surface)
    