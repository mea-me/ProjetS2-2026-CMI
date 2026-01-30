import pygame

pygame.init()

screen = pygame.display.set_mode((640, 640), pygame.SCALED)
ufo = pygame.image.load('pygameEntrainnement/ufo.png').convert_alpha()
# chemins = a partir de racine du projet (peu importe le fichier main)
# convert_alpha = transparence

# pixel rendering method : y en a plusieurs
# a regarder selon les besoins


running = True
x = 0
clock = pygame.time.Clock()
dt = 0.1 # delta time, pour gerer les framerate meme si changeant 

font = pygame.font.Font(None, size=100)

while running :
    screen.fill((255, 255, 255))

    # ufo.set_alpha(max(0, 255 - x)) # fade
    screen.blit(ufo, (x, 30))
    
    text = font.render('Le texte', True, (0, 0, 0))
    screen.blit(text, (320, 0)) # text kibouge pas

    hitbox = pygame.Rect(x, 30, ufo.get_width(), ufo.get_height())
    target = pygame.Rect(320, 0, text.get_width(), text.get_height())

    collision = hitbox.colliderect(target)
    if collision :
        text = font.render('Hellloo', True, (0, 0, 0))
        screen.blit(text, (320, 0)) 

    
    x += 50 * dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

    dt = clock.tick(60) / 1000 # milisec precision
    dt = max(0.001, min(0.1, dt)) # gérer les cas de bord (0)


pygame.quit()
        