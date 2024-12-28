import json

json_file = "level-data.json"
try:
    with open(json_file, "r") as file:
        data = json.load(file)
        print(data)
except Exception as e:
    print(f"Error leyendo el archivo JSON: {e}")
