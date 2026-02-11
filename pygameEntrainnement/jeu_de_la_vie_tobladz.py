import pygame, random, os

pygame.init()

screen_h = 0.95*pygame.display.Info().current_h
screen_w = screen_h
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
running = True
dt = 0


def jeu_de_la_vie(tableau):
    #initialisation rendu
    rendu = []
    for i in range(len(tableau)):
        rendu.append([])
        for I in range(len(tableau[0])):
            rendu[i].append(0)
    
    #check du centre
    for i in range(1,len(tableau)-1):
        for I in range(1,len(tableau[0])-1):
            s = 0
            for it in range(3):
                for IT in range(3):
                    if tableau[i+it-1][I+IT-1] == 1 and (it,IT) != (1,1):
                        s += 1
            
            if s == 3:
                rendu[i][I] = 1
            
            elif tableau[i][I] == 1 and s == 2:
                rendu[i][I] = 1
    
    #check des bords(coins exclus)
    for i in range(1,len(tableau[0])-1):
        s = 0
        s2 = 0
        for it in range(3):
            if tableau[0][i + it - 1] == 1 and it != 1:
                s += 1
            if tableau[1][i + it - 1] == 1:
                s += 1

            if tableau[len(tableau)-1][i + it - 1] == 1 and it != 1:
                s2 += 1
            if tableau[len(tableau)-2][i + it - 1] == 1:
                s2 += 1
        
        if s == 3:
            rendu[0][i] = 1
        elif tableau[0][i] == 1 and s == 2:
            rendu[0][i] = 1
        
        if s2 == 3:
            rendu[len(tableau)-1][i] = 1
        elif tableau[len(tableau)-1][i] == 1 and s2 == 2:
            rendu[len(tableau)-1][i] = 1
    
    for i in range(1,len(tableau)-1):
        s = 0
        s2 = 0
        for it in range(3):
            if tableau[i + it - 1][0] == 1 and it != 1:
                s += 1
            if tableau[i + it - 1][1] == 1:
                s += 1

            if tableau[i + it - 1][len(tableau)-1] == 1 and it != 1:
                s2 += 1
            if tableau[i + it - 1][len(tableau)-2] == 1:
                s2 += 1
        
        if s == 3:
            rendu[i][0] = 1
        elif tableau[i][0] == 1 and s == 2:
            rendu[i][0] = 1

        if s2 == 3:
            rendu[i][len(tableau)-1] = 1
        elif tableau[i][len(tableau)-1] == 1 and s2 == 2:
            rendu[i][len(tableau)-1]

    #check des coins
    s = 0
    if tableau[0][1] == 1:
        s +=1
    if tableau[1][1] == 1:
        s += 1
    if tableau[1][0] == 1:
        s += 1
    
    if s == 3:
        rendu[0][0] = 1
    elif s == 2 and tableau[0][0] == 1:
        rendu[0][0] = 1
    
    s = 0
    if tableau[0][len(tableau)-2] == 1:
        s +=1
    if tableau[1][len(tableau)-2] == 1:
        s += 1
    if tableau[1][len(tableau)-1] == 1:
        s += 1
    
    if s == 3:
        rendu[0][len(tableau)-1] = 1
    elif s == 2 and tableau[0][len(tableau)-1] == 1:
        rendu[0][len(tableau)-1] = 1

    s = 0
    if tableau[len(tableau)-1][1] == 1:
        s +=1
    if tableau[len(tableau)-2][1] == 1:
        s += 1
    if tableau[len(tableau)-2][0] == 1:
        s += 1
    
    if s == 3:
        rendu[len(tableau)-1][0] = 1
    elif s == 2 and tableau[len(tableau)-1][0] == 1:
        rendu[len(tableau)-1][0] = 1

    if s == 3:
        rendu[0][len(tableau)-1] = 1
    elif s == 2 and tableau[0][len(tableau)-1] == 1:
        rendu[0][len(tableau)-1] = 1

    s = 0
    if tableau[len(tableau)-1][len(tableau)-2] == 1:
        s +=1
    if tableau[len(tableau)-2][len(tableau)-2] == 1:
        s += 1
    if tableau[len(tableau)-2][len(tableau)-1] == 1:
        s += 1
    
    if s == 3:
        rendu[len(tableau)-1][len(tableau)-1] = 1
    elif s == 2 and tableau[len(tableau)-1][len(tableau)-1] == 1:
        rendu[len(tableau)-1][len(tableau)-1] = 1

    
    return rendu

n = 150
tableautest = []
for i in range(n):
    tableautest.append([])
    for I in range(n):
        tableautest[i].append(random.randint(0,1))

t = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    for i in range(len(tableautest)):
        for I in range(len(tableautest[0])):
            if tableautest[i][I] == 1:
                #screen.blit(pygame.transform.scale(pygame.image.load(os.path.join("pygameEntrainnement","carr_blanc.png")), (650/n,650/n)).convert_alpha(),pygame.transform.scale(pygame.image.load(os.path.join("pygameEntrainnement","carr_blanc.png")), (650/n,650/n)).convert_alpha().get_rect(topleft=((650/n)*i, (650/n)*I)))
                pygame.draw.rect(screen,(255,255,255),pygame.Rect(i*(screen_w/n),I*(screen_h/n),screen_w/n,screen_h/n))

    t+=1

    if t == 30:
        tableautest = jeu_de_la_vie(tableautest)
        t = 0

    pygame.display.flip()

    # limits FPS to 30
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000


pygame.quit()