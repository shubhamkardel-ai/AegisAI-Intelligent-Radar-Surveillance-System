import pygame
import math
import random
import sound
from settings import *
from aircraft import Aircraft
from radar import Radar
from hub import Hub
from effects import Effects
from settings import WIDTH, HEIGHT, GREEN

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 18)
small_font = pygame.font.SysFont("Consolas", 14)

CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = RADAR_RADIUS
enemies = []

for _ in range(TARGET_COUNT):
    angle = random.uniform(0, 360)
    dist = random.uniform(70, RADIUS - 20)

    x = CENTER[0] + math.cos(math.radians(angle)) * dist
    y = CENTER[1] + math.sin(math.radians(angle)) * dist

    aircraft_type = random.choice(
        ["Friendly", "Enemy", "Civilian", "Unknown"]
    )

    aircraft = Aircraft(
        x,
        y,
        random.uniform(-2, 2),
        random.uniform(-2, 2),
        aircraft_type
    )

    if aircraft_type == "Friendly":
        aircraft.id = f"F-{len([e for e in enemies if e.type == 'Friendly']) + 1:03}"
    elif aircraft_type == "Enemy":
        aircraft.id = f"E-{len([e for e in enemies if e.type == 'Enemy']) + 1:03}"
    elif aircraft_type == "Civilian":
        aircraft.id = f"C-{len([e for e in enemies if e.type == 'Civilian']) + 1:03}"
    else:
        aircraft.id = f"U-{len([e for e in enemies if e.type == 'Unknown']) + 1:03}"

    enemies.append(aircraft)

enemy_memory = [0] * len(enemies)

radar = Radar()
hub = Hub(font, GREEN)
effects = Effects()

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    for enemy in enemies:
        enemy.update()

    effects.draw_scan_lines(screen)

    for r in range(80, RADIUS + 1, 80):
        pygame.draw.circle(screen, DARK_GREEN, CENTER, r, 1)

    pygame.draw.line(screen, DARK_GREEN, (CENTER[0], 0), (CENTER[0], HEIGHT))
    pygame.draw.line(
        screen,
        DARK_GREEN,
        (0, CENTER[1]),
        (WIDTH, CENTER[1])
    )

    # Degree Labels
    for degree in range(0, 360, 30):
        x = CENTER[0] + math.cos(math.radians(degree)) * (RADIUS + 20)
        y = CENTER[1] + math.sin(math.radians(degree)) * (RADIUS + 20)

        text = small_font.render(str(degree), True, GREEN)

        screen.blit(
            text,
            (
                x - text.get_width() // 2,
                y - text.get_height() // 2
            )
        )

    for i in range(90):

        a = radar.angle + i * 2

        alpha = max(0, 180 - i * 2)

        sweep = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        p1 = CENTER

        p2 = (
            CENTER[0] + math.cos(math.radians(a - 1)) * RADIUS,
            CENTER[1] + math.sin(math.radians(a - 1)) * RADIUS
        )

        p3 = (
            CENTER[0] + math.cos(math.radians(a + 1)) * RADIUS,
            CENTER[1] + math.sin(math.radians(a + 1)) * RADIUS
        )

        pygame.draw.polygon(
            sweep,
            (0, 255, 70, alpha),
            [p1, p2, p3],
        )

        screen.blit(sweep, (0, 0))

    pygame.draw.circle(
        screen,
        GREEN,
        CENTER,
        RADIUS,
        2
    )

    effects.draw_glow(screen)

    for i, enemy in enumerate(enemies):

        x = enemy.x
        y = enemy.y

        enemy_angle = math.degrees(
            math.atan2(CENTER[1] - y, x - CENTER[0])
        )

        dif = abs((radar.angle - enemy_angle + 100) % 360 - 100)

        if dif < 2:

            if enemy_memory[i] == 0:
                sound.play_beep()

            enemy_memory[i] = 10

        if enemy_memory[i] > 0:

            enemy_memory[i] -= 1

            glow = pygame.Surface((40, 40), pygame.SRCALPHA)

            pygame.draw.circle(
                glow,
                (0, 255, 70, 70),
                (20, 20),
                14
            )

            screen.blit(glow, (x - 20, y - 20))

            if enemy_memory[i] % 2 == 0:
                enemy.draw(screen)

    radar.update()

    # Play sound once every full rotation
    if radar.angle == 0:
        sound.play_sweep()

    fps = int(clock.get_fps())

    hub.draw(
        screen,
        fps,
        len(enemies),
        radar.angle
    )

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()