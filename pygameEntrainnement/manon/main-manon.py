import pygame
import random
import copy

pygame.init()

WIDTH, HEIGHT= 800, 600
SIZE = 20
FPS = 10

NOIR = (0,0,0)
BLANC = (255,255,255)
GRIS = (50,50,50)

COLS = WIDTH // SIZE
ROWS = HEIGHT // SIZE

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Jeu de la Vie")

""" image
img_fall = pygame.image.load(".\pygameEntrainnement\manon\char.webp").convert()
img_fall = pygame.transform.scale(img_fall, 
                                  (img_fall.get_width() * 0.5,
                                   img_fall.get_height() * 0.5))

running = True
x=0
clock = pygame.time.Clock()

d_t = 0.1

while running:
    screen.fill(BLANC)

    screen.blit(img_fall, (x, 30))
    x += 60 * d_t

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

    d_t = clock.tick(60) / 1000
    d_t = max(0.001, min(0.1, d_t))

pygame.quit()"""

def create_grid():
    return [[random.choice([0,1]) for _ in range(COLS)] for _ in range(ROWS)]


def show_grid(grid):
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x]:
                rect = pygame.Rect(x*SIZE, y*SIZE, SIZE, SIZE)
                pygame.draw.rect(screen, BLANC, rect)


def count_neighbors(grid, x, y):
    count = 0
    # On regarde les 9 cases autour (de -1 à +1)
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue # On ignore la cellule elle-même
            
            # Le modulo % permet de gérer les bords (effet Pacman)
            col = (x + j + COLS) % COLS
            row = (y + i + ROWS) % ROWS
            count += grid[row][col]
    return count


def update_grid(grid):
    # IMPORTANT : On travaille sur une copie pour ne pas fausser les calculs en cours
    new_grid = copy.deepcopy(grid)
    
    for y in range(ROWS):
        for x in range(COLS):
            neighbors = count_neighbors(grid, x, y)
            state = grid[y][x]
            
            if state == 1:
                # Règle : Meurt si moins de 2 voisins (solitude) ou plus de 3 (surpopulation)
                if neighbors < 2 or neighbors > 3:
                    new_grid[y][x] = 0
            else:
                # Règle : Naît si exactement 3 voisins
                if neighbors == 3:
                    new_grid[y][x] = 1
                    
    return new_grid


grid = create_grid()
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(NOIR)

    show_grid(grid)
    grid = update_grid(grid)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
