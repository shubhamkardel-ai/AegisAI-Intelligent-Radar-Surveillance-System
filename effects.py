import pygame
from settings import WIDTH, HEIGHT, GREEN

class Effects:

    def __init__(self):
        pass

    def draw_glow(self, screen):

        CENTER = (WIDTH // 2, HEIGHT // 2)

        for radius in range(25, 0, -3):
            alpha = radius * 8

            glow = pygame.Surface((60, 60), pygame.SRCALPHA)

            pygame.draw.circle(
                glow,
                (*GREEN, alpha),
                (30, 30),
                radius
            )

            screen.blit(
                glow,
                (CENTER[0] - 30, CENTER[1] - 30)
            )

            pygame.draw.circle(
                screen,
                GREEN,
                CENTER,
                radius
            )

    def draw_trails(self, screen):
        pass

    def draw_scan_lines(self, screen):
        for y in range(0, 800, 4):
            pygame.draw.line(
                screen,
                (0, 25, 0),
                (0, y),
                (1000, y)
            )

    def draw_noise(self, screen):
        pass

    def draw_bloom(self, screen):
        pass