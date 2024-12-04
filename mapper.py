import tkinter as tk
from tkinter import ttk
import pygame
import time
import threading
import numpy as np
import json

# Inicializar pygame mixer
pygame.mixer.init()

# Cargar música
pygame.mixer.music.load("resources/[PA] Geoxor - Virtual Arcadia 2020.mp3")

# Estado del metrónomo y mapeo
metronome_running = False
mapping_active = False
spawn_times = []

# Función para generar el sonido del metrónomo
def generate_metronome_sound(frequency=880, duration=0.1, volume=0.5):
    sample_rate = 44100  # Frecuencia de muestreo
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    wave = (wave * 32767).astype(np.int16)  # Convertir a 16 bits
    wave_stereo = np.column_stack((wave, wave))  # Convertir a estéreo
    sound = pygame.sndarray.make_sound(wave_stereo)
    sound.set_volume(volume)
    return sound

# Crear el sonido del metrónomo
metronome_sound = generate_metronome_sound()

# Función para iniciar/pausar la música
def toggle_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        music_button.config(text="Reproducir Música")
    else:
        pygame.mixer.music.play(-1)
        music_button.config(text="Pausar Música")

# Función para ejecutar el metrónomo
def run_metronome(bpm):
    global metronome_running
    interval = 60 / bpm  # Intervalo en segundos
    while metronome_running:
        metronome_sound.play()
        time.sleep(interval)

# Función para iniciar/pausar el metrónomo
def toggle_metronome():
    global metronome_running
    if metronome_running:
        metronome_running = False
        metronome_button.config(text="Iniciar Metrónomo")
    else:
        metronome_running = True
        bpm = int(bpm_entry.get())
        threading.Thread(target=run_metronome, args=(bpm,)).start()
        metronome_button.config(text="Detener Metrónomo")

# Función para registrar el tiempo de aparición
def map_enemy_spawn():
    if pygame.mixer.music.get_busy():
        current_time = pygame.mixer.music.get_pos()
        spawn_times.append(current_time)
        listbox.insert(tk.END, f"Enemigo en {current_time} ms")

# Función para guardar el mapeo en un archivo JSON
def save_mapping():
    with open("enemy_spawn_times.json", "w") as file:
        json.dump(spawn_times, file)
    status_label.config(text="Mapa guardado con éxito")

# Crear ventana principal
root = tk.Tk()
root.title("Mapper con Metrónomo y Mapeo")

# Botón para reproducir/pausar música
music_button = ttk.Button(root, text="Reproducir Música", command=toggle_music)
music_button.pack(pady=10)

# Entrada para BPM del metrónomo
bpm_label = ttk.Label(root, text="BPM del Metrónomo:")
bpm_label.pack(pady=5)
bpm_entry = ttk.Entry(root)
bpm_entry.insert(0, "120")  # Valor predeterminado
bpm_entry.pack(pady=5)

# Botón para iniciar/pausar el metrónomo
metronome_button = ttk.Button(root, text="Iniciar Metrónomo", command=toggle_metronome)
metronome_button.pack(pady=10)

# Botón para mapear el tiempo de aparición
map_button = ttk.Button(root, text="Mapear Aparición de Enemigo", command=map_enemy_spawn)
map_button.pack(pady=10)

# Listbox para mostrar los tiempos mapeados
listbox = tk.Listbox(root)
listbox.pack(pady=10)

# Botón para guardar el mapeo
save_button = ttk.Button(root, text="Guardar Mapa", command=save_mapping)
save_button.pack(pady=10)

# Etiqueta de estado
status_label = ttk.Label(root, text="")
status_label.pack(pady=5)

# Iniciar la interfaz de tkinter
root.mainloop()

# Cerrar pygame al salir
pygame.mixer.quit()
