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
pygame.display.set_caption("Un juego simple")

# Colores
PLAYER_COLOR = (135, 206, 250)  # Azul claro
FIRE_COLORS = [(255, 69, 0), (255, 140, 0), (255, 215, 0)]  # Colores de fuego
BACKGROUND_COLOR = (160, 120, 190)  # Lavanda oscuro por defecto

# Jugador
player_size = 30
player_speed = 14
dash_speed = 18
dash_duration = 300  # Duración del dash en milisegundos
dash_cooldown = 400  # Tiempo entre dashes en milisegundos
dash_duration = 300  # Duración del dash en milisegundos
game_over = False
player_pos = [WIDTH // 2 - player_size // 2, HEIGHT // 2 - player_size // 2]
is_dashing = False
last_dash_time = 0
dash_start_time = 0
lives = 3  # Cantidad inicial de vidas


# Variables del juego
obstacles = []
particles = []
game_over = False  # Estado del juego
spawn_index = 0
current_time = 0


# Cargar datos de nivel
json_file = "level-data.json"
with open(json_file, "r") as file:
    level_data = json.load(file)

song_path = level_data["song"]
obstacles_data = level_data["obstacles"]
level_name = level_data.get("level_name", "Unknown Level")
background_color = tuple(level_data["background_color"])

# Reproducir la canción
pygame.mixer.music.load(song_path)
pygame.mixer.music.play(loops=-1)  # Reproducir en bucle

# Fuente para texto
font = pygame.font.SysFont(None, 30)

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

# Función para verificar colisión
def check_collision(player, obstacle):
    """Verifica si hay colisión entre el jugador y un obstáculo."""
    if obstacle.shape == "rectangle":
        return player[0] < obstacle.x + 40 and player[0] + player_size > obstacle.x and \
               player[1] < obstacle.y + 40 and player[1] + player_size > obstacle.y
    elif obstacle.shape == "circle":
        distance = ((player[0] + player_size // 2 - obstacle.x) ** 2 +
                    (player[1] + player_size // 2 - obstacle.y) ** 2) ** 0.5
        return distance < player_size // 2 + 20
    elif obstacle.shape == "oval":
        oval_width, oval_height = 60, 30
        dx = abs(player[0] + player_size // 2 - (obstacle.x + oval_width // 2))
        dy = abs(player[1] + player_size // 2 - (obstacle.y + oval_height // 2))
        return dx < (player_size // 2 + oval_width // 2) and dy < (player_size // 2 + oval_height // 2)
    elif obstacle.shape == "custom_shape":
        triangle_width, triangle_height = 60, 50
        dx = abs(player[0] + player_size // 2 - obstacle.x)
        dy = abs(player[1] + player_size // 2 - obstacle.y)
        return dx < triangle_width // 2 and dy < triangle_height // 2
    return False

# Clase para las partículas
class Particle:
    def __init__(self, x, y, is_dashing):
        self.x = x
        self.y = y
        self.size = random.randint(5, 15) if not is_dashing else random.randint(5, 15)
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


# Función para dibujar el texto
def draw_texts(level_name, lives):
    level_text = font.render(f"Level: {level_name}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {lives}", True, (255, 0, 0))
    screen.blit(level_text, (10, 10))
    screen.blit(lives_text, (10, 40))


# Función para manejar el movimiento del jugador
def handle_player_movement(keys, player_pos, is_dashing):
    speed = dash_speed if is_dashing else player_speed
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= speed
    if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size:
        player_pos[1] += speed



# Bucle principal del juego
while True:
    screen.fill(background_color)
    current_time = pygame.mixer.music.get_pos()  # Tiempo transcurrido desde que inició la canción

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw_texts(level_name, lives)

    if not game_over:
        keys = pygame.key.get_pressed()

        # Manejo de Dash
        if keys[pygame.K_SPACE] and current_time - last_dash_time >= dash_cooldown:
            is_dashing = True
            dash_start_time = current_time
            last_dash_time = current_time

        if is_dashing and current_time - dash_start_time >= dash_duration:
            is_dashing = False

        handle_player_movement(keys, player_pos, is_dashing)

        # Generar partículas detrás del jugador
        for _ in range(5 if is_dashing else 1):
            particles.append(Particle(player_pos[0] + player_size // 2, player_pos[1] + player_size // 2, is_dashing))

        for particle in particles[:]:
            particle.update()
            if particle.is_alive():
                pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y)), int(particle.size))
            else:
                particles.remove(particle)

        # Dibujar jugador
        if is_dashing:
            pygame.draw.circle(screen, random.choice(FIRE_COLORS), (player_pos[0] + player_size // 2, player_pos[1] + player_size // 2), player_size)
        else:
            pygame.draw.rect(screen, PLAYER_COLOR, (player_pos[0], player_pos[1], player_size, player_size))

        # Generar nuevos obstáculos basados en el tiempo
        if spawn_index < len(obstacles_data) and current_time >= obstacles_data[spawn_index]["spawn_time"]:
            data = obstacles_data[spawn_index]
            obstacles.append(Obstacle(data["shape"], data["position"], data["color"], data["speed"], data["direction"]))
            spawn_index += 1
        # Actualizar y dibujar obstáculos
        for obstacle in obstacles[:]:
            obstacle.update()
            obstacle.draw(screen)
            if check_collision(player_pos, obstacle):
                lives -= 1
                obstacles.remove(obstacle)
                if lives <= 0:
                    game_over = True
                            # Manejar colisiones
        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw(screen)
            if not is_dashing and check_collision(player_pos, obstacle):
                print("¡Colisión!")
                lives -= 1  # Reducir una vida al jugador
                if lives <= 0:
                    print("¡Has perdido todas tus vidas!")
                    game_over = True

    else:
        # Mostrar texto de Game Over
        game_over_text = font.render("Game Over! Press R to restart or Q to quit.", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reiniciar el juego
            player_pos = [WIDTH // 2, HEIGHT - 100]
            lives = 3
            obstacles = []
            particles = []
            # Jugador
            player_size = 30
            player_speed = 14
            dash_speed = 18
            dash_duration = 300  # Duración del dash en milisegundos
            dash_cooldown = 400  # Tiempo entre dashes en milisegundos
            dash_duration = 300  # Duración del dash en milisegundos
            game_over = False
            player_pos = [WIDTH // 2 - player_size // 2, HEIGHT // 2 - player_size // 2]
            is_dashing = False
            last_dash_time = 0
            dash_start_time = 0
            lives = 3  # Cantidad inicial de vidas

# Tiempo entre dashes en milisegundos
            is_dashing = False

            spawn_index = 0
            game_over = False
            pygame.mixer.music.play(loops=-1)
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

    # Actualizar pantalla
    pygame.display.flip()
    pygame.time.Clock().tick(60)
