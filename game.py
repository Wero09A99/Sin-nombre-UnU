import pygame
import sys
import json
import random

# Inicialización de pygame
pygame.init()

# Cargar música
pygame.mixer.init()
pygame.mixer.music.load("resources/[PA] Geoxor - Virtual Arcadia 2020.ogg")  # Reemplaza con la ruta a tu archivo de música
pygame.mixer.music.play(loops=-1)  # Reproduce la música en bucle

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PA_Project-Arrhythmia_Clone")

# Colores
BG_COLOR = (85, 0, 108 )
RED = (255, 0, 0)
PLAYER_COLOR = (0, 0, 255)

# Jugador
player_size = 30
player_pos = [WIDTH // 2, HEIGHT - 100]
player_speed = 5

# Obstáculos
obstacle_size = 40
obstacles = []
obstacle_speed = 5
obstacles_itertion = 10

# Cargar los tiempos desde el archivo JSON
with open("enemy_spawn_times.json", "r") as file:
    enemy_spawn_times = json.load(file)

# Loop principal del juego
running = True
spawn_index = 0
clock = pygame.time.Clock()

while running:
    screen.fill(BG_COLOR)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Obtener tiempo actual
    current_time = pygame.time.get_ticks()

    # Generar enemigos en tiempos mapeados
    if spawn_index < len(enemy_spawn_times) and current_time >= enemy_spawn_times[spawn_index]:
        for _ in range(obstacles_itertion):
            side = random.choice(["top", "left", "right"])
            if side == "top":
                obstacles.append([random.randint(0, WIDTH - obstacle_size), 0])
            elif side == "left":
                obstacles.append([0, random.randint(0, HEIGHT - obstacle_size)])
            else:
                obstacles.append([WIDTH - obstacle_size, random.randint(0, HEIGHT - obstacle_size)])
        spawn_index += 1

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size:
        player_pos[1] += player_speed

    # Dibujar jugador
    pygame.draw.rect(screen, PLAYER_COLOR, (player_pos[0], player_pos[1], player_size, player_size))

    # Mover y dibujar obstáculos
    obstacles_to_remove = []
    for obstacle in obstacles:
        obstacle[1] += obstacle_speed
        pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle_size, obstacle_size))

        # Detectar colisiones
        if player_pos[0] < obstacle[0] + obstacle_size and player_pos[0] + player_size > obstacle[0] and \
           player_pos[1] < obstacle[1] + obstacle_size and player_pos[1] + player_size > obstacle[1]:
            print("¡Colisión! Has perdido.")
            running = False

        # Eliminar obstáculos que están fuera de la pantalla
        if obstacle[1] > HEIGHT:
            obstacles_to_remove.append(obstacle)

    # Eliminar los obstáculos que están fuera de la pantalla
    for obstacle in obstacles_to_remove:
        obstacles.remove(obstacle)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
