import pygame
from src.simulation.entites.individu import Individu
from src.simulation.genetique.genome import Genome

blob_alleles = {
    "vitesse": ["P", True, (1, 4), (1, 2), "", "int"],
    "masse": ["P", True, (50, 200), (1, 5), "", "int"],
    "taille": ["P", True, (15, 35), (1, 5), "", "int"],
    "régime": ["P", True, ["omnivore"], None, "", "str"],
    "couleur": ["P", True, "couleur", (1, 25), "", "list"],
    "agilité": ["P", True, (20, 60), (1, 5), "", "int"],
    "température": ["P", True, (5, 25), (1, 3), "", "int"],
    "humidité": ["P", True, (40, 100), (1, 5), "", "int"],
    "aggréssivité": ["C", True, (0, 40), (1, 5), "", "int"],
    "fertilité": ["C", True, (50, 100), (1, 5), "", "int"],
    "adaptabilité": ["C", True, (60, 100), (1, 5), "", "int"],
    "perception": ["C", True, (20, 50), (1, 5), "", "int"]
}

class Blob(Individu):
    def __init__(self, x, y):
        super().__init__(x, y, espece="blob") # init via l'init de sa classe parente

        self.genome = Genome()
        self.genome.craft_alleles(blob_alleles)

        taille = self.genome.get_val("taille")
        self.rect = pygame.Rect(x, y, taille, taille)

        self.vx = 0
        self.vy = 0

        self.couleur = [255, 255, 102]
        self.base_sprite = pygame.image.load("assets/sprites/blob.png").convert_alpha()

# ============================================================================

dragon_alleles = {
    "vitesse": ["P", True, (4, 9), (1, 3), "", "int"],
    "masse": ["P", True, (200, 500), (1, 5), "", "int"],
    "taille": ["P", True, (30, 60), (1, 5), "", "int"],
    "régime": ["P", True, ["carnivore"], None, "", "str"],
    "couleur": ["P", True, "couleur", (1, 25), "", "list"],
    "agilité": ["P", True, (40, 80), (1, 5), "", "int"],
    "température": ["P", True, (30, 50), (1, 3), "", "int"],
    "humidité": ["P", True, (0, 40), (1, 5), "", "int"],
    "aggréssivité": ["C", True, (60, 100), (1, 5), "", "int"],
    "fertilité": ["C", True, (10, 40), (1, 5), "", "int"],
    "adaptabilité": ["C", True, (20, 50), (1, 5), "", "int"],
    "perception": ["C", True, (70, 100), (1, 5), "", "int"]
}

class Dragon(Individu):
    def __init__(self, x, y):
        super().__init__(x, y, espece="dragon")

        self.genome = Genome()
        self.genome.craft_alleles(dragon_alleles)

        taille = self.genome.get_val("taille")
        self.rect = pygame.Rect(x, y, taille, taille)

        self.vx = 0
        self.vy = 0

        self.couleur = [255, 34, 51]  # rouge feu
        self.base_sprite = pygame.image.load("assets/sprites/dragon.png").convert_alpha()


# ============================================================================


licorne_alleles = {
    "vitesse" : ["P",True,(6, 12), (1, 3), "La vitesse de déplacement de l'individu (0-100)", "int"],
    "masse" : ["P",True,(80, 150), (1, 5), "La masse de l'individu (0-100)", "int"],
    "taille" : ["P",True,(25, 40), (1, 5), "La taille de l'individu (0-100)", "int"],
    "régime" : ["P", True, ["herbivore"], None, "Le régime alimentaire de l'individu (carnivore ou omnivore ou herbivore)", "str"],
    "couleur" : ["P",True, None, (1, 25), "La couleur de l'individu (RGB)", "list"],
    "agilité" : ["P",True,(70,100), (1, 5), "L'agilité de l'individu (résistance au terrain escarpé)", "int"],
    "température" : ["P",True,(10,20), (1, 3), "La vitesse de déplacement de l'individu (0-100)", "int"],
    "humidité" : ["P",True,(20,80), (1, 5), "La vitesse de déplacement de l'individu (0-100)", "int"],
    "aggréssivité" : ["C",True,(0,20), (1, 5), "Le taux d'aggresivité de l'individu (0-100)", "int", True],
    "fertilité" : ["C",True,(40,80), (1, 5), "Le taux de fertilité de l'individu (0-100)", "int", True],
    "adaptabilité" : ["C",True,(40,80), (1, 5), "Le taux d'adaptabilité de l'individu (0-100)", "int", True],
    "perception" : ["C",True,(60,90), (1, 5), "La distance à laquelle il peut voir", "int", True]
}


class Licorne(Individu):
    def __init__(self, x, y):
        super().__init__(x, y, espece="licorne")

        self.genome = Genome()
        self.genome.craft_alleles(licorne_alleles)  

        taille = self.genome.get_val("taille")
        self.rect = pygame.Rect(x, y, taille, taille)

        self.vx = 0 
        self.vy = 0  

        self.couleur = [191, 60, 219]
        self.base_sprite = pygame.image.load("assets/sprites/licorne.png").convert_alpha()

# ============================================================================

dico_alleles = {
    "vitesse" : ["P",True,(3,7), (1, 3), "La vitesse de déplacement de l'individu (0-100)", "int"],
    "masse" : ["P",True,(150,450), (1, 5), "La masse de l'individu (0-100)", "int"],
    "taille" : ["P",True,(20,45), (1, 5), "La taille de l'individu (0-100)", "int"],
    "régime" : ["P", True, ["carnivore"], None, "Le régime alimentaire de l'individu (carnivore ou omnivore ou herbivore)", "str"],
    "couleur" : ["P",True, None, (1, 25), "La couleur de l'individu (RGB)", "list"],
    "agilité" : ["P",True,(60,100), (1, 5), "L'agilité de l'individu (résistance au terrain escarpé)", "int"],
    "température" : ["P",True,(15,16), (1, 3), "La vitesse de déplacement de l'individu (0-100)", "int"],
    "humidité" : ["P",True,(0,100), (1, 5), "La vitesse de déplacement de l'individu (0-100)", "int"],
    "aggréssivité" : ["C",True,(40,75), (1, 5), "Le taux d'aggresivité de l'individu (0-100)", "int", True],
    "fertilité" : ["C",True,(0,40), (1, 5), "Le taux de fertilité de l'individu (0-100)", "int", True],
    "adaptabilité" : ["C",True,(0,20), (1, 5), "Le taux d'adaptabilité de l'individu (0-100)", "int", True],
    "perception" : ["C",True,(55,75), (1, 5), "La distance à laquelle il peut voir", "int", True]
}

class Requin(Individu):
    def __init__(self, x, y):
        super().__init__(x, y, espece="requin")

        # Génome du requin
        self.genome = Genome()
        self.genome.craft_alleles()  # génère les stats selon dico_alleles

        # Taille du requin selon son gène "taille"
        taille = self.genome.get_val("taille")
        self.rect = pygame.Rect(x, y, taille, taille)

        self.vx = 0  # vitesse horizontale
        self.vy = 0  # vitesse verticale

        # Couleur du requin
        self.couleur = [2, 69, 95]
        self.base_sprite = pygame.image.load("assets/sprites/requin.png").convert_alpha()

# ============================================================================

sylveon_alleles = {
    "vitesse": ["P", True, (2, 6), (1, 3), "", "int"],
    "masse": ["P", True, (80, 200), (1, 5), "", "int"],
    "taille": ["P", True, (20, 40), (1, 5), "", "int"],
    "régime": ["P", True, ["herbivore"], None, "", "str"],
    "couleur": ["P", True, None, (1, 25), "", "list"],
    "agilité": ["P", True, (40, 80), (1, 5), "", "int"],
    "température": ["P", True, (5, 25), (1, 3), "", "int"],
    "humidité": ["P", True, (50, 100), (1, 5), "", "int"],
    "aggréssivité": ["C", True, (0, 30), (1, 5), "", "int"],
    "fertilité": ["C", True, (50, 100), (1, 5), "", "int"],
    "adaptabilité": ["C", True, (60, 100), (1, 5), "", "int"],
    "perception": ["C", True, (40, 80), (1, 5), "", "int"]
}

class Sylveon(Individu):
    def __init__(self, x, y):
        super().__init__(x, y, espece="sylveon")

        self.genome = Genome()
        self.genome.craft_alleles()

        taille = self.genome.get_val("taille")
        self.rect = pygame.Rect(x, y, taille, taille)

        self.vx = 0
        self.vy = 0

        self.couleur = self.genome.get_val("couleur")
        self.base_sprite = pygame.image.load("assets/sprites/sylveon.png").convert_alpha()