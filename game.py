import pygame
import sys
import json
import random

# Inicialización de pygame
pygame.init()
pygame.mixer.init()

# Configuración de pantalla
WIDTH, HEIGHT = 1000, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UwU")

PLAYER_COLOR = (135, 206, 250)
FIRE_COLORS = [(255, 69, 0), (255, 140, 0), (255, 215, 0)]

# Jugador
player_size = 30
player_pos = [WIDTH // 2, HEIGHT - 100]
player_speed = 5
dash_speed = 15
dash_duration = 300  # Duración del dash en milisegundos
dash_cooldown = 400  # Tiempo entre dashes en milisegundos
is_dashing = False
dash_start_time = 0
last_dash_time = 0

# Obstáculos
json_archive = "level-data.json"

# Fuente para texto
font = pygame.font.SysFont(None, 30)

# Leer datos del nivel desde el archivo JSON
with open(json_archive, "r") as file:
    level_data = json.load(file)
    song_path = level_data["song"]
    obstacles_data = level_data["obstacles"]
    level_name = level_data.get("level_name", "Unknown Level")  # Obtener el nombre del nivel
    # Obtener el color de fondo
    background_color = level_data["background_color"]

# Reproducir la canción
pygame.mixer.music.load(song_path)
pygame.mixer.music.play(loops=-1)  # Reproducir en bucle

# Clase para un obstáculo
class Obstacle:
    def __init__(self, shape, position, color, speed, direction):
        self.shape = shape
        self.x, self.y = position
        self.color = tuple(color)
        self.speed = speed
        self.direction = direction
        self.init_position()

    def init_position(self):
        """Inicializa la posición según la dirección."""
        if self.direction == "center_to_outside":
            self.x, self.y = WIDTH // 2, HEIGHT // 2
        elif self.direction == "top_to_bottom":
            self.x = random.randint(0, WIDTH)
            self.y = 0
        elif self.direction == "left_to_right":
            self.x = 0
            self.y = random.randint(0, HEIGHT)
        elif self.direction == "edges_to_center":
            edge = random.choice(["top", "bottom", "left", "right"])
            if edge == "top":
                self.x = random.randint(0, WIDTH)
                self.y = 0
            elif edge == "bottom":
                self.x = random.randint(0, WIDTH)
                self.y = HEIGHT
            elif edge == "left":
                self.x = 0
                self.y = random.randint(0, HEIGHT)
            elif edge == "right":
                self.x = WIDTH
                self.y = random.randint(0, HEIGHT)

    def update(self):
        """Actualiza la posición del obstáculo según su dirección."""
        if self.direction == "center_to_outside":
            if self.x < WIDTH // 2:
                self.x -= self.speed
            else:
                self.x += self.speed

            if self.y < HEIGHT // 2:
                self.y -= self.speed
            else:
                self.y += self.speed

        elif self.direction == "top_to_bottom":
            self.y += self.speed

        elif self.direction == "left_to_right":
            self.x += self.speed

        elif self.direction == "edges_to_center":
            if self.x < WIDTH // 2:
                self.x += self.speed
            else:
                self.x -= self.speed

            if self.y < HEIGHT // 2:
                self.y += self.speed
            else:
                self.y -= self.speed

    def draw(self, screen):
        """Dibuja el obstáculo en pantalla."""
        if self.shape == "rectangle":
            pygame.draw.rect(screen, self.color, (self.x, self.y, 40, 40))
        elif self.shape == "circle":
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 20)
        elif self.shape == "oval":
            pygame.draw.ellipse(screen, self.color, (self.x, self.y, 60, 30))
        elif self.shape == "custom_shape":
            pygame.draw.polygon(screen, self.color, [
                (self.x, self.y),
                (self.x + 30, self.y + 50),
                (self.x - 30, self.y + 50)
            ])

# Clase para las partículas
class Particle:
    def __init__(self, x, y, is_dashing):
        self.x = x
        self.y = y
        self.size = random.randint(2, 10) if not is_dashing else random.randint(5, 15)
        self.color = (255, 255, 255) if not is_dashing else random.choice(FIRE_COLORS)
        self.life = 60
        self.vx = random.uniform(-2, 2) if is_dashing else random.uniform(-1, 1)
        self.vy = random.uniform(-2, 2) if is_dashing else random.uniform(-1, 1)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size -= 0.2

    def is_alive(self):
        return self.life > 0 and self.size > 0

# Variables para el juego
running = True
clock = pygame.time.Clock()
spawn_index = 0
obstacles = []
particles = []  # Lista de partículas activas

# Bucle principal del juego
while running:
    screen.fill(background_color)
    current_time = pygame.mixer.music.get_pos()  # Tiempo transcurrido desde que inició la canción

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Dibujar texto del nivel
    level_text = font.render(f"Level: {level_name}", True, (255, 255, 255))  # Texto en color blanco
    screen.blit(level_text, (10, 10))  # Dibujar en la esquina superior izquierda

    # Movimiento del jugador
    keys = pygame.key.get_pressed()

    # Activar dash
    if keys[pygame.K_SPACE] and not is_dashing and current_time - last_dash_time >= dash_cooldown:
        is_dashing = True
        dash_start_time = current_time
        last_dash_time = current_time

    # Aplicar velocidad del jugador (dash o normal)
    speed = dash_speed if is_dashing else player_speed

    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= speed
    if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size:
        player_pos[1] += speed

    # Desactivar dash después de la duración
    if is_dashing and current_time - dash_start_time >= dash_duration:
        is_dashing = False

    # Generar partículas detrás del jugador
    for _ in range(5 if is_dashing else 1):
        particles.append(Particle(player_pos[0] + player_size // 2, player_pos[1] + player_size // 2, is_dashing))

    # Actualizar partículas
    for particle in particles[:]:
        particle.update()
        if particle.is_alive():
            pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y)), int(particle.size))
        else:
            particles.remove(particle)

    # Dibujar jugador (círculo si está dashing, cuadrado si no)
    if is_dashing:
        pygame.draw.circle(screen, random.choice(FIRE_COLORS), (player_pos[0] + player_size // 2, player_pos[1] + player_size // 2), player_size)
    else:
        pygame.draw.rect(screen, PLAYER_COLOR, (player_pos[0], player_pos[1], player_size, player_size))

    # Generar nuevos obstáculos basados en el tiempo
    if spawn_index < len(obstacles_data) and current_time >= obstacles_data[spawn_index]["spawn_time"]:
        data = obstacles_data[spawn_index]
        obstacle = Obstacle(data["shape"], data["position"], data["color"], data["speed"], data["direction"])
        obstacles.append(obstacle)
        spawn_index += 1

    # Dibujar y actualizar obstáculos
    for obstacle in obstacles:
        obstacle.update()
        obstacle.draw(screen)
        if not is_dashing:
            # Detectar colisiones
            if player_pos[0] < obstacle.x + 40 and player_pos[0] + player_size > obstacle.x and \
            player_pos[1] < obstacle.y + 40 and player_pos[1] + player_size > obstacle.y:
                print("¡Colisión! Has perdido.")
                running = False

    pygame.display.flip()
    clock.tick(60)
