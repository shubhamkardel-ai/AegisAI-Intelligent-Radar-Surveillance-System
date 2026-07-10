import pygame
import math
import random
import sound
import time
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

    aircraft.altitude = random.randint(5000, 40000)

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

locked_target = None
auto_lock = True

collision_warning = False
collision_text = ""

radar = Radar()
hub = Hub(font, GREEN)
effects = Effects()

missiles = []
missile_speed = 8
explosion_active = False
explosion_x = 0
explosion_y = 0
explosion_radius = 5

kills = 0

missile_ready = True
reload_time = 3000      # milliseconds (3 seconds)
last_fire_time = 0

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                current_ticks = pygame.time.get_ticks()

                if locked_target and missile_ready:
                    missiles.append({

                        "x": CENTER[0],
                        "y": CENTER[1],
                        "target": locked_target

                    })

                    missile_ready = False
                    last_fire_time = current_ticks

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mx, my = pygame.mouse.get_pos()

            for aircraft in enemies:

                dx = aircraft.x - mx
                dy = aircraft.y - my

                if dx * dx + dy * dy < 25 * 25:
                    locked_target = aircraft

    screen.fill(BLACK)

    for enemy in enemies:

        if auto_lock:

            nearest = None
            nearest_distance = 999999

            for aircraft in enemies:

                if aircraft.type != "Enemy":
                    continue

                dx = aircraft.x - CENTER[0]
                dy = aircraft.y - CENTER[1]

                d = math.sqrt(dx * dx + dy * dy)

                if d < nearest_distance:
                    nearest_distance = d
                    nearest = aircraft

            locked_target = nearest

        enemy.update()

        collision_warning = False
        collision_text = ""

        for i in range(len(enemies)):

            for j in range(i + 1, len(enemies)):

                dx = enemies[i].x - enemies[j].x
                dy = enemies[i].y - enemies[j].y

                distance = math.sqrt(dx * dx + dy * dy)

                if distance < 40:
                    collision_warning = True

                    collision_text = (
                        f"{enemies[i].id} <-> {enemies[j].id}"
                    )

        if enemy.distance < 120:
            enemy.threat = "HIGH"
        elif enemy.distance < 220:
            enemy.threat = "MEDIUM"
        else:
            enemy.threat = "LOW"

    effects.draw_scan_lines(screen)

    for r in range(80, RADIUS + 1, 80):
        pygame.draw.circle(
            screen,
            DARK_GREEN,
            CENTER,
            r,
            1
        )

        range_text = small_font.render(
            f"{r} KM",
            True,
            GREEN
        )

        screen.blit(
            range_text,
            (
                CENTER[0] + 8,
                CENTER[1] - r - 10
            )
        )

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

    north = font.render(
        "N",
        True,
        LIGHT_GREEN
    )

    screen.blit(
        north,
        (
            CENTER[0] - 8,
            CENTER[1] - RADIUS - 45
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

    pygame.draw.circle(
        screen,
        LIGHT_GREEN,
        CENTER,
        5
    )

    for i, enemy in enumerate(enemies):

        distance = math.sqrt(
            (enemy.x - CENTER[0]) ** 2 +
            (enemy.y - CENTER[1]) ** 2
        )

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

            if locked_target == enemy:
                pygame.draw.circle(
                    screen,
                    RED,
                    (int(enemy.x), int(enemy.y)),
                    15,
                    2
                )

            enemy_memory[i] -= 1

            glow = pygame.Surface((40, 40), pygame.SRCALPHA)

            pygame.draw.circle(
                glow,
                (0, 255, 70, 70),
                (20, 20),
                14
            )

            if distance <= RADIUS:
                screen.blit(glow, (x - 20, y - 20))

            if enemy_memory[i] % 2 == 0:
                if distance <= RADIUS:
                    enemy.draw(screen)

    for missile in missiles[:]:

        target = missile["target"]

        if target not in enemies:
            missiles.remove(missile)
            continue

        dx = target.x - missile["x"]
        dy = target.y - missile["y"]

        distance = math.sqrt(dx * dx + dy * dy)

        if distance > missile_speed:

            missile["x"] += dx / distance * missile_speed
            missile["y"] += dy / distance * missile_speed

        else:

            explosion_active = True

            explosion_x = target.x
            explosion_y = target.y

            if target in enemies:
                enemies.remove(target)
                kills += 1

            missiles.remove(missile)

        pygame.draw.circle(
            screen,
            RED,
            (int(missile["x"]), int(missile["y"])),
            4
        )
    current_ticks = pygame.time.get_ticks()

    if not missile_ready:

        if current_ticks - last_fire_time >= reload_time:
            missile_ready = True

    radar.update()
    
    # Play sound once every full rotation
    if radar.angle == 0:
        sound.play_sweep()

    fps = int(clock.get_fps())
    current_time = time.strftime("%H:%M:%S")

    friendly_count = sum(1 for e in enemies if e.type == "Friendly")
    enemy_count = sum(1 for e in enemies if e.type == "Enemy")
    civilian_count = sum(1 for e in enemies if e.type == "Civilian")
    unknown_count = sum(1 for e in enemies if e.type == "Unknown")

    high_threat = sum(1 for e in enemies if e.threat == "HIGH")

    hub.draw(
        screen,
        fps,
        len(enemies),
        radar.angle
    )

    stats = [

        "RADAR STATUS",

        f"Friendly : {friendly_count}",
        f"Enemy    : {enemy_count}",
        f"Civilian : {civilian_count}",
        f"Unknown  : {unknown_count}",

        "",
        f"Locked : {locked_target.id if locked_target else 'NONE'}",

        "",
        f"High Threat : {high_threat}",

        "",
        f"KILLS : {kills}",

        "",
        f"MISSILE : {'READY' if missile_ready else 'RELOADING'}",

        "",
        f"FPS : {fps}",

        "Radar : ONLINE",

        "",
        f"TIME : {current_time}"
    ]

    for i, line in enumerate(stats):
        text = small_font.render(
            line,
            True,
            GREEN
        )

        screen.blit(
            text,
            (760, 430 + i * 22)
        )

    # Target Information Panel
    if locked_target:

        panel_x = WIDTH - 260
        panel_y = 120

        pygame.draw.rect(
            screen,
            DARK_GREEN,
            (panel_x, panel_y, 240, 180),
            2
        )

        info_font = pygame.font.SysFont("Consolas", 16)

        lines = [
            "TARGET INFORMATION",
            "",
            f"ID   : {locked_target.id}",
            f"TYPE : {locked_target.type}",
            f"SPD  : {locked_target.speed}",
            f"HDG  : {int(locked_target.heading)}°",
            f"ALT  : {locked_target.altitude} FT",
            f"DST  : {locked_target.distance} PX",
            f"THREAT : {locked_target.threat}",
            "STATUS : TRACKED"
        ]

        for i, line in enumerate(lines):
            text = info_font.render(
                line,
                True,
                GREEN
            )

            screen.blit(
                text,
                (panel_x + 10, panel_y + 10 + i * 20)
            )

    if collision_warning:
        warning = font.render(
            "COLLISION WARNING",
            True,
            RED
        )

        ids = small_font.render(
            collision_text,
            True,
            RED
        )

        screen.blit(
            warning,
            (20, 20)
        )

        screen.blit(
            ids,
            (20, 50)
        )

    if explosion_active:

        pygame.draw.circle(
            screen,
            (255, 120, 0),
            (int(explosion_x), int(explosion_y)),
            explosion_radius
        )

        explosion_radius += 2

        if explosion_radius > 30:
            explosion_active = False
            explosion_radius = 5

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()