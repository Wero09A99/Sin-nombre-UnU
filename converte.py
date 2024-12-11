import random
import json

# Cargar los archivos JSON
with open('enemy_spawn_times.json', 'r') as times_file:
    times = json.load(times_file)

with open('level-data.json', 'r') as obstacles_file:
    obstacles_data = json.load(obstacles_file)

# Definir formas y colores posibles
shapes = ["rectangle", "circle", "oval", "custom_shape"]
colors = [
    [255, 0, 0],  # rojo
    [0, 255, 0],  # verde
    [0, 0, 255],  # azul
    [255, 255, 0],  # amarillo
    [100, 50, 200],  # morado
    [50, 255, 50],  # verde claro
    [200, 0, 100],  # rosa
    [150, 200, 50],  # verde amarillento
    [255, 100, 50]   # naranja
]

# Crear una lista de obstáculos a partir de los tiempos
new_obstacles = []
for time in times:
    shape = random.choice(shapes)
    color = random.choice(colors)
    position = [random.randint(0, 600), random.randint(0, 400)]  # Posiciones aleatorias
    speed = random.uniform(3, 7)  # Velocidad aleatoria entre 3 y 7
    new_obstacles.append({
        "shape": shape,
        "position": position,
        "color": color,
        "spawn_time": time,
        "speed": speed
    })

# Añadir los obstáculos preexistentes del JSON original
new_obstacles.extend(obstacles_data["obstacles"])

# Crear el nuevo JSON
final_json = {
    "song": obstacles_data["song"],
    "obstacles": new_obstacles
}

# Guardar el JSON final en un archivo
with open("level-data.json", 'w') as output_file:
    json.dump(final_json, output_file, indent=4)

print("Archivo JSON generado: generated_obstacles.json")
