import pygame

class Hub:

    def __init__(self, font, color):
        self.font = font
        self.color = color

    def draw(self, screen, fps, targets, angle):

        screen.blit(
            self.font.render(f"FPS : {fps}", True, self.color),
            (15, 15)
        )

        screen.blit(
            self.font.render(f"TARGETS : {targets}", True, self.color),
            (15, 40)
        )

        screen.blit(
            self.font.render(f"ANGLE : {int(angle)}", True, self.color),
            (15, 65)
        )

        screen.blit(
            self.font.render("LOCK : NONE", True, self.color),
            (15, 90)
        )

        screen.blit(
            self.font.render("STATUS : ONLINE", True, self.color),
            (15, 115)
        )