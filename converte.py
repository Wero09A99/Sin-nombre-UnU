import random
import json

# Cargar los archivos JSON
with open('enemy_spawn_times.json', 'r') as times_file:
    times = json.load(times_file)

# Definir formas, colores y fondos posibles (Paleta "cute")
shapes = ["rectangle", "circle", "oval", "custom_shape"]
colors = [
    [255, 182, 193],  # rosa claro
    [255, 228, 225],  # rosa pálido
    [173, 216, 230],  # azul claro
    [255, 240, 245],  # lavanda muy suave
    [144, 238, 144],  # verde menta
    [255, 222, 173],  # amarillo claro
    [255, 218, 185],  # melocotón claro
    [255, 255, 224],  # amarillo pastel
    [255, 182, 193]   # rosa pastel
]
bg_color = [
    [160, 120, 190],  # Lavanda oscuro
    [90, 120, 150],   # Azul oscuro suave
    [120, 100, 160],  # Morado suave
    [180, 130, 180]   # Rosa oscuro suave
]
directions = ["center_to_outside", "top_to_bottom", "left_to_right", "edges_to_center"]

# Crear una lista de nuevos obstáculos a partir de los tiempos
new_obstacles = []
for time in times:
    shape = random.choice(shapes)
    color = random.choice(colors)
    direction = random.choice(directions)
    position = [random.randint(0, 800), random.randint(0, 600)]  # Posiciones aleatorias
    speed = random.uniform(4, 7)  # Velocidad aleatoria entre 3 y 7
    size = random.randint(50, 100)  # Tamaño aleatorio entre 20 y 60

    new_obstacles.append({
        "shape": shape,
        "position": position,
        "direction": direction,
        "color": color,
        "spawn_time": time,
        "speed": speed,
        "size": size
    })

# Crear el nuevo JSON, incluyendo el nombre del nivel y el color de fondo
level_name = "First Test"  # Cambia el nombre según sea necesario
background_color = random.choice(bg_color)  # Definir el color de fondo, puedes cambiarlo según quieras

final_json = {
    "song": "resources/[PA] Geoxor - Virtual Arcadia 2020.ogg",  # Define la ruta de la canción
    "level_name": level_name,  # Nuevo campo para el nombre del nivel
    "background_color": background_color,  # Campo añadido para el color de fondo
    "obstacles": new_obstacles
}

# Guardar el JSON final en un archivo
with open("level-data.json", 'w') as output_file:
    json.dump(final_json, output_file, indent=4)

print("Archivo JSON generado: level-data.json")
