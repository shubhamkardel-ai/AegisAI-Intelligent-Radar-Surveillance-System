import pygame
from settings import FRIENDLY, ENEMY, CIVILIAN, UNKNOWN, HEIGHT, WIDTH

class Aircraft:

    def __init__(self, x, y, vx, vy, aircraft_type):

        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.type = aircraft_type

        self.id = ""

        if self.type == "Friendly":
            self.color = FRIENDLY
        elif self.type == "Enemy":
            self.color = ENEMY
        elif self.type == "Civilian":
            self.color = CIVILIAN
        else:
            self.color = UNKNOWN

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # Bounce from screen edges
        if self.x <= 0 or self.x >= WIDTH:
            self.vx *= -1
        if self.y <= 0 or self.y >= HEIGHT:
            self.vy *= -1

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            5
        )

        font = pygame.font.SysFont("Consolas", 12)

        text = font.render(
            self.id,
            True,
            self.color
        )

        screen.blit(
            text,
            (int(self.x) + 8, int(self.y) - 8)
        )
