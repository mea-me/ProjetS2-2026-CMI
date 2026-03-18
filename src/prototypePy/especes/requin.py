import pygame
from random import randint,choice
import copy
#from ..__init__ import W, H, ALLOWED_MASK


class Allele:
    def __init__(self, nom:str, al_type:str, req:bool,  valeur,  mutation_rate:int, mutation_step:int,tipe:str,):
        """
        :param al_type: Le type du gène comportement ou physique (ex: C / P)
        :param req: Si l'allèle est obligatoire (basique) ou pas (ex : vitesse)
        :param nom: Le nom du gène (ex: "vitesse")
        :param valeur_base: La valeur numérique (ex: 50) ou booléenne 
        :param mutation_rate: Chance de muter à chaque génération (en %)
        :param mutation_step: De combien ça change si ça mute (ex: +/- 2)
        """
        self.al_type = al_type
        self.req = req
        self.nom = nom
        self.valeur = valeur
        self.mutation_rate = mutation_rate
        self.mutation_step = mutation_step
        self.type = tipe

    def __repr__(self):
        # formater le print
        return f"[{self.nom}: {self.valeur}]" 

class Genome:
    def __init__(self):
        self.alleles = [] # liste d'objets Allele

    def add_allele(self, allele):
        self.alleles.append(allele)

    def get_val(self, nom_allele):
        #  récupérer une valeur par son nom d'allele
        for a in self.alleles:
            if a.nom == nom_allele:
                return a.valeur
        return 1 # code d'erreur si echec

    def muter(self):
        """Applique potentiellement une mutation (sur chaque allèle)"""
        for gene in self.alleles:
            if isinstance(gene.valeur, int) and randint(1, 99) < gene.mutation_rate:  # si mutation

                gene.valeur += randint(-gene.mutation_step, gene.mutation_step)
                
                if gene.valeur < 1: 
                    gene.valeur = 1 # borne anti négative (genre vitesse négative pas possible)

            elif isinstance(gene.valeur, list) and randint(1, 99) < gene.mutation_rate:
                for i in range(len(gene.valeur)):
                    gene.valeur[i] += randint(-gene.mutation_step, gene.mutation_step)

                    if gene.valeur[i] < 0: 
                        gene.valeur[i] += 255 # borne anti négative (genre vitesse négative pas possible)

                    elif gene.valeur[i] > 255: 
                        gene.valeur[i] -= 255 # borne anti positron (genre vitesse négative pas possible)

    def __repr__(self):
        # formater le print
        li = ""
        for a in self.alleles :
            li += f'{str(a)};\n '
        return f'Genome({li[:-2]})'
    
    def craft_alleles(self):
        for key,value in dico_alleles.items():
            if value[1]:
                if value[5] == "int":
                    self.add_allele(Allele(key,value[0],True,randint(value[2][0],value[2][1]),randint(0,100),randint(value[3][0],value[3][1]),value[5]))

                if value[5] == "str":
                    self.add_allele(Allele(key,value[0],True,choice(value[2]),randint(0,100),value[3],value[5]))
                    
                if key == "couleur":
                    self.add_allele(Allele("couleur","P",True,[randint(160,200),randint(180,200),randint(185,210)],randint(0,100),randint(value[3][0],value[3][1]),value[5]))

    def show_alleles(self):
        for i in self.alleles:
            for y in i:
                print(y)
                
    def clone(self):
        return copy.deepcopy(self)
    

class Individu:       
    def __init__(self, x, y, espece):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 5, 5)
        self.age = 0
        self.energie = 100 # Par défaut
        self.alive = True
        self.genome = Genome()
        self.id_espece = espece

        # Cooldown de collision 
        self.collision_cooldown = 0 # temps restant avant nouvelle collision 
        self.collision_delay = 0.5


    def get_position(self):
        return (self.rect.x,self.rect.y)

    def give_genome(self,new_genome):
        self.genome = new_genome

    def update(self):
        # c'est ça qu'on fera a chaque 'tick' de la clock pygame
        self.age += 1
        self.energie -= 0.1 * self.genome.get_val("taille") # Plus on est gros, plus on consomme

        if self.energie <= 0:
            self.alive = False #bleurgh##

    def draw(self,screen):
        pygame.draw.rect(screen, self.genome.get_val("couleur"), self.rect)
        #screen.blit(self.image, self.rect.topleft)

    def craft_individu(self):
        self.genome.craft_alleles()
        

    def give_rect(self,size):
        self.rect = pygame.Rect(self.x, self.y, size, size)

    def get_individu(self):
        pass

    def is_alive(self):
        if self.age >= 900:
           return False 
        return True

    def collide_with(self,individu2):
        return self.rect.colliderect(individu2.rect)

    def deplacement_random(self): 
        vitesse = self.genome.get_val("vitesse")
        
        nv_x = self.rect.x + choice([-vitesse, 0, vitesse])
        nv_y = self.rect.y + choice([-vitesse, 0, vitesse])
        self.rect.x = nv_x
        self.rect.y = nv_y

    def haut(self):
        vitesse = self.genome.get_val("vitesse")
        self.rect.y -= vitesse 

    def bas(self):
        vitesse = self.genome.get_val("vitesse")
        self.rect.y += vitesse

    def gauche(self):
        vitesse = self.genome.get_val("vitesse")
        self.rect.x -= vitesse

    def droite(self):
        vitesse = self.genome.get_val("vitesse")
        self.rect.x += vitesse

    def get_close(self,x,y):
        if x < self.x:
            self.gauche()
        elif x > self.x:
            self.droite()

        if y < self.y:
            self.haut()
        elif y > self.y:
            self.bas()

    def __repr__(self): 
        return f"Individu :\n{repr(self.genome)}"  # la aussi c'est une idée 
    
    def __del__(self):
        pass

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
        self.couleur = self.genome.get_val("couleur")

    def draw(self, screen):
        pygame.draw.rect(screen, self.couleur, self.rect)


dico_alleles = {
#           0        1     2                3          4        5
# "nom" : [al_type, req, valeur (écart), mutStep, description, type]
"vitesse" : ["P",True,(3,7), (1, 3), "La vitesse de déplacement de l'individu (0-100)", "int"],
"masse" : ["P",True,(150,450), (1, 5), "La masse de l'individu (0-100)", "int"],
"taille" : ["P",True,(20,45), (1, 5), "La taille de l'individu (0-100)", "int"],
"régime" : ["P", True, ["carnivore"], None, "Le régime alimentaire de l'individu (carnivore ou omnivore ou herbivore)", "str"],
"couleur" : ["P",True,"couleur pas accéder", (1, 25), "La couleur de l'individu (RGB)", "list"],
"agilité" : ["P",True,(60,100), (1, 5), "L'agilité de l'individu (résistance au terrain escarpé)", "int"],
# climatoseptikPoP
"température" : ["P",True,(15,16), (1, 3), "La vitesse de déplacement de l'individu (0-100)", "int"],
"humidité" : ["P",True,(0,100), (1, 5), "La vitesse de déplacement de l'individu (0-100)", "int"],

"aggréssivité" : ["C",True,(40,75), (1, 5), "Le taux d'aggresivité de l'individu (0-100)", "int", True],
"fertilité" : ["C",True,(0,40), (1, 5), "Le taux de fertilité de l'individu (0-100)", "int", True],
"adaptabilité" : ["C",True,(0,20), (1, 5), "Le taux d'adaptabilité de l'individu (0-100)", "int", True],
"perception" : ["C",True,(55,75), (1, 5), "La distance à laquelle il peut voir", "int", True]
}