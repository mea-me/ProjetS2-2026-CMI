import pygame

class InfoPanel:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20)

    def draw(self, indi, world):
        W, H = self.screen.get_size()

        # Fond du panneau
        pygame.draw.rect(self.screen, (30, 30, 30), (W - 300, 0, 300, H))
        pygame.draw.rect(self.screen, (200, 200, 200), (W - 300, 0, 300, H), 2)

        y = 20

        def write(text):
            nonlocal y
            surf = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(surf, (W - 280, y))
            y += 30

        write("=== Individu ===")
        write(f"ID : George")
        write(f"Espèce : grenouille")

        # Caractéristiques génétiques
        write("")
        write("=== Génome ===")
        for allele in indi.genome.alleles:
            write(f"{allele.nom} : {allele.valeur}")

        # Biome
        temp, hum, biome = world.get_infos_at(indi.x, indi.y)
        write("")
        write("=== Biome ===")
        write(f"Type : {biome}")
        write(f"Temp : {temp}°C")
        write(f"Hum : {hum}%")

        # Âge
        write("")
        write("=== Âge ===")
        write(f"{round(indi.age/60, 1)} ans")
