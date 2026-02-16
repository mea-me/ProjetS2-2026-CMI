import pygame

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


# Format : "nom": {"temperature": T, "humidite": H, "color": (R, G, B)}
dico_biomes = {
    "foret":    {"temperature": 25, "humidite": 80,  "color": (34, 139, 34)},   # Vert Fonc
    "plaine":   {"temperature": 15, "humidite": 30,  "color": (144, 238, 144)}, # Vert Clair
    "ocean":    {"temperature": 10, "humidite": 100, "color": (30, 144, 255)},  # Bleu
    "desert":   {"temperature": 40, "humidite": 0,   "color": (237, 201, 175)}, # Sable
    "montagne": {"temperature": -5, "humidite": 20,  "color": (128, 128, 128)}, # Gris
    "neige":    {"temperature": -20, "humidite": 60, "color": (255, 250, 250)}  # Blanc
}


class WorldMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.biomes = [] # liste d'objets Biome
        self.background_biome = "plaine"

    def add_zone(self, nom, x, y, width, height): # add a la liste de biomes
        self.biomes.append(Biome(nom, x, y, width, height))

    def get_infos_at(self, x, y):
        # On cherche de la dernière zone ajoutée vers la première (logique de calques)
        for b in reversed(self.biomes):
            if b.contains(x, y):
                return b.temperature, b.humidite, b.nom
        
        # Si aucun biome trouvé, c'est le fond
        bg = dico_biomes[self.background_biome]
        return bg["temperature"], bg["humidite"], self.background_biome
    
    def paint(self, surface):
        # fond
        bg_color = dico_biomes[self.background_biome]["color"]
        surface.fill(bg_color)

        # faire les autres layers
        for b in self.biomes:
            b.draw_biome(surface)
