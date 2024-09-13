import tkinter as tk
from PIL import Image, ImageTk
import imageio
import time
import random
import threading

# Função para pré-carregar os frames dos vídeos
def preload_frames(video_path, screen_width, screen_height):
    reader = imageio.get_reader(video_path)
    frames = []
    for frame in reader:
        img = Image.fromarray(frame)
        img = img.resize((screen_width, screen_height))  # Redimensionar o frame para preencher a tela
        img_tk = ImageTk.PhotoImage(img)
        frames.append(img_tk)
    reader.close()
    return frames

# Função para atualizar os frames
def play_video():
    global frame_index, video_playing, current_frames
    if video_playing:
        try:
            frame = current_frames[frame_index]
            label.config(image=frame)
            label.image = frame
            frame_index += 1
            if frame_index >= len(current_frames):  # Termina o vídeo de clique e volta ao padrão
                if current_frames != normal_frames:  # Se não for o vídeo padrão
                    current_frames = normal_frames
                    frame_index = 0
                    enable_clicks()  # Habilitar cliques novamente após o vídeo acabar
                else:
                    frame_index = 0  # Loop para o vídeo padrão
        except IndexError:
            frame_index = 0

    # Continuar rodando enquanto video_playing for True
    root.after(20, play_video)

# Função para desabilitar cliques
def disable_clicks():
    label.unbind("<ButtonPress-1>")
    label.unbind("<ButtonRelease-1>")

# Função para habilitar cliques
def enable_clicks():
    label.bind("<ButtonPress-1>", on_mouse_down)
    label.bind("<ButtonRelease-1>", on_mouse_up)

# Vídeo padrão
normalBingo = 'videos/Normal_Bingo.gif'
angryBingo = 'videos/Angry_Bingo.gif'
sadBingo = 'videos/Sad_Bingo.gif'
happyBingo = 'videos/Happy_Bingo.gif'

fastClick = [sadBingo, angryBingo]

root = tk.Tk()
root.attributes("-fullscreen", True)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

label = tk.Label(root)
label.pack()

# Pré-carregar frames dos vídeos
normal_frames = preload_frames(normalBingo, screen_width, screen_height)
angry_frames = preload_frames(angryBingo, screen_width, screen_height)
sad_frames = preload_frames(sadBingo, screen_width, screen_height)
happy_frames = preload_frames(happyBingo, screen_width, screen_height)

current_frames = normal_frames
frame_index = 0

mouse_down_time = None
long_click_duration = 0.5  # Duração em segundos para considerar um clique longo

video_playing = True

# Funções para detectar clique longo e curto
def on_mouse_down(event):
    global mouse_down_time
    mouse_down_time = time.time()

def on_mouse_up(event):
    global mouse_down_time, video_playing, current_frames, frame_index
    if mouse_down_time is not None:
        click_duration = time.time() - mouse_down_time
        mouse_down_time = None
        if click_duration >= long_click_duration:
            current_frames = happy_frames  # Clique longo
            print("clique longo")
        else:
            current_frames = random.choice([sad_frames, angry_frames])  # Clique curto
            print("clique rápido")

        disable_clicks()  # Desabilitar cliques enquanto o vídeo está rodando
        frame_index = 0  # Reiniciar do início
        video_playing = True

label.bind("<ButtonPress-1>", on_mouse_down)
label.bind("<ButtonRelease-1>", on_mouse_up)

# Iniciar a reprodução do vídeo padrão
root.after(20, play_video)

root.mainloop()
