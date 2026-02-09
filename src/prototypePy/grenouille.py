import pygame
from random import randint

milieu_dico = {"marre":((x,y),(x,y))}
class Grenouille(pygame.sprite.Sprite):
    def __init__(self,x,y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha() #charge l'image
        self.predation = 4 #indice de prédation/position dans la chaines alimentaire
        self.fertilite = 3 #indice de fertilité de l'éspèce
        self.milieu_pref = "marre" #indique sont milieu pref
        self.rect = self.image.get_rect() #récupere donner de l'image sur l'écran
        self.rect.x = x #récupère la position x
        self.rect.y = y #récupère la position y
        self.milieu = milieu_dico.key if (self.rect.x,self.rect.y) in milieu_dico.values
        #si milieu_pref == milieu => bonus
        
    
    def update(self):
        #met a jour l'objet ?
        pass

    def draw(self,screen):
        screen.blit(self.image, self.rect)