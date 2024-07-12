import PySimpleGUI as sg
import cv2
import numpy as np
from PIL import Image
import random

# Função para capturar frames do vídeo e convertê-los para um formato que o PySimpleGUI possa exibir
def get_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (640, 480))  # Ajustar o tamanho do frame se necessário
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        yield imgbytes
    cap.release()

# Lista de vídeos de reações aleatórias
reaction_videos = [
    'videos/angryrobot.gif',
    'videos/sadrobot.gif',
    'videos/badrobot.gif',
    'videos/loverobot.gif'
    
]

# Vídeo padrão
default_video = 'videos/padraorobot.gif'

# Função para escolher um vídeo de reação aleatoriamente
def get_random_video():
    return random.choice(reaction_videos)

# Layout da interface principal com um elemento de imagem para exibir o vídeo
layout = [
    [sg.Image(filename='', key='-IMAGE-', enable_events=True)],  # Habilita eventos para o elemento de imagem
]

# Criar a janela principal
window = sg.Window("Olhos de Robo", layout)

# Inicializar o vídeo atual e o gerador de frames
current_video = default_video
frame_generator = get_frame(current_video)

# Loop de eventos
while True:
    event, values = window.read(timeout=20)  # Tempo de timeout para atualizar o vídeo
    if event == sg.WIN_CLOSED:
        break
    elif event == '-IMAGE-':  # Detecta clique na imagem
        current_video = get_random_video()
        frame_generator = get_frame(current_video)

    try:
        # Atualizar o frame no elemento de imagem
        frame = next(frame_generator)
        window['-IMAGE-'].update(data=frame)
    except StopIteration:
        # Quando o vídeo terminar, voltar ao vídeo padrão
        current_video = default_video
        frame_generator = get_frame(current_video)

window.close()
