import pygame
import random
from ..genetique.genome import Genome
from src.core.config import W, H, ALLOWED_MASK

def colorize(surface, color):
    colored = surface.copy()
    r, g, b = color
    colored.fill((r, g, b, 255), None, pygame.BLEND_RGBA_MULT)
    return colored

class Individu:       
    def __init__(self, x, y, espece):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 5, 5)
        self.age = 0
        self.energie = 10000 # Par défaut
        self.alive = True
        self.genome = Genome()
        self.id_espece = espece

        self.vx = 0  # vitesse horizontale
        self.vy = 0  # vitesse verticale

        # Cooldown de collision 
        self.collision_cooldown = 0 # temps restant avant nouvelle collision 
        self.collision_delay = 0.5

        self.base_sprite = pygame.image.load("assets/sprites/random.png").convert_alpha()



    def get_position(self):
        return (self.rect.x,self.rect.y)

    def give_genome(self,new_genome):
        self.genome = new_genome

    def update(self):
        # c'est ça qu'on fera a chaque 'tick' de la clock pygame
        self.age += 1
        self.energie -= 0.001 * self.genome.get_val("taille") * self.genome.get_val("vitesse") * self.genome.get_val("masse") # Plus on est gros, plus on consomme

        # if self.energie <= 0:
        #     self.alive = False #bleurgh##

    def draw(self, screen):
        color = self.genome.get_val("couleur")
        sprite = colorize(self.base_sprite, color)

        # redimensionner selon la taille génétique
        taille = self.genome.get_val("taille")
        sprite = pygame.transform.scale(sprite, (taille, taille))

        screen.blit(sprite, self.rect.topleft)


    def craft_individu(self, template_dico=None):
        self.genome.craft_alleles(template_dico)
        

    def give_rect(self,size):
        self.rect = pygame.Rect(self.x, self.y, size, size)

    def get_individu(self):
        pass

    def is_alive(self):
        if self.age >= 900 or self.energie <= 0:
           #if self.energie <= 0:
               #print("mort de faim (la honte)", self.genome.get_val("régime"))
           return False 
        return True

    def collide_with(self,individu2):
        return self.rect.colliderect(individu2.rect)

    def deplacement_random(self): 
        vitesse = self.genome.get_val("vitesse")
        
        nv_x = self.rect.x + random.choice([-vitesse, 0, vitesse])
        nv_y = self.rect.y + random.choice([-vitesse, 0, vitesse])
        
        try:
            if ALLOWED_MASK.get_at((nv_x + self.rect.width//2, nv_y + self.rect.height//2)):
                self.rect.x = nv_x
                self.rect.y = nv_y
        except IndexError:
            pass # si ils sont débilent et essayent d'aller la ou ils ont pas le droit


    # déplacement d'avant

    #def haut(self):
    #    vitesse = self.genome.get_val("vitesse")
    #    self.rect.y -= vitesse 
#
    #def bas(self):
    #    vitesse = self.genome.get_val("vitesse")
    #    self.rect.y += vitesse
#
    #def gauche(self):
    #    vitesse = self.genome.get_val("vitesse")
    #    self.rect.x -= vitesse
#
    #def droite(self):
    #    vitesse = self.genome.get_val("vitesse")
    #    self.rect.x += vitesse
#
    #def get_close(self, x, y):
    #    if x < self.rect.x:
    #        self.gauche()
    #    elif x > self.rect.x:
    #        self.droite()
#
    #    if y < self.rect.y:
    #        self.haut()
    #    elif y > self.rect.y:
    #        self.bas()

    def __repr__(self): 
        return f"Individu :\n{repr(self.genome)}"     