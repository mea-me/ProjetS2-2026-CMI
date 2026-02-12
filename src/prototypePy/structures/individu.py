import pygame
import random
from genome import Genome

class Individu:       # class qui va probablment beauuucoup changer
    def __init__(self, x, y, size):
        # width et height sont la taille de l'objet
        self.rect = pygame.Rect(x, y, size, size)
        self.age = 0
        self.energie = 100 # Par défaut
        self.is_alive = True
        self.genome = Genome()

        #self.image = pygame.image.load("pygameEntrainnement/ufo.png").convert_alpha() 
        #self.image = pygame.transform.scale(self.image, (size,size))


    def get_position(self):
        return (self.rect.x,self.rect.y)

    def update(self):
        # c'est ça qu'on fera a chaque 'tick' de la clock pygame
        self.age += 1/360 
        self.energie -= 0.1 * self.genome.get_val("taille") # Plus on est gros, plus on consomme
        
        if self.energie <= 0:
            self.is_alive = False #bleurgh

    def draw(self,screen):
        pygame.draw.rect(screen, self.genome.get_val("couleur"), self.rect)
        #screen.blit(self.image, self.rect.topleft)

    def craft_individu(self):
        self.genome.craft_alleles()

    def get_individu(self):
        pass

    def deplacement(self):
        vitesse = self.genome.get_val("vitesse") 
        # X peut être -vitesse, 0 ou +vitesse
        if self.rect.x > vitesse and self.rect.x < pygame.display.Info().current_w + vitesse:
            self.rect.x += random.choice([-vitesse, 0, vitesse])
        elif self.rect.x > vitesse:
            self.rect.x += random.choice([-vitesse,0])
        else:
            self.rect.x += random.choice([vitesse,0])
        # Y peut être -vitesse, 0 ou +vitesse
        if self.rect.y > vitesse and self.rect.y < pygame.display.Info().current_h + vitesse:
            self.rect.y += random.choice([-vitesse, 0, vitesse])
        elif self.rect.y > vitesse:
            self.rect.y += random.choice([-vitesse,0])
        else:
            self.rect.y += random.choice([vitesse,0])


    def __repr__(self): 
        return f"Individu :\n{repr(self.genome)}"  # la aussi c'est une idée 
    

    