import pygame

class Plante:
    def __init__(self, x, y, energie, age):
        self.x = x 
        self.y = y
        self.energie = energie
        self.age = age
        self.alive = True

        self.rect = pygame.Rect(x, y, 5, 5)

    def draw(self,screen):
        pygame.draw.rect(screen, (0,255,0), self.rect)
        #screen.blit(self.image, self.rect.topleft)


    def grow(self):
        if self.age > 180:
            print("test")
            self.energie += 100

    def manger(self):
        # pour quand un animal la mange
        if self.alive:
            e = self.energie
            self.energie = 0
            self.alive = False
            return e
        return 0

Liste_plantes = []