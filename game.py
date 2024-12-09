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

# TITULO
TITLE_LEVEL = "Level: First test"

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PA_Project-Arrhythmia_Clone")

# Paleta de colores
BG_COLOR = (15, 15, 35)          # Fondo oscuro con un toque morado
OBSTACLE_COLOR = (138, 43, 226)  # Morado fuerte
PLAYER_COLOR = (135, 206, 250)   # Azul claro
PARTICLE_COLOR = (255, 255, 255) # Blanco para partículas
TEXT_COLOR = (200, 200, 200)     # Gris claro

# Jugador
player_size = 30
player_pos = [WIDTH // 2, HEIGHT - 100]
player_speed = 5

# Variables para dasheo
dash_speed = 15
dash_duration = 10  # Duración en frames
dash_cooldown = 500  # Tiempo de espera en milisegundos
last_dash_time = 0
is_dashing = False
dash_frames = 0
dash_direction = [0, 0]

# Obstáculos
obstacle_size = 40
obstacles = []
obstacle_speed = 5
obstacles_itertion = 10

# Fuente para texto
font = pygame.font.SysFont(None, 24)

# Cargar los tiempos desde el archivo JSON
with open("enemy_spawn_times.json", "r") as file:
    enemy_spawn_times = json.load(file)

# Clase para las partículas
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 10)
        self.color = PARTICLE_COLOR
        self.life = 60
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size -= 0.2

    def is_alive(self):
        return self.life > 0 and self.size > 0

# Lista para las partículas
particles = []

# Loop principal del juego
running = True
spawn_index = 0
clock = pygame.time.Clock()

while running:
    screen.fill(BG_COLOR)

    # Obtener tiempo actual
    current_time = pygame.time.get_ticks()

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Manejo de dasheo
    keys = pygame.key.get_pressed()
    current_dash_time = pygame.time.get_ticks()

    if not is_dashing:
        # Detectar inicio de dasheo
        if keys[pygame.K_SPACE]:
            direction = [0, 0]
            if keys[pygame.K_LEFT]:
                direction[0] = -1
            elif keys[pygame.K_RIGHT]:
                direction[0] = 1
            if keys[pygame.K_UP]:
                direction[1] = -1
            elif keys[pygame.K_DOWN]:
                direction[1] = 1

            # Normalizar la dirección para diagonales
            if direction != [0, 0]:
                length = (direction[0]**2 + direction[1]**2) ** 0.5
                direction = [direction[0]/length, direction[1]/length]

                # Verificar cooldown
                if current_dash_time - last_dash_time >= dash_cooldown:
                    is_dashing = True
                    dash_frames = 0
                    dash_direction = direction
                    last_dash_time = current_dash_time
    else:
        # Realizar dasheo
        player_pos[0] += dash_direction[0] * dash_speed
        player_pos[1] += dash_direction[1] * dash_speed

        # Limitar la posición del jugador dentro de la pantalla
        player_pos[0] = max(0, min(WIDTH - player_size, player_pos[0]))
        player_pos[1] = max(0, min(HEIGHT - player_size, player_pos[1]))

        dash_frames += 1
        if dash_frames >= dash_duration:
            is_dashing = False

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

    # Movimiento del jugador si no está dasheando
    if not is_dashing:
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size:
            player_pos[1] += player_speed

    # Crear partículas detrás del jugador
    particles.append(Particle(player_pos[0] + player_size // 2, player_pos[1] + player_size // 2))

    # Actualizar y dibujar partículas
    for particle in particles[:]:
        particle.update()
        if particle.is_alive():
            pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y)), int(particle.size))
        else:
            particles.remove(particle)

    # Dibujar jugador
    pygame.draw.rect(screen, PLAYER_COLOR, (player_pos[0], player_pos[1], player_size, player_size))

    # Mover y dibujar obstáculos
    obstacles_to_remove = []
    for obstacle in obstacles:
        obstacle[1] += obstacle_speed
        pygame.draw.rect(screen, OBSTACLE_COLOR, (obstacle[0], obstacle[1], obstacle_size, obstacle_size))

        # Detectar colisiones
        if (player_pos[0] < obstacle[0] + obstacle_size and
            player_pos[0] + player_size > obstacle[0] and
            player_pos[1] < obstacle[1] + obstacle_size and
            player_pos[1] + player_size > obstacle[1]):
            print("¡Colisión! Has perdido.")
            running = False

        # Eliminar obstáculos que están fuera de la pantalla
        if obstacle[1] > HEIGHT:
            obstacles_to_remove.append(obstacle)

    # Eliminar los obstáculos que están fuera de la pantalla
    for obstacle in obstacles_to_remove:
        obstacles.remove(obstacle)

    # Dibujar texto
    text = font.render(TITLE_LEVEL, True, TEXT_COLOR)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
