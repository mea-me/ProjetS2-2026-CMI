import pygame

class Button:
    def __init__(self, x, y, w, h, text, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont("Arial", 22)

    def draw(self, screen):
        pygame.draw.rect(screen, (40,40,40), self.rect)
        pygame.draw.rect(screen, (200,200,200), self.rect, 2)
        txt = self.font.render(self.text, True, (255,255,255))
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 8))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()


class Menu:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state

        W, H = screen.get_size()

        self.buttons = [
            Button(20, 75, 160, 40, "Pause / Play", self.toggle_pause),
            Button(20, 125, 160, 40, "Vitesse x1", self.speed_x1),
            Button(20, 175, 160, 40, "Vitesse x2", self.speed_x2),
            Button(20, 225, 160, 40, "+20 ans", self.skip_time),
            Button(20, 275, 160, 40, "Reset", self.reset_game),
            Button(20, 325, 160, 40, "Quitter", self.quit_game)
            
        ]

        self.button_start = [
            Button(20, 75, 160, 40, "Pause / Play", self.toggle_pause),
            Button(20, 125, 160, 40, "Vitesse x1", self.speed_x1),
            Button(20, 175, 160, 40, "Vitesse x2", self.speed_x2),
            Button(20, 225, 160, 40, "+20 ans", self.skip_time),
            Button(20, 275, 160, 40, "Reset", self.reset_game),
            Button(20, 325, 160, 40, "Quitter", self.quit_game)
        ]



    def toggle_pause(self):
        self.game_state["paused"] = not self.game_state["paused"]

    def speed_x1(self):
        self.game_state["speed"] = 1

    def speed_x2(self):
        self.game_state["speed"] = 2

    def skip_time(self):
        self.game_state["skip"] = 20 * 60  # 100 ans

    def quit_game(self):
        self.game_state["running"] = False

    def reset_game(self):
        self.game_state["reset"] = True


    def draw(self):
        for b in self.buttons:
            b.draw(self.screen)

    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)

    def draw_start(self):
        for b in self.buttons_start:
            b.draw(self.screen)

    def handle_event_start(self, event):
        for b in self.buttons_start:
            b.handle_event(event)
