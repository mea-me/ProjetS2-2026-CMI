import pygame, random

pygame.init()

screen = pygame.display.set_mode((650, 650))
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

tableautest = []
for i in range(5):
    tableautest.append([])
    for I in range(5):
        tableautest[i].append(random.randint(0,1))

print(tableautest)
print("")
print(jeu_de_la_vie(tableautest))


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    pygame.display.flip()

    # limits FPS to 30
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(30) / 1000


pygame.quit()