#Même vide, ce fichier dit à Python :
#➡️ “Ce dossier est un module importable”.
#D'après copilot

import pygame
pygame.init()

info = pygame.display.Info()
W, H = info.current_w, info.current_h

#ellipse
mask_surface = pygame.Surface((W, H), pygame.SRCALPHA) # -> SRCALPHA = transparent
mask_surface.fill((0, 0, 0, 0)) # no no zone

overlay = pygame.Surface((W, H)) 
overlay.fill((10, 10, 10)) # Couleur de l'extérieur du globe (gris très foncé/noir)

playable_rect = pygame.Rect(20, 20, W - 40, H - 40) # ellipse magenta qui servira de trou
pygame.draw.ellipse(overlay, (255, 0, 255), playable_rect) 
overlay.set_colorkey((255, 0, 255)) # le magenta = 100% transparent

# Masque de collision (rétréci de 40px de chaque côté)
movement_rect = playable_rect.inflate(-80, -80) 

mask_surface = pygame.Surface((W, H), pygame.SRCALPHA)
# ellipse de déplacement autorisée 
pygame.draw.ellipse(mask_surface, (255, 255, 255, 255), movement_rect)

ALLOWED_MASK = pygame.mask.from_surface(mask_surface)

pygame.quit()