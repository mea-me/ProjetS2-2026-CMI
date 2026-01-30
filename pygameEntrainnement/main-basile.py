import pygame
from pygame.locals import *
import time
import math


def jeu_de_la_vie(T):
    #Une cellule vivante reste vivante si elle a 2 ou 3 voisines vivantes.
    #Une cellule vivante meurt si elle a moins de 2 voisines vivantes.
    #Une cellule vivante meurt si elle a plus de 3 voisines vivantes.
    #Une cellule morte devient vivante si elle a exactement 3 voisines vivantes
    rows = len(T)
    cols = len(T[0])    

    # Nouvelle grille vide
    new_T = [[0 for _ in range(cols)] for _ in range(rows)]

    # Fonction pour compter les voisines vivantes
    def count_neighbors(r, c):
        count = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue  # on ignore la cellule elle-même
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    count += T[nr][nc]
        return count

    # Application des règles
    for r in range(rows):
        for c in range(cols):
            neighbors = count_neighbors(r, c)

            if T[r][c] == 1:
                # Cellule vivante
                if neighbors == 2 or neighbors == 3:
                    new_T[r][c] = 1
                else:
                    new_T[r][c] = 0
            else:
                # Cellule morte
                if neighbors == 3:
                    new_T[r][c] = 1

    return new_T



# --- Paramètres ---
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 30

# Exemple de grille (à remplacer par ton tableau)
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

grid[3][4]=1
grid[3][5]=1
grid[3][6]=1

grid[5][4]=1
grid[6][5]=1
grid[7][3]=1
grid[7][4]=1
grid[7][5]=1

print(grid)

pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
clock = pygame.time.Clock()

def act_screen(screen,grid):
    screen.fill((20, 20, 20))
    # --- Affichage de la grille ---
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = (255, 255, 255) if grid[y][x] == 1 else (60, 60, 60)
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
            # Optionnel : dessiner les lignes de la grille
            pygame.draw.rect(screen, (30, 30, 30), rect, 1)
    
running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN: #mettre en pause appuyant sur entré
            if event.key == pygame.K_RETURN:
                paused = not(paused)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mp = pygame.mouse.get_pos()
            mix = math.floor(mp[0]/20)
            miy = math.floor(mp[1]/20)
            if grid[miy][mix] == 1: #Si la cellule vivante elle meurt ect
                grid[miy][mix] = 0
            else:
                grid[miy][mix] = 1
            act_screen(screen,grid)
            pygame.display.flip()

    if paused:                
        act_screen(screen,grid)
        time.sleep(0.2)
        grid = jeu_de_la_vie(grid)
        pygame.display.flip()
        clock.tick(60)

pygame.quit()