import pygame
import random
from .genome import Genome

class Individu:       # class qui va probablment beauuucoup changer
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

        #self.image = pygame.image.load("pygameEntrainnement/ufo.png").convert_alpha() 
        #self.image = pygame.transform.scale(self.image, (size,size))


    def get_position(self):
        return (self.rect.x,self.rect.y)

    def give_genome(self,new_genome):
        self.genome = new_genome

    def update(self):
        # c'est ça qu'on fera a chaque 'tick' de la clock pygame
        self.age += 1
        self.energie -= 0.1 * self.genome.get_val("taille") # Plus on est gros, plus on consomme
        
        """if self.energie <= 0:
            self.is_alive = False #bleurgh"""

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

    def deplacement(self): 
        vitesse = self.genome.get_val("vitesse")

        self.rect.x += random.choice([-vitesse, 0, vitesse])
        self.rect.y += random.choice([-vitesse, 0, vitesse])

        # Empêche automatiquement de sortir de l'écran
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

    def __repr__(self): 
        return f"Individu :\n{repr(self.genome)}"  # la aussi c'est une idée 
    
    def __del__(self):
        pass
    

    