import json
import random

# Ruta del archivo JSON
json_file = "level-data.json"

# Cargar los datos del JSON
with open(json_file, "r") as file:
    level_data = json.load(file)

# Añadir velocidad predeterminada a los obstáculos que no tienen 'speed'
for obstacle in level_data["obstacles"]:
    if "speed" not in obstacle:
        obstacle["speed"] = random.uniform(3, 7)  # Velocidad aleatoria entre 3 y 7

# Guardar el archivo JSON actualizado
with open(json_file, "w") as file:
    json.dump(level_data, file, indent=4)

print(f"Archivo JSON actualizado: {json_file}")
